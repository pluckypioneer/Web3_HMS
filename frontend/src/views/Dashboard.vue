<template>
  <div class="layout-container">
    <!-- Header -->
    <el-header class="layout-header">
      <div class="flex-between">
        <div class="flex-center gap-16">
          <h1 style="color: white; margin: 0;">Web3 医院管理系统</h1>
        </div>
        <div class="flex-center gap-16">
          <el-button type="primary" @click="$router.push('/blockchain')">
            <el-icon><Connection /></el-icon>
            区块链状态
          </el-button>
          <el-dropdown @command="handleCommand">
            <el-button type="primary">
              {{ userStore.user?.name || '用户' }}
              <el-icon><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <!-- Main Content -->
    <el-container>
      <!-- Sidebar -->
      <el-aside width="250px" class="layout-sidebar">
        <el-menu
          :default-active="$route.path"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/dashboard">
            <el-icon><House /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <el-menu-item index="/patients" v-if="userStore.hasRole(['doctor', 'admin'])">
            <el-icon><User /></el-icon>
            <span>患者管理</span>
          </el-menu-item>
          
          <el-menu-item index="/appointments">
            <el-icon><Calendar /></el-icon>
            <span>预约管理</span>
          </el-menu-item>
          
          <el-menu-item index="/medical-records" v-if="userStore.hasRole(['doctor', 'admin'])">
            <el-icon><Document /></el-icon>
            <span>病历管理</span>
          </el-menu-item>
          
          <el-menu-item index="/blockchain" v-if="userStore.hasRole(['admin'])">
            <el-icon><Connection /></el-icon>
            <span>区块链管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- Main Content Area -->
      <el-main class="layout-main">
        <div class="dashboard-container">
          <!-- Welcome Section -->
          <div class="welcome-section mb-24">
            <h2>欢迎回来，{{ userStore.user?.name }}！</h2>
            <p>今天是 {{ currentDate }}，祝您工作愉快！</p>
          </div>

          <!-- Stats Cards -->
          <el-row :gutter="24" class="mb-24">
            <el-col :xs="24" :sm="12" :md="6">
              <div class="info-card p-24">
                <div class="flex-between">
                  <div>
                    <h3>今日预约</h3>
                    <p class="stat-number">{{ stats.todayAppointments }}</p>
                  </div>
                  <el-icon size="40" color="#409eff"><Calendar /></el-icon>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <div class="info-card p-24">
                <div class="flex-between">
                  <div>
                    <h3>在院患者</h3>
                    <p class="stat-number">{{ stats.inpatients }}</p>
                  </div>
                  <el-icon size="40" color="#67c23a"><User /></el-icon>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <div class="info-card p-24">
                <div class="flex-between">
                  <div>
                    <h3>病历记录</h3>
                    <p class="stat-number">{{ stats.medicalRecords }}</p>
                  </div>
                  <el-icon size="40" color="#e6a23c"><Document /></el-icon>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="6">
              <div class="info-card p-24">
                <div class="flex-between">
                  <div>
                    <h3>区块链交易</h3>
                    <p class="stat-number">{{ stats.blockchainTx }}</p>
                  </div>
                  <el-icon size="40" color="#f56c6c"><Connection /></el-icon>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Recent Activities -->
          <el-row :gutter="24">
            <el-col :xs="24" :lg="12">
              <div class="table-container">
                <div class="table-header">
                  <h3 class="table-title">最近预约</h3>
                </div>
                <el-table :data="recentAppointments" style="width: 100%">
                  <el-table-column prop="patient_name" label="患者姓名" />
                  <el-table-column prop="doctor_name" label="医生" />
                  <el-table-column prop="schedule_time" label="预约时间" />
                  <el-table-column prop="status" label="状态">
                    <template #default="scope">
                      <el-tag :type="getStatusType(scope.row.status)">
                        {{ getStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-col>
            
            <el-col :xs="24" :lg="12">
              <div class="table-container">
                <div class="table-header">
                  <h3 class="table-title">区块链状态</h3>
                </div>
                <div class="blockchain-info">
                  <div class="blockchain-status">
                    <div class="blockchain-indicator"></div>
                    <span>区块链连接正常</span>
                  </div>
                  <p>最新区块: {{ blockchainStatus.latestBlock }}</p>
                  <p>网络ID: {{ blockchainStatus.networkId }}</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import api from '@/utils/api'

const userStore = useUserStore()
const router = useRouter()

const stats = ref({
  todayAppointments: 0,
  inpatients: 0,
  medicalRecords: 0,
  blockchainTx: 0
})

const recentAppointments = ref([])
const blockchainStatus = ref({
  latestBlock: 0,
  networkId: 0
})

const currentDate = computed(() => {
  return dayjs().format('YYYY年MM月DD日 dddd')
})

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'SCHEDULED': 'info',
    'CONFIRMED': 'success',
    'CANCELLED': 'danger',
    'COMPLETED': 'success'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'SCHEDULED': '已预约',
    'CONFIRMED': '已确认',
    'CANCELLED': '已取消',
    'COMPLETED': '已完成'
  }
  return statusMap[status] || status
}

const handleCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

const loadDashboardData = async () => {
  try {
    // Load stats
    const statsResponse = await api.get('/dashboard/stats')
    stats.value = statsResponse.data
    
    // Load recent appointments
    const appointmentsResponse = await api.get('/appointments?limit=5')
    recentAppointments.value = appointmentsResponse.data.appointments
    
    // Load blockchain status
    const blockchainResponse = await api.get('/blockchain/status')
    blockchainStatus.value = blockchainResponse.data
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section h2 {
  color: var(--text-primary);
  margin-bottom: 8px;
}

.welcome-section p {
  color: var(--text-secondary);
  font-size: 16px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: var(--text-primary);
  margin: 8px 0;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: var(--primary-color);
  color: white;
}

.sidebar-menu .el-menu-item.is-active .el-icon {
  color: white;
}
</style>
