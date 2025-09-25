// src/router/index.ts (更新后)
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Layout from '@/views/Layout.vue'

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
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue')
        },
        {
          path: 'patients',
          name: 'Patients',
          component: () => import('@/views/Patients.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'patients/add',
          name: 'AddPatient',
          component: () => import('@/views/AddPatient.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'patients/:id',
          name: 'PatientDetail',
          component: () => import('@/views/PatientDetail.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'patients/:id/edit',
          name: 'EditPatient',
          component: () => import('@/views/EditPatient.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'appointments',
          name: 'Appointments',
          component: () => import('@/views/Appointments.vue')
        },
        {
          path: 'medical-records',
          name: 'MedicalRecords',
          component: () => import('@/views/MedicalRecords.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'prescriptions',
          name: 'Prescriptions',
          component: () => import('@/views/Prescriptions.vue'),
          meta: { role: ['doctor', 'admin'] }
        },
        {
          path: 'inventory',
          name: 'Inventory',
          component: () => import('@/views/Inventory.vue'),
          meta: { role: ['admin'] }
        },
        {
          path: 'blockchain',
          name: 'Blockchain',
          component: () => import('@/views/Blockchain.vue'),
          meta: { role: ['admin'] }
        },
        {
          path: 'statistics',
          name: 'Statistics',
          component: () => import('@/views/Statistics.vue'),
          meta: { role: ['admin'] }
        },
        {
          path: 'profile',
          name: 'Profile',
          component: () => import('@/views/Profile.vue')
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } 
  // 检查角色权限
  else if (to.meta.role && !userStore.hasRole(to.meta.role as string[])) {
    next('/dashboard')
    ElMessage.warning('您没有权限访问此页面')
  } else {
    next()
  }
})

export default router