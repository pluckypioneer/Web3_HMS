import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/patients',
      name: 'Patients',
      component: () => import('@/views/Patients.vue'),
      meta: { requiresAuth: true, role: ['doctor', 'admin'] }
    },
    {
      path: '/patients/:id',
      name: 'PatientDetail',
      component: () => import('@/views/PatientDetail.vue'),
      meta: { requiresAuth: true, role: ['doctor', 'admin'] }
    },
    {
      path: '/appointments',
      name: 'Appointments',
      component: () => import('@/views/Appointments.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/medical-records',
      name: 'MedicalRecords',
      component: () => import('@/views/MedicalRecords.vue'),
      meta: { requiresAuth: true, role: ['doctor', 'admin'] }
    },
    {
      path: '/blockchain',
      name: 'Blockchain',
      component: () => import('@/views/Blockchain.vue'),
      meta: { requiresAuth: true, role: ['admin'] }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.role && !userStore.hasRole(to.meta.role as string[])) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
