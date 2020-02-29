<template>
<nav class="navbar navbar-expand-md navbar-dark bg-dark">
  <div class="navbar-collapse collapse w-100 order-1 order-md-0 dual-collapse2">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <img src="../assets/logo.png" width="50%" alt="logo">
      </li>
    </ul>
  </div>
  <div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
    <ul class="navbar-nav ml-auto">
      <li v-if="!loggedIn" class="nav-item">
        <router-link class="nav-link" :to="{ name: 'Login' }">Sign in</router-link>
      </li>
      <li v-if="!loggedIn" class="nav-item">
        <router-link class="nav-link" :to="{ name: 'Register' }">Sign up</router-link>
      </li>
      <li v-if="loggedIn" class="nav-item">
        <router-link class="nav-link" :to="{ name: 'Logout' }">Log out</router-link>
      </li>
    </ul>
  </div>
</nav>
</template>

<script>
export default {
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn;
    },
  },
};
</script>
