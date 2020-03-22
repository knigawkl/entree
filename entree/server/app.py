import datetime
import jwt
import os
import errno
import bcrypt
from flask import Flask, jsonify, request, redirect, url_for, make_response, send_file
from flask_cors import CORS
from flask_mysqldb import MySQL


def check_if_login_exists(login: str):
    cur = mysql.connection.cursor()
    query = f"select count(*) from users where user = '{login}';"
    cur.execute(query)
    res = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return res[0]


def insert_new_user(login: str, email: str, password: str):
    cur = mysql.connection.cursor()
    query = f"insert into users (user, email, password) values ('{login}', '{email}', '{password}')"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()


def get_pass(login: str):
    cur = mysql.connection.cursor()
    query = f"select password from users where user = '{login}';"
    cur.execute(query)
    res = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return res[0] if res else None


def get_entrees():
    entrees = []
    cur = mysql.connection.cursor()
    query = f"select * from entrees"
    cur.execute(query)
    res = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for row in res:
        entree_dict = {"id": row[0], "name": row[1], "files": "", "date": str(row[2])}
        entrees.append(entree_dict)
    return entrees


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'customerobsessed'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'entree'

CORS(app)
mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register/', methods=['POST', 'PUT'])
def register():
    req = request.get_json()
    login = req['login']
    if login and check_if_login_exists(login):
        resp = jsonify('Username unavailable')
        return resp
    elif login and not check_if_login_exists(login):
        resp = jsonify('Username available')
    if request.method == 'PUT':
        password, email = req['password'], req['email']

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)
        hashed = hashed.decode("utf-8")

        insert_new_user(login=login, email=email, password=hashed)
    return resp


@app.route('/login/', methods=['POST'])
def login():
    auth = request.get_json()
    login, password = auth['login'], auth['password']

    db_pass = get_pass(login=login)

    if auth and db_pass and bcrypt.checkpw(password.encode('utf8'), db_pass.encode('utf8')):
        token = jwt.encode({'user': auth['login'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Authorization failed', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/logout/', methods=['POST'])
def logout():
    return make_response('Logged out', 200)


@app.route('/hub/', methods=['GET', 'POST'])
def hub():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()

        # todo dodawanie rezerwacji do db
        id = str(post_data.get('id'))
        db.hset(id, 'id', id)
        db.hset(id, 'title', post_data.get('title'))
        db.hset(id, 'author', post_data.get('author'))
        db.hset(id, 'year', post_data.get('year'))

        db.sadd('books', id)
        response_object['message'] = 'Book added!'
    else:
        response_object['entrees'] = get_entrees()
    return jsonify(response_object)


def remove_entree(book_id):
    db_resp = db.smembers('books')
    for member in db_resp:
        if member == book_id:
            db.hdel(member, 'id', 'title', 'author', 'year', 'file')
            db.srem('books', member)
            return True
    return False


@app.route('/hub/<book_id>', methods=['PUT', 'DELETE'])
def entree(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        id = book_id
        response_object['message'] = 'File added!'
    if request.method == 'DELETE':
        remove_entree(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def save_file(file, id):
    path = f"files/{id}/{file.filename}"
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    file.save(path)
    db.lpush(f'_{id}', file.filename)


@app.route('/file/<entree_id>/<filename>', methods=['POST', 'GET', 'DELETE'])
def file(entree_id, filename):
    if request.method == 'POST':
        file = request.files['file']
        save_file(file, entree_id)
        return make_response('File uploaded', 200)
    if request.method == 'DELETE':
        db.lrem(f'_{entree_id}', 1, filename)
        return make_response('File deleted', 200)
    if request.method == 'GET':
        return send_file(f'files/{entree_id}/{filename}', mimetype="Content-Type: application/pdf",
                         as_attachment=True, attachment_filename=filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
