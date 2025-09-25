<template>
  <div class="navbar">
    <div class="logo">
      <el-icon class="logo-icon"><Hospital /></el-icon>
      <span>Web3 医院管理系统</span>
    </div>
    
    <div class="user-info">
      <el-dropdown>
        <div class="user-dropdown">
          <el-avatar :src="userAvatar" class="user-avatar" />
          <span class="user-name">{{ userStore.user?.name }}</span>
          <el-icon class="dropdown-icon"><CaretBottom /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleProfile">
              <el-icon><User /></el-icon>
              <span>个人中心</span>
            </el-dropdown-item>
            <el-dropdown-item @click="handleSettings">
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">
              <el-icon><Logout /></el-icon>
              <span>退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const userAvatar = computed(() => {
  // 生成基于用户名的随机头像颜色
  const name = userStore.user?.name || '用户'
  const colors = [
    '#409eff', '#67c23a', '#e6a23c', '#f56c6c', 
    '#909399', '#c0c4cc', '#722ed1', '#1890ff'
  ]
  const hash = name.split('').reduce((acc, char) => {
    return acc + char.charCodeAt(0)
  }, 0)
  return `https://picsum.photos/seed/${hash}/200`
})

const handleProfile = () => {
  router.push('/profile')
}

const handleSettings = () => {
  router.push('/settings')
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已成功退出登录')
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.logo-icon {
  font-size: 24px;
  color: #409eff;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.user-avatar {
  width: 36px;
  height: 36px;
}

.user-name {
  font-size: 14px;
  color: #303133;
}

.dropdown-icon {
  font-size: 16px;
  color: #909399;
}
</style>