import datetime
import jwt
import os
import errno
import bcrypt
from flask import Flask, jsonify, request, redirect, url_for, make_response, send_file, send_from_directory
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'customerobsessed'

CORS(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing token'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'})
        return f(*args, **kwargs)

    return decorated


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register/', methods=['POST', 'PUT'])
def register():
    req = request.get_json()
    login = req['login']
    if login and db.hget(login, 'login') == login:
        resp = jsonify('Login unavailable')
        return resp
    else:
        resp = jsonify('Username available')
    if request.method == 'PUT':
        password, email = req['password'], req['email']

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)
        hashed = hashed.decode("utf-8")
        print(hashed)

        db.hset(login, 'login', login)
        db.hset(login, 'password', hashed)
        db.hset(login, 'email', email)
    return resp


@app.route('/login/', methods=['POST'])
def login():
    auth = request.get_json()
    login, password = auth['login'], auth['password']

    if auth and bcrypt.checkpw(password.encode('utf8'), db.hget(login, 'password').encode('utf8')):
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

        id = str(post_data.get('id'))
        db.hset(id, 'id', id)
        db.hset(id, 'title', post_data.get('title'))
        db.hset(id, 'author', post_data.get('author'))
        db.hset(id, 'year', post_data.get('year'))

        db.sadd('books', id)
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = get_books()
    return jsonify(response_object)


def get_books():
    books = []
    db_resp = db.smembers('books')
    for member in db_resp:
        files = db.lrange(f'_{member}', 0, -1)
        book_dict = {'id': member, 'title': db.hget(member, 'title'), 'author': db.hget(member, 'author'),
                     'year': db.hget(member, 'year'), 'files': files}
        books.append(book_dict)
    return books


def remove_book(book_id):
    db_resp = db.smembers('books')
    for member in db_resp:
        if member == book_id:
            db.hdel(member, 'id', 'title', 'author', 'year', 'file')
            db.srem('books', member)
            return True
    return False


@app.route('/hub/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        #post_data = request.get_json()
        id = book_id

        response_object['message'] = 'File added!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def save_file(file, id):
    path = f"files/{id}/{file.filename}"
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    file.save(path)
    db.lpush(f'_{id}', file.filename)


@app.route('/file/<book_id>/<filename>', methods=['POST', 'GET', 'DELETE'])
# @token_required
def file(book_id, filename):
    if request.method == 'POST':
        file = request.files['file']
        save_file(file, book_id)
        return make_response('File uploaded', 200)
    if request.method == 'DELETE':
        db.lrem(f'_{book_id}', 1, filename)
        return make_response('File deleted', 200)
    if request.method == 'GET':
        return send_file(f'files/{book_id}/{filename}', mimetype="Content-Type: application/pdf",
                         as_attachment=True, attachment_filename=filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
