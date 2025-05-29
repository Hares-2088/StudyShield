import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuth } from '@/api/authService';
import StudySession from '@/views/StudySession.vue';
import ActiveStudySession from '@/views/ActiveStudySession.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shop',
    name: 'Shop',
    component: () => import('@/views/Shop.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/challenges',
    name: 'Challenges',
    component: () => import('@/views/Challenges.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/start-session',
    name: 'StartSession',
    component: StudySession,
    meta: { requiresAuth: true }
  },
  {
    path: '/active-session/:sessionId',
    name: 'ActiveStudySession',
    component: ActiveStudySession,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to) => {
  const token = localStorage.getItem('access_token')
  const { checkAuth } = useAuth()

  // Public pages are always allowed
  if (to.meta.requiresAuth === false) {
    return true
  }

  // If no token, skip the network call and go to /login immediately
  if (!token) {
    return { name: 'Login' }
  }

  // Otherwise (we have a token) call checkAuth() once
  const isAuth = await checkAuth()
  console.log('guard:', to.fullPath, 'authenticated?', isAuth)

  if (!isAuth) {
    return { name: 'Login' }
  }

  // If you’re trying to visit /login or /register when already authed,
  // send them to the dashboard
  if ((to.name === 'Login' || to.name === 'Register') && isAuth) {
    return { name: 'Dashboard' }
  }

  // All good
  return true
})

export default router