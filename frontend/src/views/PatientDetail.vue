<template>
  <div class="patient-detail-container">
    <el-page-header 
      @back="handleBack"
      content="患者详情"
    ></el-page-header>
    
    <el-card class="mt-16">
      <template #header>
        <div class="flex-between">
          <h2>患者基本信息</h2>
          <el-button type="primary" @click="editPatient">
            <el-icon><Edit /></el-icon>
            编辑信息
          </el-button>
        </div>
      </template>
      
      <div class="patient-info-grid">
        <div class="info-item">
          <span class="info-label">姓名:</span>
          <span class="info-value">{{ patientInfo.name }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">性别:</span>
          <span class="info-value">{{ patientInfo.gender === 'M' ? '男' : '女' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">年龄:</span>
          <span class="info-value">{{ calculateAge(patientInfo.birthdate) }}岁</span>
        </div>
        <div class="info-item">
          <span class="info-label">身份证号:</span>
          <span class="info-value">{{ patientInfo.id_card }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">联系电话:</span>
          <span class="info-value">{{ patientInfo.phone }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">邮箱:</span>
          <span class="info-value">{{ patientInfo.email }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">地址:</span>
          <span class="info-value">{{ patientInfo.address }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">医保卡号:</span>
          <span class="info-value">{{ patientInfo.insurance_number }}</span>
        </div>
      </div>
    </el-card>
    
    <el-tabs v-model="activeTab" class="mt-16">
      <el-tab-pane label="病历记录" name="records">
        <medical-records :patient-id="patientId" />
      </el-tab-pane>
      <el-tab-pane label="预约记录" name="appointments">
        <appointment-history :patient-id="patientId" />
      </el-tab-pane>
      <el-tab-pane label="检查报告" name="reports">
        <examination-reports :patient-id="patientId" />
      </el-tab-pane>
      <el-tab-pane label="区块链存证" name="blockchain">
        <blockchain-records :patient-id="patientId" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'
import MedicalRecords from '@/components/MedicalRecords.vue'
import AppointmentHistory from '@/components/AppointmentHistory.vue'
import ExaminationReports from '@/components/ExaminationReports.vue'
import BlockchainRecords from '@/components/BlockchainRecords.vue'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const patientId = computed(() => route.params.id as string)
const patientInfo = ref({
  name: '',
  gender: 'M',
  birthdate: '',
  id_card: '',
  phone: '',
  email: '',
  address: '',
  insurance_number: ''
})
const activeTab = ref('records')
const loading = ref(true)

const calculateAge = (birthdate: string) => {
  if (!birthdate) return 0
  return dayjs().diff(dayjs(birthdate), 'year')
}

const fetchPatientInfo = async () => {
  try {
    loading.value = true
    const response = await api.get(`/patients/${patientId.value}`)
    patientInfo.value = response.data
  } catch (error) {
    ElMessage.error('获取患者信息失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.push('/patients')
}

const editPatient = () => {
  // 编辑患者信息的逻辑
  router.push(`/patients/${patientId.value}/edit`)
}

onMounted(() => {
  fetchPatientInfo()
})
</script>

<style scoped>
.patient-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.patient-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 10px;
}

.info-label {
  width: 100px;
  color: #606266;
  font-weight: 500;
}

.info-value {
  flex: 1;
  color: #303133;
}
</style>