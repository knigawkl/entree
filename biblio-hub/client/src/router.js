import Vue from 'vue';
import Router from 'vue-router';
import Register from './components/Register.vue';
import Login from './components/Login.vue';
import Logout from './components/Logout.vue';
import Hub from './components/Hub.vue';

Vue.use(Router);

export default new Router({
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresVisitor: true,
      },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        requiresVisitor: true,
      },
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout,
    },
    {
      path: '/hub',
      name: 'Hub',
      component: Hub,
      meta: {
        requiresAuth: true,
      },
    },
  ],
});
