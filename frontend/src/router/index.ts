import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '仪表盘' }
  },
  {
    path: '/indicators',
    name: 'Indicators',
    component: () => import('../views/Indicators.vue'),
    meta: { title: '经济指标' }
  },
  {
    path: '/indicators/:code',
    name: 'IndicatorDetail',
    component: () => import('../views/IndicatorDetail.vue'),
    meta: { title: '指标详情' }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('../views/Analysis.vue'),
    meta: { title: '多维分析' }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/Alerts.vue'),
    meta: { title: '预警中心' }
  },
  {
    path: '/decision',
    name: 'Decision',
    component: () => import('../views/Decision.vue'),
    meta: { title: '投资决策' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
