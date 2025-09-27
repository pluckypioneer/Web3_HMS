<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>Web3 医院管理系统</h1>
        <p>创建您的账号</p>
      </div>
      
      <el-form 
        :model="registerForm" 
        :rules="registerRules" 
        ref="registerFormRef"
        class="register-form"
      >
        <el-form-item label="钱包地址" prop="blockchain_addr">
          <div class="wallet-connect">
            <el-input 
              v-model="registerForm.blockchain_addr" 
              placeholder="请输入钱包地址或连接钱包"
              readonly
            >
              <template #append>
                <el-button v-if="!account" @click="connectWallet">
                  {{ connecting ? '连接中...' : '连接钱包' }}
                </el-button>
                <el-button v-else @click="disconnectWallet">
                  {{ formatAddress(account) }}
                </el-button>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input 
            v-model="registerForm.name" 
            placeholder="请输入姓名"
          ></el-input>
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-select v-model="registerForm.gender" placeholder="请选择性别" style="width: 100%">
            <el-option label="男" value="M" />
            <el-option label="女" value="F" />
          </el-select>
        </el-form-item>

        <el-form-item label="出生日期" prop="birth_date">
          <el-date-picker
            v-model="registerForm.birth_date"
            type="date"
            placeholder="请选择出生日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="registerForm.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="患者" value="patient" />
            <el-option label="医生/护士" value="doctor" />
          </el-select>
        </el-form-item>

        <el-form-item label="身份证号" prop="id_card">
          <el-input 
            v-model="registerForm.id_card" 
            placeholder="请输入身份证号"
          ></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input 
            v-model="registerForm.phone" 
            placeholder="请输入联系电话"
          ></el-input>
        </el-form-item>

        <el-form-item label="医保卡号" prop="insurance_number">
          <el-input 
            v-model="registerForm.insurance_number" 
            placeholder="请输入医保卡号"
          ></el-input>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="registerForm.email" 
            placeholder="请输入邮箱"
          ></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请确认密码"
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="register-button" 
            @click="handleRegister"
            :loading="loading"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-link">
        已有账号？<el-button type="text" @click="goToLogin">立即登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, FormInstance } from 'element-plus'
import api from '@/utils/api'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const registerFormRef = ref<FormInstance>()
const connecting = ref(false)

// Web3 相关状态
const account = ref<string | null>(null)
const ethereum: any = (window as any).ethereum

// 注册表单
const registerForm = reactive({
  blockchain_addr: '',
  name: '',
  gender: '',
  birth_date: '',
  role: 'patient',
  id_card: '',
  phone: '',
  insurance_number: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const registerRules = computed(() => ({
  blockchain_addr: [
    { required: true, message: '请连接钱包或输入钱包地址', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  birth_date: [
    { required: true, message: '请选择出生日期', trigger: 'change' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  insurance_number: [
    { required: true, message: '请输入医保卡号', trigger: 'blur' }
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

// 格式化钱包地址显示
const formatAddress = (address: string) => {
  if (!address) return ''
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`
}

// 连接钱包
const connectWallet = async () => {
  if (!ethereum) {
    ElMessage.error('请安装 MetaMask 或其他兼容的钱包插件')
    return
  }

  try {
    connecting.value = true
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' })
    account.value = accounts[0]
    registerForm.blockchain_addr = accounts[0]
    ElMessage.success('钱包连接成功')
  } catch (error) {
    ElMessage.error('连接钱包失败')
    console.error('Wallet connection error:', error)
  } finally {
    connecting.value = false
  }
}

// 断开钱包连接
const disconnectWallet = () => {
  account.value = null
  registerForm.blockchain_addr = ''
}

// 页面跳转
const goToLogin = () => {
  router.push('/login')
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // 准备注册数据
    const registerData: any = {
      email: registerForm.email,
      password: registerForm.password,
      role: registerForm.role,
      blockchain_addr: registerForm.blockchain_addr
    }
    
    // 根据角色设置对应的数据模型
    if (registerForm.role === 'patient') {
      registerData.patient_data = {
        name: registerForm.name,
        gender: registerForm.gender,
        birth_date: registerForm.birth_date,
        id_card: registerForm.id_card,
        phone: registerForm.phone,
        insurance_number: registerForm.insurance_number
      }
    } else if (registerForm.role === 'doctor') {
      registerData.doctor_data = {
        name: registerForm.name,
        gender: registerForm.gender,
        birth_date: registerForm.birth_date,
        id_card: registerForm.id_card,
        phone: registerForm.phone
      }
    }
    
    // 调用注册API
    const response = await api.post('/auth/register', registerData)
    
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

// 页面加载时检查是否已安装钱包
onMounted(() => {
  if (ethereum) {
    ethereum.request({ method: 'eth_accounts' }).then((accounts: string[]) => {
      if (accounts.length > 0) {
        account.value = accounts[0]
        registerForm.blockchain_addr = accounts[0]
      }
    })
  }
})
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  width: 500px;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  color: #303133;
  margin-bottom: 10px;
}

.register-header p {
  color: #909399;
  font-size: 14px;
}

.register-form {
  width: 100%;
}

.register-form :deep(.el-form-item__label) {
  font-weight: 500;
}

.register-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.wallet-connect :deep(.el-input-group__append) {
  background-color: #f5f7fa;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #909399;
  font-size: 14px;
}
</style>