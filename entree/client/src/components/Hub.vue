<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"><br>
        <alert :message="message" v-if="showMessage"/>

        <button type="button"
                class="btn btn-secondary btn-sm"
                v-b-modal.entree-modal>Add Entree</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 40%">Name</th>
              <th scope="col" style="width: 20%">PDF File</th>
              <th scope="col" style="width: 15%">Date</th>
              <th style="width: 20%"/>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entree, index) in entrees" :key="index">
              <td>{{ entree.name }}</td>
              <td>
                <div v-for="(file, index) in entree.files" :key="index">
                  <b-link @click="downloadFile(entree.id, file)">{{file}}</b-link>
                  <img src="../assets/trash.png"
                       width="10%"
                       v-on:click="deleteFile(entree.id, file)"
                       data-cy="trash">
                  <br>
                </div>
              </td>
              <td>{{ entree.date }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button"
                          class="btn btn-light btn-sm"
                          v-b-modal.entree-update-modal
                          @click="editEntree(entree)">
                    Add pdf
                  </button>
                  <button type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteEntree(entree)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addEntreeModal"
             id="entree-modal"
             title="Add a new entree"
             hide-footer>
      <b-form @submit="onSubmitAdd" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                    label="Name"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addEntreeForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Date"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                          type="date"
                          v-model="addEntreeForm.date"
                          required
                          placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group label="File">
          <b-form-file
            accept=".pdf"
            v-model="addEntreeForm.file"
            :state=null
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."
          />
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editEntreeModal"
             id="entree-update-modal"
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
      entrees: [],
      addEntreeForm: {
        id: '',
        name: '',
        date: '',
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
    deleteFile(entreeId, filename) {
      const token = localStorage.getItem('access_token');
      axios.delete(`http://localhost:5000/file/${entreeId}/${filename}`, {
        headers: { Authorization: `${token}` },
      })
        .then(() => {
          this.getEntrees();
          this.message = 'File deleted!';
          this.showMessage = true;
        })
        .catch(() => {
          this.message = 'Deletion failed';
          this.showMessage = true;
        });
    },
    submitFile(file, entreeId) {
      const formData = new FormData();
      formData.append('file', file);
      const token = localStorage.getItem('access_token');
      axios.post(`http://localhost:5000/file/${entreeId}/new`, formData,
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
    downloadFile(entreeId, filename) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://localhost:5000/file/${entreeId}/${filename}`, {
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
    getEntrees() {
      const path = 'http://localhost:5000/hub/';
      axios.get(path)
        .then((res) => {
          this.entrees = res.data.entrees;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addFile(payload, entreeID) {
      const path = `http://localhost:5000/hub/${entreeID}`;
      axios.put(path, payload)
        .then(() => {
          this.getEntrees();
          this.message = 'File added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getEntrees();
        });
    },
    onSubmitAddFile(evt) {
      evt.preventDefault();
      this.$refs.editEntreeModal.hide();
      const payload = {
        id: this.updateForm.id,
        file: this.updateForm.file.name,
      };
      this.submitFile(this.updateForm.file, payload.id);
      this.addFile(payload, this.updateForm.id);
    },
    onResetAddFile(evt) {
      evt.preventDefault();
      this.$refs.editEntreeModal.hide();
      this.initForm();
      this.getEntrees();
    },
    editEntree(entree) {
      this.updateForm = entree;
    },
    removeEntree(entreeID) {
      const path = `http://localhost:5000/hub/${entreeID}`;
      axios.delete(path)
        .then(() => {
          this.getEntrees();
          this.message = 'Entree removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getEntrees();
        });
    },
    onDeleteEntree(entree) {
      this.removeEntree(entree.id);
    },
    initForm() {
      this.addEntreeForm.name = '';
      this.addEntreeForm.date = '';
      this.addEntreeForm.file = '';
      this.updateForm.id = '';
      this.updateForm.name = '';
      this.updateForm.date = '';
      this.updateForm.file = '';
    },
    addEntree(payload) {
      const path = 'http://localhost:5000/hub/';
      axios.post(path, payload)
        .then((response) => {
          const id = response;
          this.getEntrees();
          this.message = 'Entree added!';
          this.showMessage = true;
          return id;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getEntrees();
        });
    },
    onSubmitAdd(evt) {
      evt.preventDefault();
      this.$refs.addEntreeModal.hide();
      const payload = {
        name: this.addEntreeForm.name,
        date: this.addEntreeForm.date,
      };
      this.addEntree(payload);
      // this.submitFile(this.addEntreeForm.file);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addEntreeModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getEntrees();
  },
};
</script>
