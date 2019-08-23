<template class="nav-drawer-container">
  <v-navigation-drawer
    :mini-variant="navDrawerMini"
    app
    hide-overlay
  >
    <v-icon
      large
      @click="toggleNavDrawer"
    >
      {{ navDrawerMini ? 'mdi-chevron-right' : 'mdi-chevron-left' }}
    </v-icon>
    <template v-if="apiAccessed && !navDrawerMini">
      <v-list>
        <v-list-tile v-if="loggedIn">
          <v-list-tile-avatar>
            <v-icon color="blue">
              mdi-account-circle
            </v-icon>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>
              {{ currentUserFirstName }}
            </v-list-tile-title>
          </v-list-tile-content>
          <v-list-action>
            <v-btn
              depressed
              icon
              @click="logout"
            >
              <v-icon color="error">
                mdi-logout
              </v-icon>
            </v-btn>
          </v-list-action>
        </v-list-tile>
        <v-list-tile
          v-else
          class="nav-bar-list-tile"
        >
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
        </v-list-tile>
        <v-list-tile
          v-for="route in navRoutes"
          :key="route.name"
          @click="navigateToRoute(route)"
        >
          <v-list-tile-avatar>
            <v-icon>{{ route.icon }}</v-icon>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>
              {{ route.name }}
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </template>
    <template v-else-if="navDrawerMini">
      <v-flex
        v-for="route in navRoutes"
        :key="route.name"
        @click="navigateToRoute(route)"
      >
        <v-btn icon>
          <v-icon>{{ route.icon }}</v-icon>
        </v-btn>
      </v-flex>
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
    navRoutes() {
      return this.$router.options.routes.slice(0, 2);
    },
  },
  watch: {
    login() {
      this.loginOpen = false;
      this.registerOpen = false;
    },
  },
  methods: {
    navigateToRoute(route) {
      this.$router.push(route);
      this.$store.commit('SET_NAV_DRAWER', true);
    },
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
