<template>
  <v-app>
    <v-content>
      <div id="app">
        <VToolbar>
          <VDialog
            v-model="loginOpen"
            max-width="30%"
          >
            <template v-slot:activator="{ on }">
              <VBtn
                flat
                v-on="on"
              >
                Login
              </VBtn>
            </template>
            <VCard>
              <GirderLogin />
            </VCard>
          </VDialog>
          <VDialog
            v-model="registerOpen"
            max-width="30%"
          >
            <template v-slot:activator="{ on }">
              <VBtn
                flat
                color="primary"
                v-on="on"
              >
                Register
              </VBtn>
            </template>
            <VCard>
              <GirderRegister />
            </VCard>
          </VDialog>
          <VSpacer />
          <template
            v-if="loggedIn"
          >
            <h1> {{ currentUserFirstName }} </h1>
            <VBtn
              depressed
              color="error"
              @click="logout"
            >
              Logout
            </VBtn>
          </template>
        </VToolbar>
        <!-- <GirderAuthentication
          v-if="!this.$store.state.user.loggedIn"
          register
        /> -->
        <CollectionMap class="collection-map" />
        <VCard>
          <DataBrowser :location.sync="location" />
        </VCard>
      </div>
    </v-content>
  </v-app>
</template>

<script>

import Vue from 'vue';
import { mapState } from 'vuex';
import VueStatic from 'vue-static';
import {
  VToolbar,
  VSpacer,
  VBtn,
  VDialog,
  VCard,
} from 'vuetify';
import { DataBrowser } from '@girder/components/src/components';
import GirderLogin from '@girder/components/src/components/Authentication/Login.vue';
import GirderRegister from '@girder/components/src/components/Authentication/Register.vue';
import CollectionMap from './components/CollectionMap.vue';
import store from './store';

Vue.use(VueStatic);

export default {
  name: 'App',
  store,
  components: {
    CollectionMap,
    GirderLogin,
    GirderRegister,
    DataBrowser,
    VToolbar,
    VSpacer,
    VBtn,
    VDialog,
    VCard,
  },
  inject: ['girderRest'],
  data() {
    return {
      loginOpen: false,
      registerOpen: false,
    };
  },
  computed: {
    ...mapState({
      currentUserFirstName: state => state.user.firstName,
      loggedIn: state => state.user.loggedIn,
    }),
    girderRestUser() {
      return this.girderRest.user;
    },
    location: {
      get() {
        if (this.browserLocation) {
          return this.browserLocation;
        }
        return { type: 'collections' };
      },
      set(newVal) {
        this.browserLocation = newVal;
      },
    },
  },
  watch: {
    girderRestUser(user) {
      this.$store.commit('SET_USER_INFO', user);
      this.loginOpen = false;
      this.registerOpen = false;
    },
  },
  async mounted() {
    const user = await this.girderRest.fetchUser();
    if (user) this.$store.commit('SET_USER_INFO', user);
  },
  methods: {
    async logout() {
      await this.girderRest.logout();
      this.$store.commit('USER_LOGOUT');
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

.collection-map {
  margin-left: 3%;
  margin-right: 3%;
  height: 700px;
}
</style>
