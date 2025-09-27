import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

export interface User {
  id: string
  name: string
  email: string
  role: string
  blockchain_addr?: string
  dept_name?: string
  title?: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  
  const hasRole = (roles: string[]) => {
    if (!user.value) return false
    return roles.includes(user.value.role)
  }
  
  const setAuth = (newToken: string, userData: User) => {
    token.value = newToken
    user.value = userData
    localStorage.setItem('token', newToken)
  }

  const login = async (email: string, password: string) => {
    loading.value = true
    try {
      const response = await api.post('/auth/login', { email, password })
      const { token: newToken, user: userData } = response as any
      
      token.value = newToken
      user.value = userData
      localStorage.setItem('token', newToken)
      
      ElMessage.success('登录成功')
      return true
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || '登录失败')
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    ElMessage.success('已退出登录')
  }

  const initialize = async () => {
    if (token.value) {
      try {
        const response = await api.get('/auth/me')
        user.value = response as any
      } catch (error) {
        logout()
      }
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    loading.value = true
    try {
      const response = await api.put('/auth/profile', data)
      user.value = response.data
      ElMessage.success('个人信息更新成功')
      return true
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || '更新失败')
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    hasRole,
    setAuth,
    login,
    logout,
    initialize,
    updateProfile
  }
})