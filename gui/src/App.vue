<template>
  <v-app>
    <v-content>
      <template class="app-container">
        <NavDrawer />
        <router-view />
      </template>
    </v-content>
  </v-app>
</template>

<script>

import Vue from 'vue';
import { mapState } from 'vuex';
import VueStatic from 'vue-static';
import store from '@/store';
import router from '@/router';
import NavDrawer from '@/components/NavigationDrawer.vue';

Vue.use(VueStatic);

export default {
  name: 'App',
  store,
  router,
  components: {
    NavDrawer,
  },
  inject: ['girderRest'],
  data() {
    return {};
  },
  computed: {
    ...mapState({
      currentUserFirstName: state => state.user.firstName,
      loggedIn: state => state.user.loggedIn,
      login: state => state.user.login,
      apiAccessed: state => state.api.accessed,
      navDrawerMini: state => state.app.navDrawerMini,
    }),
    girderRestUser() {
      return this.girderRest.user;
    },
  },
  watch: {
    girderRestUser(user) {
      this.$store.commit('SET_USER_INFO', user);
    },
  },
  async mounted() {
    const user = await this.girderRest.fetchUser();
    if (user) this.$store.commit('SET_USER_INFO', user);
    this.$store.commit('SET_API_ACCESSED');
  },
  methods: {
    toggleNavDrawer() {
      this.$store.commit('TOGGLE_NAV_DRAWER');
    },
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
