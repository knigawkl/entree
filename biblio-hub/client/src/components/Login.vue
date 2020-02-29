<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 mt-5 mx-auto">
        <alert :message="message" v-if="showMessage"></alert>
        <form id="login_form" v-on:submit.prevent="signin">
          <div class="form-group">
            <label id="login_label" for="login">Login</label>
            <div id="msg"></div>
            <input id="login" type="text" v-model="login" class="form-control" name="login"
                   placeholder="Enter login" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input id="password" type="password" v-model="password" class="form-control"
                   name="password" placeholder="Enter Password" required>
          </div>
          <button type="submit" class="btn btn-sm btn-dark btn-block">Sign in</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import Alert from './Alert.vue';

export default {
  name: 'signin',
  data() {
    return {
      login: '',
      password: '',
      serverError: '',
      successMessage: '',
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    signin() {
      this.$store.dispatch('retrieveToken', {
        login: this.login,
        password: this.password,
      })
        .then((response) => {
          this.$router.push({ name: 'Hub' });
          this.successMessage = response.data;
        })
        .catch((error) => {
          this.message = 'Invalid data!';
          this.showMessage = true;
          this.serverError = error.response.data;
          this.password = '';
          this.successMessage = '';
        });
    },
  },
};
</script>
