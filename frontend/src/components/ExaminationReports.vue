<template>
  <div class="examination-reports">
    <div class="toolbar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索检查报告..."
        style="width: 200px; margin-right: 10px"
        clearable
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>
    
    <el-table :data="reports" stripe style="width: 100%">
      <el-table-column prop="date" label="检查日期" width="120" />
      <el-table-column prop="type" label="检查类型" width="150" />
      <el-table-column prop="department" label="科室" width="120" />
      <el-table-column prop="doctor" label="医生" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'completed' ? 'success' : 'warning'">
            {{ row.status === 'completed' ? '已完成' : '处理中' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleViewReport(row)">查看报告</el-button>
          <el-button size="small" @click="handleDownloadReport(row)">下载</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  patientId: string
}>()

const searchKeyword = ref('')
const reports = ref([
  {
    id: '1',
    date: '2023-05-01',
    type: '血常规检查',
    department: '检验科',
    doctor: '张医生',
    status: 'completed'
  },
  {
    id: '2',
    date: '2023-04-20',
    type: '心电图检查',
    department: '心电图室',
    doctor: '李医生',
    status: 'completed'
  }
])

const handleSearch = () => {
  ElMessage.info('搜索功能待实现')
}

const handleViewReport = (report: any) => {
  ElMessage.info(`查看报告 ${report.id}`)
}

const handleDownloadReport = (report: any) => {
  ElMessage.info(`下载报告 ${report.id}`)
}

onMounted(() => {
  // 模拟获取检查报告
  console.log('Fetching examination reports for patient:', props.patientId)
})
</script>

<style scoped>
.examination-reports {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  text-align: right;
}
</style>