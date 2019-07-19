import Vue from 'vue';
import Router from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import QueryBuilder from '@/views/QueryBuilder.vue';
import DefaultItemView from '@/views/DefaultItemView.vue';

Vue.use(Router);
export default new Router({
  routes: [
    {
      path: '/query/',
      name: 'Query Builder',
      component: QueryBuilder,
    },
    {
      path: '/item/:id',
      name: 'Item View',
      component: DefaultItemView,
    },
    {
      path: '/',
      name: 'Main Page',
      component: MainPage,
    },
  ],
});
