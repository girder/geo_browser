<template class="nav-drawer-container">
  <v-navigation-drawer
    :mini-variant="navDrawerMini"
    app
    hide-overlay
  >
    <v-icon
      large
      color="blue"
      @click="toggleNavDrawer"
    >
      mdi-account-circle
    </v-icon>
    <template v-if="apiAccessed && !navDrawerMini">
      <v-list v-if="!loggedIn">
        <v-list-tile class="nav-bar-list-tile">
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
        </v-list-tile>
        <v-list-tile class="nav-bar-list-tile">
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
        </v-list-tile>
      </v-list>
      <v-list v-else>
        <h1> {{ currentUserFirstName }} </h1>
        <v-btn
          depressed
          color="error"
          @click="logout"
        >
          Logout
        </v-btn>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script>

import { mapState } from 'vuex';
import GirderLogin from '@girder/components/src/components/Authentication/Login.vue';
import GirderRegister from '@girder/components/src/components/Authentication/Register.vue';

export default {
  name: 'NavigationDrawer',
  components: {
    GirderLogin,
    GirderRegister,
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
      login: state => state.user.login,
      apiAccessed: state => state.api.accessed,
      navDrawerMini: state => state.app.navDrawerMini,
    }),
  },
  watch: {
    login() {
      this.loginOpen = false;
      this.registerOpen = false;
    },
  },
  methods: {
    toggleNavDrawer() {
      this.$store.commit('TOGGLE_NAV_DRAWER');
    },
    async logout() {
      await this.girderRest.logout();
      this.$store.commit('USER_LOGOUT');
    },
  },
};
</script>

<style>
.nav-bar-list-tile .v-list__tile{
  justify-content: center;
}
</style>
