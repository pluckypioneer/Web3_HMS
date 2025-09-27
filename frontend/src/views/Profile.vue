<template>
  <div class="profile-container">
    <!-- 页面头部 -->
    <div class="profile-header">
      <div class="header-content">
        <div class="user-avatar">
          <el-avatar :size="80" :src="userAvatar">
            <el-icon><User /></el-icon>
          </el-avatar>
        </div>
        <div class="user-info">
          <h1 class="user-name">{{ (userStore.user?.username || userStore.user?.name) || '用户' }}</h1>
          <p class="user-role">{{ getRoleDisplay(userStore.user?.role) }}</p>
          <p class="user-email">{{ userStore.user?.email }}</p>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="profile-content">
      <el-row :gutter="24">
        <!-- 左侧：个人信息编辑 -->
        <el-col :xs="24" :lg="16">
          <el-card shadow="hover" class="info-card">
            <template #header>
              <div class="card-header">
                <h3><el-icon><User /></el-icon> 个人信息</h3>
                <el-button 
                  type="primary" 
                  :icon="Edit" 
                  @click="toggleEdit"
                  :disabled="loading"
                >
                  {{ isEditing ? '取消编辑' : '编辑资料' }}
                </el-button>
              </div>
            </template>

            <el-form 
              ref="profileFormRef"
              :model="profileForm" 
              :rules="profileRules"
              label-width="100px"
              class="profile-form"
              :disabled="!isEditing"
            >
              <el-form-item label="用户名" prop="username">
                <el-input 
                  v-model="profileForm.username" 
                  placeholder="请输入用户名"
                  :prefix-icon="User"
                />
              </el-form-item>

              <el-form-item label="邮箱" prop="email">
                <el-input 
                  v-model="profileForm.email" 
                  placeholder="请输入邮箱"
                  :prefix-icon="Message"
                />
              </el-form-item>

              <el-form-item label="角色">
                <el-input 
                  :value="getRoleDisplay(profileForm.role)" 
                  disabled
                  :prefix-icon="Avatar"
                />
              </el-form-item>

              <el-form-item label="区块链地址" prop="blockchain_addr">
                <el-input 
                  v-model="profileForm.blockchain_addr" 
                  placeholder="请输入区块链钱包地址"
                  :prefix-icon="Link"
                >
                  <template #append v-if="profileForm.blockchain_addr">
                    <el-button 
                      @click="copyToClipboard(profileForm.blockchain_addr)"
                      :icon="CopyDocument"
                    />
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item v-if="isEditing">
                <el-button 
                  type="primary" 
                  @click="handleSave"
                  :loading="loading"
                  size="large"
                >
                  <el-icon><Check /></el-icon>
                  保存更改
                </el-button>
                <el-button 
                  @click="handleCancel"
                  :disabled="loading"
                  size="large"
                >
                  <el-icon><Close /></el-icon>
                  取消
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 密码修改区域 -->
          <el-card shadow="hover" class="password-card">
            <template #header>
              <div class="card-header">
                <h3><el-icon><Lock /></el-icon> 密码安全</h3>
              </div>
            </template>

            <el-form 
              ref="passwordFormRef"
              :model="passwordForm" 
              :rules="passwordRules"
              label-width="100px"
              class="password-form"
            >
              <el-form-item label="当前密码" prop="currentPassword">
                <el-input 
                  v-model="passwordForm.currentPassword" 
                  type="password"
                  placeholder="请输入当前密码"
                  show-password
                  :prefix-icon="Lock"
                />
              </el-form-item>

              <el-form-item label="新密码" prop="newPassword">
                <el-input 
                  v-model="passwordForm.newPassword" 
                  type="password"
                  placeholder="请输入新密码"
                  show-password
                  :prefix-icon="Lock"
                />
              </el-form-item>

              <el-form-item label="确认密码" prop="confirmPassword">
                <el-input 
                  v-model="passwordForm.confirmPassword" 
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                  :prefix-icon="Lock"
                />
              </el-form-item>

              <el-form-item>
                <el-button 
                  type="warning" 
                  @click="handleChangePassword"
                  :loading="passwordLoading"
                  size="large"
                >
                  <el-icon><Key /></el-icon>
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- 右侧：账户统计和活动 -->
        <el-col :xs="24" :lg="8">
          <!-- 账户统计 -->
          <el-card shadow="hover" class="stats-card">
            <template #header>
              <h3><el-icon><DataBoard /></el-icon> 账户统计</h3>
            </template>
            
            <div class="stats-content">
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-label">注册时间</span>
                  <span class="stat-value">{{ formatDate(userStore.user?.created_at) }}</span>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-label">最后登录</span>
                  <span class="stat-value">{{ formatDate(userStore.user?.last_login) }}</span>
                </div>
              </div>
              
              <div class="stat-item" v-if="userStore.user?.blockchain_addr">
                <div class="stat-icon">
                  <el-icon><Link /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-label">区块链状态</span>
                  <el-tag type="success" size="small">已连接</el-tag>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 安全提示 -->
          <el-card shadow="hover" class="security-card">
            <template #header>
              <h3><el-icon><DataBoard /></el-icon> 安全提示</h3>
            </template>
            
            <div class="security-tips">
              <el-alert
                title="账户安全提醒"
                type="info"
                :closable="false"
                show-icon
              >
                <ul class="tips-list">
                  <li>定期更换密码，确保账户安全</li>
                  <li>不要在公共设备上保存密码</li>
                  <li>妥善保管区块链钱包地址</li>
                  <li>发现异常登录请及时联系管理员</li>
                </ul>
              </el-alert>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import {
  User, Edit, Lock, Key, Check, Close, Message, Link, Avatar,
  Calendar, Clock, DataBoard, CopyDocument
} from '@element-plus/icons-vue'
import api from '@/utils/api'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'

