<template>
  <div class="appointments-page">
    <el-card class="page-card">
      <template #header>
        <div class="flex-between">
          <h1>预约管理</h1>
          <el-button type="primary" @click="showAddForm">
            <el-icon><Plus /></el-icon>
            创建预约
          </el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="患者ID">
          <el-input 
            v-model="searchForm.patientId" 
            placeholder="请输入患者ID" 
            clearable
          />
        </el-form-item>
        <el-form-item label="医生ID">
          <el-input 
            v-model="searchForm.doctorId" 
            placeholder="请输入医生ID" 
            clearable
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="已预约" value="SCHEDULED" />
            <el-option label="已确认" value="CONFIRMED" />
            <el-option label="已完成" value="COMPLETED" />
            <el-option label="已取消" value="CANCELLED" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchAppointments">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 预约表格 -->
      <el-table 
        :data="appointments" 
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="id" label="预约ID" width="150" />
        <el-table-column prop="patient_id" label="患者ID" width="150" />
        <el-table-column prop="doctor_id" label="医生ID" width="150" />
        <el-table-column prop="dept_name" label="科室" width="120" />
        <el-table-column prop="schedule_time" label="预约时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.schedule_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="appointment_type" label="类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.appointment_type === 'OUTPATIENT'">门诊</el-tag>
            <el-tag v-else-if="scope.row.appointment_type === 'FOLLOW_UP'" type="success">复诊</el-tag>
            <el-tag v-else-if="scope.row.appointment_type === 'EMERGENCY'" type="danger">急诊</el-tag>
            <span v-else>{{ scope.row.appointment_type }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'SCHEDULED'">已预约</el-tag>
            <el-tag v-else-if="scope.row.status === 'CONFIRMED'" type="success">已确认</el-tag>
            <el-tag v-else-if="scope.row.status === 'COMPLETED'" type="info">已完成</el-tag>
            <el-tag v-else-if="scope.row.status === 'CANCELLED'" type="danger">已取消</el-tag>
            <span v-else>{{ scope.row.status }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="fee" label="费用" width="100">
          <template #default="scope">
            ¥{{ scope.row.fee }}
          </template>
        </el-table-column>
        <el-table-column label="支付状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_paid ? 'success' : 'danger'">
              {{ scope.row.is_paid ? '已支付' : '未支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewAppointment(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="editAppointment(scope.row.id)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="cancelAppointment(scope.row.id)">
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 创建/编辑预约对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef" 
        :model="appointmentForm" 
        :rules="formRules" 
        label-width="100px"
      >
        <el-form-item label="患者ID" prop="patient_id">
          <el-input v-model="appointmentForm.patient_id" />
        </el-form-item>
        <el-form-item label="医生ID" prop="doctor_id">
          <el-input v-model="appointmentForm.doctor_id" />
        </el-form-item>
        <el-form-item label="科室ID" prop="dept_id">
          <el-input v-model="appointmentForm.dept_id" />
        </el-form-item>
        <el-form-item label="科室名称" prop="dept_name">
          <el-input v-model="appointmentForm.dept_name" />
        </el-form-item>
        <el-form-item label="预约时间" prop="schedule_time">
          <el-date-picker
            v-model="appointmentForm.schedule_time"
            type="datetime"
            placeholder="请选择预约时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预约类型" prop="appointment_type">
          <el-select v-model="appointmentForm.appointment_type" placeholder="请选择预约类型" style="width: 100%">
            <el-option label="门诊" value="OUTPATIENT" />
            <el-option label="复诊" value="FOLLOW_UP" />
            <el-option label="急诊" value="EMERGENCY" />
          </el-select>
        </el-form-item>
        <el-form-item label="预约原因" prop="reason">
          <el-input 
            v-model="appointmentForm.reason" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input 
            v-model="appointmentForm.notes" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="费用" prop="fee">
          <el-input-number 
            v-model="appointmentForm.fee" 
            :min="0" 
            :step="0.01" 
            controls-position="right" 
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="支付状态">
          <el-switch v-model="appointmentForm.is_paid" />
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method">
          <el-input v-model="appointmentForm.payment_method" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'
import dayjs from 'dayjs'

interface Appointment {
  id: string
  patient_id: string
  doctor_id: string
  dept_id: string
  dept_name: string
  schedule_time: string
  appointment_type: string
  status: string
  reason: string
  notes: string
  fee: number
  is_paid: boolean
  payment_method: string
  payment_tx_hash: string
  created_at: string
  updated_at: string
}

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('创建预约')
const isEdit = ref(false)
const editAppointmentId = ref('')

const appointments = ref<Appointment[]>([])

const searchForm = reactive({
  patientId: '',
  doctorId: '',
  status: '',
  dateRange: []
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

const appointmentForm = reactive({
  patient_id: '',
  doctor_id: '',
  dept_id: '',
  dept_name: '',
  schedule_time: '',
  appointment_type: 'OUTPATIENT',
  reason: '',
  notes: '',
  fee: 0,
  is_paid: false,
  payment_method: ''
})

const formRules = {
  patient_id: [{ required: true, message: '请输入患者ID', trigger: 'blur' }],
  doctor_id: [{ required: true, message: '请输入医生ID', trigger: 'blur' }],
  dept_id: [{ required: true, message: '请输入科室ID', trigger: 'blur' }],
  dept_name: [{ required: true, message: '请输入科室名称', trigger: 'blur' }],
  schedule_time: [{ required: true, message: '请选择预约时间', trigger: 'change' }],
  appointment_type: [{ required: true, message: '请选择预约类型', trigger: 'change' }]
}

// 获取预约列表
const fetchAppointments = async () => {
  try {
    loading.value = true
    const params: any = {
      page: pagination.currentPage,
      per_page: pagination.pageSize
    }
    
    if (searchForm.patientId) params.patient_id = searchForm.patientId
    if (searchForm.doctorId) params.doctor_id = searchForm.doctorId
    if (searchForm.status) params.status = searchForm.status
    
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.date_from = searchForm.dateRange[0]
      params.date_to = searchForm.dateRange[1]
    }
    
    const response = await api.get('/appointments', { params })
    
    appointments.value = response.data.appointments
    pagination.total = response.data.total
  } catch (error) {
    ElMessage.error('获取预约列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索预约
const searchAppointments = () => {
  pagination.currentPage = 1
  fetchAppointments()
}

// 重置搜索
const resetSearch = () => {
  searchForm.patientId = ''
  searchForm.doctorId = ''
  searchForm.status = ''
  searchForm.dateRange = []
  pagination.currentPage = 1
  fetchAppointments()
}

// 分页相关
const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  fetchAppointments()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  fetchAppointments()
}

// 格式化时间
const formatDateTime = (date: string) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 显示新增表单
const showAddForm = () => {
  dialogTitle.value = '创建预约'
  isEdit.value = false
  dialogVisible.value = true
}

// 显示编辑表单
const showEditForm = (appointment: Appointment) => {
  dialogTitle.value = '编辑预约'
  isEdit.value = true
  editAppointmentId.value = appointment.id
  
  // 填充表单数据
  appointmentForm.patient_id = appointment.patient_id
  appointmentForm.doctor_id = appointment.doctor_id
  appointmentForm.dept_id = appointment.dept_id
  appointmentForm.dept_name = appointment.dept_name
  appointmentForm.schedule_time = appointment.schedule_time
  appointmentForm.appointment_type = appointment.appointment_type
  appointmentForm.reason = appointment.reason
  appointmentForm.notes = appointment.notes
  appointmentForm.fee = appointment.fee
  appointmentForm.is_paid = appointment.is_paid
  appointmentForm.payment_method = appointment.payment_method
  
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  try {
    submitLoading.value = true
    
    if (isEdit.value) {
      // 编辑预约
      await api.put(`/appointments/${editAppointmentId.value}`, appointmentForm)
      ElMessage.success('预约更新成功')
    } else {
      // 创建预约
      await api.post('/appointments', appointmentForm)
      ElMessage.success('预约创建成功')
    }
    
    dialogVisible.value = false
    fetchAppointments()
  } catch (error) {
    ElMessage.error(isEdit.value ? '预约更新失败' : '预约创建失败')
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(appointmentForm, {
    patient_id: '',
    doctor_id: '',
    dept_id: '',
    dept_name: '',
    schedule_time: '',
    appointment_type: 'OUTPATIENT',
    reason: '',
    notes: '',
    fee: 0,
    is_paid: false,
    payment_method: ''
  })
}

// 查看预约
const viewAppointment = (id: string) => {
  ElMessage.info(`查看预约 ${id} 功能待实现`)
  // 这里可以跳转到预约详情页面
}

// 编辑预约
const editAppointment = (id: string) => {
  const appointment = appointments.value.find(item => item.id === id)
  if (appointment) {
    showEditForm(appointment)
  }
}

// 取消预约
const cancelAppointment = (id: string) => {
  ElMessageBox.confirm('确定要取消该预约吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.put(`/appointments/${id}`, { status: 'CANCELLED' })
      ElMessage.success('预约已取消')
      fetchAppointments()
    } catch (error) {
      ElMessage.error('取消预约失败')
      console.error(error)
    }
  }).catch(() => {
    // 用户取消操作
  })
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.appointments-page {
  padding: 20px;
}

.page-card {
  max-width: 1200px;
  margin: 0 auto;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>