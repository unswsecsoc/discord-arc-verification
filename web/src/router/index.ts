import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Home from '../views/Home.vue';
import About from '../views/About.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: About,
  },
  {
    path: '/verifications/:token',
    name: 'Verification',
    component: () => import(/* webpackChunkName: "verification" */ '@/views/Verification.vue'),
  },
  {
    path: '/verify_success',
    name: 'Verification Success',
    component: () => import(/* webpackChunkName: "verification" */ '@/views/VerifySuccess.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
