import Vue from 'vue';
import 'vuetify/dist/vuetify.min.css';
import App from '@/App.vue';
import { GirderProvider } from '@/plugins';

Vue.config.productionTip = false;

new Vue({
  provide: GirderProvider,
  render: h => h(App),
}).$mount('#app');
