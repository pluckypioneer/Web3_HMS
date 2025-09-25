<template>
  <div class="blockchain-records">
    <div class="toolbar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索区块链记录..."
        style="width: 200px; margin-right: 10px"
        clearable
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>
    
    <el-table :data="records" stripe style="width: 100%">
      <el-table-column prop="date" label="记录日期" width="120" />
      <el-table-column prop="type" label="记录类型" width="150" />
      <el-table-column prop="hash" label="哈希值" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'confirmed' ? 'success' : 'warning'">
            {{ row.status === 'confirmed' ? '已确认' : '待确认' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleViewDetails(row)">查看详情</el-button>
          <el-button size="small" @click="handleVerify(row)">验证</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="info-section">
      <el-alert
        title="区块链存证说明"
        description="所有患者的重要医疗记录都会通过区块链技术进行存证，确保数据不可篡改且可追溯。"
        type="info"
        show-icon
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  patientId: string
}>()

const searchKeyword = ref('')
const records = ref([
  {
    id: '1',
    date: '2023-05-01',
    type: '病历记录',
    hash: '0x1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890',
    status: 'confirmed'
  },
  {
    id: '2',
    date: '2023-04-20',
    type: '检查报告',
    hash: '0x2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890a',
    status: 'confirmed'
  }
])

const handleSearch = () => {
  ElMessage.info('搜索功能待实现')
}

const handleViewDetails = (record: any) => {
  ElMessage.info(`查看记录详情 ${record.id}`)
}

const handleVerify = (record: any) => {
  ElMessage.info(`验证记录 ${record.id}`)
}

onMounted(() => {
  // 模拟获取区块链记录
  console.log('Fetching blockchain records for patient:', props.patientId)
})
</script>

<style scoped>
.blockchain-records {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  text-align: right;
}

.info-section {
  margin-top: 20px;
}
</style>