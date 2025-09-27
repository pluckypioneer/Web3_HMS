<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Web3 医院管理系统</h1>
        <p v-if="isLogin">请使用您的账号登录</p>
        <p v-else>创建您的账号</p>
      </div>
      
      <!-- 登录表单 -->
      <el-form 
        v-if="isLogin"
        :model="loginForm" 
        :rules="loginRules" 
        ref="loginFormRef"
        class="login-form"
      >
        <el-form-item prop="email">
          <el-input 
            v-model="loginForm.email" 
            placeholder="请输入邮箱" 
            prefix-icon="User"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            @click="handleLogin"
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 注册表单 -->
      <el-form 
        v-else
        :model="registerForm" 
        :rules="registerRules" 
        ref="registerFormRef"
        class="login-form"
      >
        <el-form-item prop="name">
          <el-input 
            v-model="registerForm.name" 
            placeholder="请输入姓名" 
            prefix-icon="User"
          ></el-input>
        </el-form-item>

        <el-form-item prop="email">
          <el-input 
            v-model="registerForm.email" 
            placeholder="请输入邮箱" 
            prefix-icon="Message"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请确认密码" 
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            @click="handleRegister"
            :loading="loading"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 切换登录/注册 -->
      <div class="switch-form">
        <span v-if="isLogin">
          还没有账号？<el-button type="text" @click="switchToRegister">立即注册</el-button>
        </span>
        <span v-else>
          已有账号？<el-button type="text" @click="switchToLogin">立即登录</el-button>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, FormInstance } from 'element-plus'
import api from '@/utils/api'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const isLogin = ref(true)
const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loginRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const registerRules = computed(() => ({
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { 
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}))

const switchToRegister = () => {
  isLogin.value = false
}

const switchToLogin = () => {
  isLogin.value = true
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    // 调用登录API
    const response = await api.post('/auth/login', {
      email: loginForm.email,
      password: loginForm.password
    })
    
    // 保存令牌和用户信息
    const { token: newToken, user: userData } = response as any
    
    userStore.token = newToken
    userStore.user = userData
    localStorage.setItem('token', newToken)
    
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || '登录失败')
    } else if (error.name === 'ValidationError') {
      // 表单验证失败，无需额外处理
    } else {
      ElMessage.error('登录过程出错，请重试')
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // 调用注册API
    const response = await api.post('/auth/register', {
      name: registerForm.name,
      email: registerForm.email,
      password: registerForm.password
    })
    
    // 注册成功后自动登录
    const { token: newToken, user: userData } = response as any
    
    userStore.token = newToken
    userStore.user = userData
    localStorage.setItem('token', newToken)
    
    ElMessage.success('注册成功')
    router.push('/dashboard')
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || '注册失败')
    } else {
      ElMessage.error('注册过程出错，请重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #303133;
  margin-bottom: 10px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  width: 100%;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.switch-form {
  text-align: center;
  margin-top: 20px;
  color: #909399;
  font-size: 14px;
}
</style>