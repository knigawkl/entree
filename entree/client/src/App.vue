<template>
  <div id="app">
    <my_nav></my_nav>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    my_nav: Navbar,
  },
};
</script>
