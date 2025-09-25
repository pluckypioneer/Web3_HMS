<template>
  <div class="appointment-history">
    <div class="toolbar">
      <el-button type="primary" @click="handleNewAppointment">新建预约</el-button>
    </div>
    
    <el-table :data="appointments" stripe style="width: 100%">
      <el-table-column prop="date" label="预约日期" width="120" />
      <el-table-column prop="time" label="预约时间" width="120" />
      <el-table-column prop="doctor" label="医生" width="120" />
      <el-table-column prop="department" label="科室" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleViewAppointment(row)">查看</el-button>
          <el-button size="small" @click="handleCancelAppointment(row)" 
                     :disabled="row.status !== 'pending'">
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps<{
  patientId: string
}>()

const appointments = ref([
  {
    id: '1',
    date: '2023-05-20',
    time: '09:00',
    doctor: '李医生',
    department: '内科',
    status: 'pending'
  },
  {
    id: '2',
    date: '2023-04-15',
    time: '14:30',
    doctor: '王医生',
    department: '外科',
    status: 'completed'
  }
])

const getStatusType = (status: string) => {
  switch (status) {
    case 'pending': return 'warning'
    case 'confirmed': return 'primary'
    case 'completed': return 'success'
    case 'cancelled': return 'danger'
    default: return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending': return '待确认'
    case 'confirmed': return '已确认'
    case 'completed': return '已完成'
    case 'cancelled': return '已取消'
    default: return '未知'
  }
}

const handleNewAppointment = () => {
  ElMessage.info('新建预约功能待实现')
}

const handleViewAppointment = (appointment: any) => {
  ElMessage.info(`查看预约 ${appointment.id}`)
}

const handleCancelAppointment = (appointment: any) => {
  ElMessageBox.confirm(
    `确定要取消预约 #${appointment.id} 吗？`,
    '确认取消',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('预约已取消')
  }).catch(() => {
    // 用户取消操作
  })
}

onMounted(() => {
  // 模拟获取预约记录
  console.log('Fetching appointment history for patient:', props.patientId)
})
</script>

<style scoped>
.appointment-history {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  text-align: right;
}
</style>