import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);
const store = new Vuex.Store({
  state: {
    user: {
      loggedIn: false,
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
    USER_LOGOUT(state) {
      state.user = {
        loggedIn: false,
      };
    },
    /* eslint-enable no-param-reassign */
  },
  actions: {},
});

export default store;
