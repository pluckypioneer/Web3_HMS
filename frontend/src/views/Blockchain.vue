<template>
  <div class="layout-container">
    <!-- Header -->
    <el-header class="layout-header">
      <div class="flex-between">
        <div class="flex-center gap-16">
          <h1 style="color: white; margin: 0;">区块链管理</h1>
        </div>
        <div class="flex-center gap-16">
          <el-button type="primary" @click="refreshStatus">
            <el-icon><Refresh /></el-icon>
            刷新状态
          </el-button>
          <el-button @click="$router.push('/dashboard')">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-button>
        </div>
      </div>
    </el-header>

    <!-- Main Content -->
    <el-main class="layout-main">
      <div class="blockchain-container">
        <!-- Blockchain Status -->
        <div class="blockchain-status-card mb-24">
          <div class="blockchain-info">
            <div class="blockchain-status">
              <div 
                class="blockchain-indicator"
                :class="{ 'connected': blockchainStatus.connected, 'disconnected': !blockchainStatus.connected }"
              ></div>
              <span>{{ blockchainStatus.connected ? '区块链连接正常' : '区块链连接断开' }}</span>
            </div>
            <div class="status-details">
              <p><strong>最新区块:</strong> {{ blockchainStatus.latestBlock }}</p>
              <p><strong>网络ID:</strong> {{ blockchainStatus.networkId }}</p>
              <p><strong>连接时间:</strong> {{ connectionTime }}</p>
            </div>
          </div>
        </div>

        <!-- Contract Information -->
        <el-row :gutter="24" class="mb-24">
          <el-col :xs="24" :md="8" v-for="contract in contracts" :key="contract.name">
            <div class="info-card p-24">
              <h3>{{ contract.name }}</h3>
              <div class="contract-details">
                <p><strong>地址:</strong> {{ contract.address }}</p>
                <p><strong>网络:</strong> {{ contract.network }}</p>
                <p><strong>部署时间:</strong> {{ formatDate(contract.deploy_time) }}</p>
                <p><strong>状态:</strong> 
                  <el-tag :type="contract.is_active ? 'success' : 'danger'">
                    {{ contract.is_active ? '活跃' : '非活跃' }}
                  </el-tag>
                </p>
              </div>
            </div>
          </el-col>
        </el-row>

        <!-- Data Verification -->
        <div class="table-container mb-24">
          <div class="table-header">
            <h3 class="table-title">数据验证</h3>
          </div>
          <div class="p-24">
            <el-form :model="verificationForm" label-width="120px">
              <el-row :gutter="24">
                <el-col :xs="24" :md="12">
                  <el-form-item label="记录ID">
                    <el-input v-model="verificationForm.recordId" placeholder="请输入记录ID" />
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :md="12">
                  <el-form-item label="哈希值">
                    <el-input v-model="verificationForm.hashValue" placeholder="请输入哈希值" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item>
                <el-button type="primary" @click="verifyData" :loading="verifying">
                  <el-icon><Check /></el-icon>
                  验证数据
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="verificationResult" class="verification-result">
              <h4>验证结果</h4>
              <div class="result-details">
                <p><strong>数据完整性:</strong> 
                  <el-tag :type="verificationResult.valid ? 'success' : 'danger'">
                    {{ verificationResult.valid ? '有效' : '无效' }}
                  </el-tag>
                </p>
                <p><strong>当前哈希:</strong> {{ verificationResult.current_hash }}</p>
                <p><strong>提供哈希:</strong> {{ verificationResult.provided_hash }}</p>
                <p><strong>区块链验证:</strong> 
                  <el-tag :type="verificationResult.blockchain_verified ? 'success' : 'warning'">
                    {{ verificationResult.blockchain_verified ? '已验证' : '未验证' }}
                  </el-tag>
                </p>
                <p v-if="verificationResult.block_number">
                  <strong>区块号:</strong> {{ verificationResult.block_number }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Transactions -->
        <div class="table-container">
          <div class="table-header">
            <h3 class="table-title">最近交易</h3>
          </div>
          <el-table :data="recentTransactions" style="width: 100%">
            <el-table-column prop="tx_hash" label="交易哈希" width="200">
              <template #default="scope">
                <el-link :href="getEtherscanUrl(scope.row.tx_hash)" target="_blank">
                  {{ scope.row.tx_hash.substring(0, 10) }}...
                </el-link>
              </template>
            </el-table-column>
            <el-table-column prop="data_type" label="数据类型" />
            <el-table-column prop="block_number" label="区块号" />
            <el-table-column prop="gas_used" label="Gas使用量" />
            <el-table-column prop="created_at" label="创建时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import api from '@/utils/api'

const blockchainStatus = ref({
  connected: false,
  latestBlock: 0,
  networkId: 0
})

const contracts = ref([])
const recentTransactions = ref([])
const verifying = ref(false)
const verificationResult = ref(null)

const verificationForm = ref({
  recordId: '',
  hashValue: ''
})

const connectionTime = computed(() => {
  return dayjs().format('YYYY-MM-DD HH:mm:ss')
})

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const getEtherscanUrl = (txHash: string) => {
  return `https://sepolia.etherscan.io/tx/${txHash}`
}

const refreshStatus = async () => {
  try {
    await loadBlockchainStatus()
    await loadContracts()
    await loadRecentTransactions()
    ElMessage.success('状态刷新成功')
  } catch (error) {
    ElMessage.error('状态刷新失败')
  }
}

const loadBlockchainStatus = async () => {
  try {
    const response = await api.get('/blockchain/status')
    blockchainStatus.value = response.data
  } catch (error) {
    console.error('Failed to load blockchain status:', error)
  }
}

const loadContracts = async () => {
  try {
    const response = await api.get('/blockchain/contracts')
    contracts.value = response.data.contracts
  } catch (error) {
    console.error('Failed to load contracts:', error)
  }
}

const loadRecentTransactions = async () => {
  try {
    const response = await api.get('/blockchain/transactions?limit=10')
    recentTransactions.value = response.data.transactions
  } catch (error) {
    console.error('Failed to load recent transactions:', error)
  }
}

const verifyData = async () => {
  if (!verificationForm.value.recordId || !verificationForm.value.hashValue) {
    ElMessage.warning('请输入记录ID和哈希值')
    return
  }

  verifying.value = true
  try {
    const response = await api.get('/blockchain/verify', {
      params: {
        record_id: verificationForm.value.recordId,
        hash_value: verificationForm.value.hashValue
      }
    })
    verificationResult.value = response.data
    ElMessage.success('数据验证完成')
  } catch (error) {
    ElMessage.error('数据验证失败')
  } finally {
    verifying.value = false
  }
}

onMounted(() => {
  refreshStatus()
})
</script>

<style scoped>
.blockchain-container {
  max-width: 1200px;
  margin: 0 auto;
}

.blockchain-status-card {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  border-radius: 12px;
  padding: 24px;
}

.blockchain-status {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.blockchain-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #f56c6c;
  animation: pulse 2s infinite;
}

.blockchain-indicator.connected {
  background-color: #67c23a;
}

.blockchain-indicator.disconnected {
  background-color: #f56c6c;
}

.status-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.status-details p {
  margin: 0;
  font-size: 14px;
}

.contract-details p {
  margin: 8px 0;
  font-size: 14px;
}

.verification-result {
  margin-top: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.verification-result h4 {
  margin-bottom: 16px;
  color: #2c3e50;
}

.result-details p {
  margin: 8px 0;
  font-size: 14px;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(103, 194, 58, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(103, 194, 58, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(103, 194, 58, 0);
  }
}
</style>
