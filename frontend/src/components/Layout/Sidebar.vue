<template>
  <el-scrollbar class="sidebar-scrollbar">
    <el-menu
      default-active="dashboard"
      class="sidebar-menu"
      mode="vertical"
      @select="handleMenuSelect"
    >
      <el-menu-item index="dashboard">
        <el-icon><Home /></el-icon>
        <span>首页</span>
      </el-menu-item>
      
      <el-sub-menu index="patients" v-if="hasPermission(['doctor', 'admin'])">
        <template #title>
          <el-icon><UserFilled /></el-icon>
          <span>患者管理</span>
        </template>
        <el-menu-item index="patients/list">患者列表</el-menu-item>
        <el-menu-item index="patients/add">新增患者</el-menu-item>
      </el-sub-menu>
      
      <el-menu-item index="appointments">
        <el-icon><Calendar /></el-icon>
        <span>预约管理</span>
      </el-menu-item>
      
      <el-menu-item index="medical-records" v-if="hasPermission(['doctor', 'admin'])">
        <el-icon><Document /></el-icon>
        <span>病历管理</span>
      </el-menu-item>
      
      <el-menu-item index="prescriptions" v-if="hasPermission(['doctor', 'admin'])">
        <el-icon><MedicineBox /></el-icon>
        <span>处方管理</span>
      </el-menu-item>
      
      <el-menu-item index="inventory" v-if="hasPermission(['admin'])">
        <el-icon><Box /></el-icon>
        <span>药品库存</span>
      </el-menu-item>
      
      <el-menu-item index="blockchain" v-if="hasPermission(['admin'])">
        <el-icon><Link /></el-icon>
        <span>区块链管理</span>
      </el-menu-item>
      
      <el-menu-item index="statistics" v-if="hasPermission(['admin'])">
        <el-icon><Histogram /></el-icon>
        <span>统计分析</span>
      </el-menu-item>
    </el-menu>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const routeMap: Record<string, string> = {
  'dashboard': '/dashboard',
  'patients/list': '/patients',
  'patients/add': '/patients/add',
  'appointments': '/appointments',
  'medical-records': '/medical-records',
  'prescriptions': '/prescriptions',
  'inventory': '/inventory',
  'blockchain': '/blockchain',
  'statistics': '/statistics'
}

const handleMenuSelect = (index: string) => {
  const path = routeMap[index]
  if (path) {
    router.push(path)
  }
}

const hasPermission = (roles: string[]) => {
  if (!userStore.user) return false
  return roles.includes(userStore.user.role)
}
</script>

<style scoped>
.sidebar-scrollbar {
  height: 100%;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
  padding-top: 20px;
}
</style>