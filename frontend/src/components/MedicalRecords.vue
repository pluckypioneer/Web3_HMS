<template>
  <div class="medical-records">
    <div class="toolbar">
      <el-button type="primary" @click="handleAddRecord">新增病历</el-button>
    </div>
    
    <el-table :data="medicalRecords" stripe style="width: 100%">
      <el-table-column prop="date" label="就诊日期" width="120" />
      <el-table-column prop="doctor" label="主治医生" width="120" />
      <el-table-column prop="diagnosis" label="诊断结果" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '有效' : '已归档' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleViewRecord(row)">查看</el-button>
          <el-button size="small" @click="handleEditRecord(row)">编辑</el-button>
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

const medicalRecords = ref([
  {
    id: '1',
    date: '2023-05-01',
    doctor: '李医生',
    diagnosis: '上呼吸道感染',
    status: 'active'
  },
  {
    id: '2',
    date: '2023-03-15',
    doctor: '王医生',
    diagnosis: '高血压',
    status: 'archived'
  }
])

const handleAddRecord = () => {
  ElMessage.info('新增病历功能待实现')
}

const handleViewRecord = (record: any) => {
  ElMessage.info(`查看病历 ${record.id}`)
}

const handleEditRecord = (record: any) => {
  ElMessage.info(`编辑病历 ${record.id}`)
}

onMounted(() => {
  // 模拟获取病历记录
  console.log('Fetching medical records for patient:', props.patientId)
})
</script>

<style scoped>
.medical-records {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  text-align: right;
}
</style>