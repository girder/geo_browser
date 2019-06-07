<template>
  <v-app>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>

import Vue from 'vue';
import VueStatic from 'vue-static';
import store from '@/store';
import router from '@/router';

Vue.use(VueStatic);

export default {
  name: 'App',
  store,
  router,
  inject: ['girderRest'],
  computed: {
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
