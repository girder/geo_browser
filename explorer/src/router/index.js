import Vue from 'vue';
import Router from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import DefaultItemView from '@/views/DefaultItemView.vue';

Vue.use(Router);
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: MainPage,
    },
    {
      path: '/item/:id',
      name: 'Item',
      component: DefaultItemView,
    },
  ],
});
