<template>
  <div id="main-page">
    <v-toolbar>
      <v-btn
        depressed
        color="error"
        @click="goToItemPage"
      >
        Item Page
      </v-btn>
      <v-spacer />
      <template v-if="apiAccessed">
        <template v-if="!loggedIn">
          <v-dialog
            v-model="loginOpen"
            max-width="30%"
          >
            <template v-slot:activator="{ on }">
              <v-btn
                depressed
                color="secondary"
                v-on="on"
              >
                Login
              </v-btn>
            </template>
            <v-card>
              <GirderLogin />
            </v-card>
          </v-dialog>
          <v-dialog
            v-model="registerOpen"
            max-width="30%"
          >
            <template v-slot:activator="{ on }">
              <v-btn
                depressed
                color="primary"
                v-on="on"
              >
                Register
              </v-btn>
            </template>
            <v-card>
              <GirderRegister />
            </v-card>
          </v-dialog>
        </template>
        <template v-if="loggedIn">
          <h1> {{ currentUserFirstName }} </h1>
          <v-btn
            depressed
            color="error"
            @click="logout"
          >
            Logout
          </v-btn>
        </template>
      </template>
    </v-toolbar>
    <CollectionMap class="collection-map" />
    <v-card>
      <DataBrowser :location.sync="location" />
    </v-card>
  </div>
</template>

<script>

import { mapState } from 'vuex';
import { DataBrowser } from '@girder/components/src/components';
import GirderLogin from '@girder/components/src/components/Authentication/Login.vue';
import GirderRegister from '@girder/components/src/components/Authentication/Register.vue';
import CollectionMap from '@/components/CollectionMap.vue';

export default {
  name: 'MainPage',
  components: {
    CollectionMap,
    GirderLogin,
    GirderRegister,
    DataBrowser,
  },
  data() {
    return {
      loginOpen: false,
      registerOpen: false,
      browserLocation: null,
    };
  },
  inject: ['girderRest'],
  computed: {
    ...mapState({
      currentUserFirstName: state => state.user.firstName,
      loggedIn: state => state.user.loggedIn,
      login: state => state.user.login,
      apiAccessed: state => state.api.accessed,
    }),
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
    login() {
      this.loginOpen = false;
      this.registerOpen = false;
    },
  },
  methods: {
    async logout() {
      await this.girderRest.logout();
      this.$store.commit('USER_LOGOUT');
    },
    goToItemPage() {
      this.$router.push({
        name: 'Item',
        params: {
          id: 'yoooo',
          a: 1,
          b: 2,
        },
      });
    },
  },
};
</script>

<style>
.collection-map {
  margin-left: 3%;
  margin-right: 3%;
  height: 700px;
}
</style>
