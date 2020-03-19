<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 mt-5 mx-auto">
        <alert :message="message" v-if="showMessage"></alert>
        <form id="reg_form" v-on:submit.prevent="register">
          <div class="form-group">
            <label for="reg_email">Email Address</label>
            <input id="reg_email" type="email" v-model="reg_email"
                   class="form-control" name="reg_email"
                   placeholder="Enter email" required>
          </div>
          <div class="form-group">
            <label id="login_label" for="reg_login">Login</label>
            <div id="msg"></div>
            <input id="reg_login" type="text" v-model="reg_login" class="form-control"
                   name="reg_login"
                   placeholder="Enter login" required>
          </div>
          <div class="form-group">
            <label for="reg_password">Password</label>
            <input id="reg_password" type="password" v-model="reg_password" class="form-control"
                   name="reg_password" placeholder="Enter Password" required>
          </div>
          <button type="submit" class="btn btn-sm btn-dark btn-block">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script type="text/javascript">

import axios from 'axios';
import Alert from './Alert.vue';

window.onkeyup = () => {
  if (document.getElementById('reg_form') != null) {
    document.getElementById('reg_form').onkeypress = (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
      }
    };

    document.getElementById('reg_form').addEventListener('submit', (e) => {
      e.preventDefault();
    });

    document.getElementById('reg_login').addEventListener('change', (e) => {
      const input = e.target;
      const path = 'http://localhost:5000/register/';
      axios.post(path, {
        login: input.value,
        password: 'mock',
        email: 'mock',
      }).then((response) => {
        if (response.data === 'Username available') {
          document.getElementById('login_label').innerHTML = 'Login available!';
          document.getElementById('login_label').style.color = 'green';
        } else {
          document.getElementById('login_label').innerHTML = 'Login unavailable!';
          document.getElementById('login_label').style.color = 'red';
        }
      });
    });
  }
};

export default {
  data() {
    return {
      reg_email: '',
      reg_login: '',
      reg_password: '',
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    register() {
      const path = 'http://localhost:5000/register/';

      axios.put(path, {
        email: this.reg_email,
        login: this.reg_login,
        password: this.reg_password,
      }).then((resp) => {
        if (resp.data === 'Username available') {
          this.$router.push({ name: 'Login' });
        } else {
          this.message = 'Invalid data!';
          this.showMessage = true;
        }
      });
    },
  },
};

</script>
