import Vue from "vue";
import VueRouter from "vue-router";
import main from '@/views/main'
import search from '@/views/search'


Vue.use(VueRouter);

const routes = [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
      path: '/search',
      name: 'search',
      component: search
    },
    {
      path: '*',
      name: 'error',
      component: main
    }
  
    
];

const router = new VueRouter({
  // mode: 'history',
  routes
});
export default router;