import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);
const store = new Vuex.Store({
  state: {
    user: {
      loggedIn: false,
    },
    api: {
      accessed: false,
    },
    app: {
      navDrawerMini: true,
    },
  },
  getters: {
    user: state => state.user,
  },
  mutations: {
    /* eslint-disable no-param-reassign */
    SET_USER_INFO(state, payload) {
      state.user = {
        ...payload,
        loggedIn: true,
      };
    },
    SET_API_ACCESSED(state) {
      state.api.accessed = true;
    },
    USER_LOGOUT(state) {
      state.user = {
        loggedIn: false,
      };
    },
    TOGGLE_NAV_DRAWER(state) {
      state.app.navDrawerMini = !state.app.navDrawerMini;
    },
    SET_NAV_DRAWER(state, open = true) {
      state.app.navDrawerMini = open;
    },
    /* eslint-enable no-param-reassign */
  },
  actions: {},
});

export default store;
