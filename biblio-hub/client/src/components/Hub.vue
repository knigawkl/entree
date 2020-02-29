<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"><br>
        <alert :message="message" v-if="showMessage"/>

        <button type="button"
                class="btn btn-secondary btn-sm"
                v-b-modal.book-modal>Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 40%">Title</th>
              <th scope="col" style="width: 20%">PDF File</th>
              <th scope="col" style="width: 15%">Author</th>
              <th scope="col" style="width: 5%">Year</th>
              <th style="width: 20%"/>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>
                <div v-for="(file, index) in book.files" :key="index">
                  <b-link @click="downloadFile(book.id, file)">{{file}}</b-link>
                  <img src="../assets/trash.png"
                       width="10%"
                       v-on:click="deleteFile(book.id, file)"
                       data-cy="trash">
                  <br>
                </div>
              </td>
              <td>{{ book.author }}</td>
              <td>{{ book.year }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button"
                          class="btn btn-light btn-sm"
                          v-b-modal.book-update-modal
                          @click="editBook(book)">
                    Add pdf
                  </button>
                  <button type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteBook(book)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addBookModal"
             id="book-modal"
             title="Add a new book"
             hide-footer>
      <b-form @submit="onSubmitAdd" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.author"
                          required
                          placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-group"
                      label="Year:"
                      label-for="form-year-input">
          <b-form-input id="form-year-input"
                          type="text"
                          v-model="addBookForm.year"
                          placeholder="Enter year">
          </b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-file
            accept=".pdf"
            v-model="addBookForm.file"
            :state=null
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."
          />
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editBookModal"
             id="book-update-modal"
             title="Add PDF file"
             hide-footer>
      <b-form @submit="onSubmitAddFile" @reset="onResetAddFile" class="w-100">
        <b-form-group id="form-file-group">
          <b-form-file
            accept=".pdf"
            id="form-file-input"
            v-model="updateForm.file"
            :state=null
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."
          />
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import { saveAs } from 'file-saver';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      books: [],
      addBookForm: {
        id: '',
        title: '',
        author: '',
        year: '',
        file: null,
      },
      updateForm: {
        file: null,
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    deleteFile(bookId, filename) {
      const token = localStorage.getItem('access_token');
      axios.delete(`http://localhost:5000/file/${bookId}/${filename}`, {
        headers: { Authorization: `${token}` },
      })
        .then(() => {
          this.getBooks();
          this.message = 'File deleted!';
          this.showMessage = true;
        })
        .catch(() => {
          this.message = 'Deletion failed';
          this.showMessage = true;
        });
    },
    submitFile(file, bookId) {
      const formData = new FormData();
      formData.append('file', file);
      const token = localStorage.getItem('access_token');
      axios.post(`http://localhost:5000/file/${bookId}/new`, formData,
        { headers: { 'Content-Type': 'multipart/form-data', Authorization: `${token}` } })
        .then(() => {
          this.message = 'File added!';
          this.showMessage = true;
        })
        .catch(() => {
          this.message = 'File upload error!';
          this.showMessage = true;
        });
    },
    downloadFile(bookId, filename) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://localhost:5000/file/${bookId}/${filename}`, {
        responseType: 'arraybuffer',
        headers: { 'Content-Type': 'application/pdf', Authorization: `${token}` },
      })
        .then((response) => {
          const blob = new Blob([response.data], {
            type: 'application/pdf',
          });
          saveAs(blob, filename);
        })
        .catch(() => {
          this.message = 'Download failed';
          this.showMessage = true;
        });
    },
    getBooks() {
      const path = 'http://localhost:5000/hub/';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addFile(payload, bookID) {
      const path = `http://localhost:5000/hub/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'File added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onSubmitAddFile(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        id: this.updateForm.id,
        file: this.updateForm.file.name,
      };
      this.submitFile(this.updateForm.file, payload.id);
      this.addFile(payload, this.updateForm.id);
    },
    onResetAddFile(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks();
    },
    editBook(book) {
      this.updateForm = book;
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/hub/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.year = '';
      this.addBookForm.file = '';
      this.updateForm.id = '';
      this.updateForm.title = '';
      this.updateForm.author = '';
      this.updateForm.year = '';
      this.updateForm.file = '';
    },
    addBook(payload) {
      const path = 'http://localhost:5000/hub/';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    onSubmitAdd(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        id: Math.random().toString(36).substring(2, 15),
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        year: this.addBookForm.year,
      };
      this.submitFile(this.addBookForm.file, payload.id);
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