// 配置dayjs
dayjs.locale('zh-cn')
dayjs.extend(relativeTime)

const userStore = useUserStore()
const loading = ref(false)
const passwordLoading = ref(false)
const isEditing = ref(false)

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

// 个人信息表单
const profileForm = reactive({
  username: '',
  email: '',
  role: '',
  blockchain_addr: ''
})

// 密码修改表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 个人信息验证规则
const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在2-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  blockchain_addr: [
    {
      pattern: /^0x[a-fA-F0-9]{40}$/,
      message: '请输入正确的以太坊地址格式',
      trigger: 'blur'
    }
  ]
}

// 密码验证规则
const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{6,}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算用户头像
const userAvatar = computed(() => {
  const name = (userStore.user?.username || userStore.user?.name) || '用户'
  const hash = name.split('').reduce((acc: number, char: string) => {
    return acc + char.charCodeAt(0)
  }, 0)
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${hash}`
})

// 获取角色显示文本
const getRoleDisplay = (role?: string) => {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    doctor: '医生',
    patient: '患者'
  }
  return roleMap[role || ''] || '未知'
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return '未知'
  try {
    const date = dayjs(dateString)
    return date.format('YYYY年MM月DD日 HH:mm')
  } catch {
    return '无效日期'
  }
}

// 复制到剪贴板
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 初始化表单数据
const initializeForm = () => {
  if (userStore.user) {
    profileForm.username = userStore.user.username || userStore.user.name || ''
    profileForm.email = userStore.user.email || ''
    profileForm.role = userStore.user.role || ''
    profileForm.blockchain_addr = userStore.user.blockchain_addr || ''
  }
}

// 切换编辑模式
const toggleEdit = () => {
  if (isEditing.value) {
    handleCancel()
  } else {
    isEditing.value = true
    initializeForm()
  }
}

// 取消编辑
const handleCancel = () => {
  isEditing.value = false
  initializeForm()
  profileFormRef.value?.clearValidate()
}

// 保存个人信息
const handleSave = async () => {
  if (!profileFormRef.value) return
  
  try {
    await profileFormRef.value.validate()
    loading.value = true
    
    const updateData = {
      username: profileForm.username,
      email: profileForm.email,
      blockchain_addr: profileForm.blockchain_addr || undefined
    }
    
    const response = await api.put('/auth/me', updateData)
    
    // 更新本地用户信息
    if (userStore.user) {
      Object.assign(userStore.user, response as any)
    }
    
    isEditing.value = false
    ElMessage.success('个人信息更新成功')
  } catch (error: any) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.message || '更新失败，请重试')
  } finally {
    loading.value = false
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    
    await ElMessageBox.confirm(
      '确认要修改密码吗？修改后需要重新登录。',
      '确认修改',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    passwordLoading.value = true
    
    await api.put('/auth/change-password', {
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    
    // 清空表单
    Object.assign(passwordForm, {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    ElMessage.success('密码修改成功，请重新登录')
    
    // 延迟登出，给用户看到成功消息
    setTimeout(() => {
      userStore.logout()
      window.location.href = '/login'
    }, 2000)
    
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('密码修改失败:', error)
      ElMessage.error(error.response?.data?.message || '密码修改失败，请重试')
    }
  } finally {
    passwordLoading.value = false
  }
}

// 组件加载时初始化
onMounted(() => {
  initializeForm()
})
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 24px;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-avatar {
  flex-shrink: 0;
}

.user-info {
  color: white;
}

.user-name {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-role {
  font-size: 16px;
  margin: 0 0 4px 0;
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 12px;
  display: inline-block;
}

.user-email {
  font-size: 14px;
  margin: 0;
  opacity: 0.8;
}

.profile-content {
  max-width: 1200px;
  margin: 0 auto;
}

.info-card,
.password-card,
.stats-card,
.security-card {
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.info-card:hover,
.password-card:hover,
.stats-card:hover,
.security-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.profile-form {
  max-width: 600px;
}

.password-form {
  max-width: 400px;
}

.stats-content {
  padding: 0;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
  gap: 16px;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.security-tips {
  padding: 0;
}

.tips-list {
  margin: 16px 0 0 0;
  padding-left: 20px;
  list-style: none;
}

.tips-list li {
  position: relative;
  padding: 8px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.4;
}

.tips-list li::before {
  content: '•';
  position: absolute;
  left: -15px;
  color: #409eff;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container {
    padding: 12px;
  }
  
  .profile-header {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .user-name {
    font-size: 24px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .profile-form,
  .password-form {
    max-width: 100%;
  }
}

/* 动画效果 */
.el-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.el-button {
  transition: all 0.3s ease;
}

.el-input {
  transition: all 0.3s ease;
}

.el-form-item {
  margin-bottom: 22px;
}

/* 美化表单元素 */
:deep(.el-input__wrapper) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
}

:deep(.el-card__header) {
  background: #fafbfc;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-alert) {
  border-radius: 8px;
}

:deep(.el-tag) {
  border-radius: 12px;
}
</style>