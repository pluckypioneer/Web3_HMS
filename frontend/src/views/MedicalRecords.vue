<template>
  <div class="medical-records-page">
    <el-card class="page-card">
      <template #header>
        <div class="flex-between">
          <h1>病历管理</h1>
          <el-button type="primary" @click="showAddForm">
            <el-icon><Plus /></el-icon>
            新增病历
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
        <el-form-item label="病历类型">
          <el-select v-model="searchForm.recordType" placeholder="请选择病历类型" clearable>
            <el-option label="电子病历" value="EMR" />
            <el-option label="处方" value="PRESCRIPTION" />
            <el-option label="手术记录" value="SURGERY" />
            <el-option label="检查报告" value="REPORT" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input 
            v-model="searchForm.search" 
            placeholder="请输入标题、诊断或内容关键词" 
            clearable
            @keyup.enter="searchRecords"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchRecords">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 病历表格 -->
      <el-table 
        :data="medicalRecords" 
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="title" label="标题" width="200" />
        <el-table-column prop="record_type" label="类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.record_type === 'EMR'">电子病历</el-tag>
            <el-tag v-else-if="scope.row.record_type === 'PRESCRIPTION'" type="success">处方</el-tag>
            <el-tag v-else-if="scope.row.record_type === 'SURGERY'" type="warning">手术记录</el-tag>
            <el-tag v-else-if="scope.row.record_type === 'REPORT'" type="info">检查报告</el-tag>
            <el-tag v-else>{{ scope.row.record_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="patient_id" label="患者ID" width="150" />
        <el-table-column prop="doctor_id" label="医生ID" width="150" />
        <el-table-column prop="diagnosis" label="诊断结果" width="200" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="保密" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_confidential ? 'danger' : 'success'">
              {{ scope.row.is_confidential ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewRecord(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="editRecord(scope.row.id)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteRecord(scope.row.id)">
              删除
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

    <!-- 新增/编辑病历对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef" 
        :model="recordForm" 
        :rules="formRules" 
        label-width="100px"
      >
        <el-form-item label="患者ID" prop="patient_id">
          <el-input v-model="recordForm.patient_id" />
        </el-form-item>
        <el-form-item label="医生ID" prop="doctor_id">
          <el-input v-model="recordForm.doctor_id" />
        </el-form-item>
        <el-form-item label="病历类型" prop="record_type">
          <el-select v-model="recordForm.record_type" placeholder="请选择病历类型" style="width: 100%">
            <el-option label="电子病历" value="EMR" />
            <el-option label="处方" value="PRESCRIPTION" />
            <el-option label="手术记录" value="SURGERY" />
            <el-option label="检查报告" value="REPORT" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="recordForm.title" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input 
            v-model="recordForm.content" 
            type="textarea" 
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="诊断结果" prop="diagnosis">
          <el-input 
            v-model="recordForm.diagnosis" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="治疗方案" prop="treatment">
          <el-input 
            v-model="recordForm.treatment" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="处方" prop="prescription">
          <el-input 
            v-model="recordForm.prescription" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input 
            v-model="recordForm.notes" 
            type="textarea" 
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="保密">
          <el-switch v-model="recordForm.is_confidential" />
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

interface MedicalRecord {
  id: string
  patient_id: string
  doctor_id: string
  record_type: string
  title: string
  content: string
  diagnosis: string
  treatment: string
  prescription: string
  notes: string
  is_confidential: boolean
  created_at: string
}

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增病历')
const isEdit = ref(false)
const editRecordId = ref('')

const medicalRecords = ref<MedicalRecord[]>([])

const searchForm = reactive({
  patientId: '',
  doctorId: '',
  recordType: '',
  search: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

const recordForm = reactive({
  patient_id: '',
  doctor_id: '',
  record_type: '',
  title: '',
  content: '',
  diagnosis: '',
  treatment: '',
  prescription: '',
  notes: '',
  is_confidential: false
})

const formRules = {
  patient_id: [{ required: true, message: '请输入患者ID', trigger: 'blur' }],
  doctor_id: [{ required: true, message: '请输入医生ID', trigger: 'blur' }],
  record_type: [{ required: true, message: '请选择病历类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

// 获取病历列表
const fetchRecords = async () => {
  try {
    loading.value = true
    const params: any = {
      page: pagination.currentPage,
      per_page: pagination.pageSize
    }
    
    if (searchForm.patientId) params.patient_id = searchForm.patientId
    if (searchForm.doctorId) params.doctor_id = searchForm.doctorId
    if (searchForm.recordType) params.record_type = searchForm.recordType
    if (searchForm.search) params.search = searchForm.search
    
    const response = await api.get('/medical-records', { params })
    
    medicalRecords.value = response.data.records
    pagination.total = response.data.total
  } catch (error) {
    ElMessage.error('获取病历列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索病历
const searchRecords = () => {
  pagination.currentPage = 1
  fetchRecords()
}

// 重置搜索
const resetSearch = () => {
  searchForm.patientId = ''
  searchForm.doctorId = ''
  searchForm.recordType = ''
  searchForm.search = ''
  pagination.currentPage = 1
  fetchRecords()
}

// 分页相关
const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  fetchRecords()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  fetchRecords()
}

// 格式化时间
const formatDateTime = (date: string) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 显示新增表单
const showAddForm = () => {
  dialogTitle.value = '新增病历'
  isEdit.value = false
  dialogVisible.value = true
}

// 显示编辑表单
const showEditForm = (record: MedicalRecord) => {
  dialogTitle.value = '编辑病历'
  isEdit.value = true
  editRecordId.value = record.id
  
  // 填充表单数据
  recordForm.patient_id = record.patient_id
  recordForm.doctor_id = record.doctor_id
  recordForm.record_type = record.record_type
  recordForm.title = record.title
  recordForm.content = record.content
  recordForm.diagnosis = record.diagnosis
  recordForm.treatment = record.treatment
  recordForm.prescription = record.prescription
  recordForm.notes = record.notes
  recordForm.is_confidential = record.is_confidential
  
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  try {
    submitLoading.value = true
    
    if (isEdit.value) {
      // 编辑病历
      await api.put(`/medical-records/${editRecordId.value}`, recordForm)
      ElMessage.success('病历更新成功')
    } else {
      // 新增病历
      await api.post('/medical-records', recordForm)
      ElMessage.success('病历添加成功')
    }
    
    dialogVisible.value = false
    fetchRecords()
  } catch (error) {
    ElMessage.error(isEdit.value ? '病历更新失败' : '病历添加失败')
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(recordForm, {
    patient_id: '',
    doctor_id: '',
    record_type: '',
    title: '',
    content: '',
    diagnosis: '',
    treatment: '',
    prescription: '',
    notes: '',
    is_confidential: false
  })
}

// 查看病历
const viewRecord = (id: string) => {
  ElMessage.info(`查看病历 ${id} 功能待实现`)
  // 这里可以跳转到病历详情页面
}

// 编辑病历
const editRecord = (id: string) => {
  const record = medicalRecords.value.find(item => item.id === id)
  if (record) {
    showEditForm(record)
  }
}

// 删除病历
const deleteRecord = (id: string) => {
  ElMessageBox.confirm('确定要删除该病历吗？此操作不可恢复', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.delete(`/medical-records/${id}`)
      ElMessage.success('删除成功')
      fetchRecords()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.medical-records-page {
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