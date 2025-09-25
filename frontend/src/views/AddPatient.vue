<template>
  <div class="add-patient-page">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>新增患者</span>
          <el-button @click="router.back()">返回</el-button>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="patientForm"
        :rules="formRules"
        label-width="120px"
        class="patient-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="patientForm.name" placeholder="请输入患者姓名" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="patientForm.idCard" placeholder="请输入身份证号" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="patientForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birthDate">
              <el-date-picker
                v-model="patientForm.birthDate"
                type="date"
                placeholder="请选择出生日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="patientForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="patientForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          
          <el-col :span="24">
            <el-form-item label="地址" prop="address">
              <el-input
                v-model="patientForm.address"
                type="textarea"
                placeholder="请输入详细地址"
                :rows="2"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="24">
            <el-form-item label="过敏史" prop="allergies">
              <el-input
                v-model="patientForm.allergies"
                type="textarea"
                placeholder="请输入患者过敏史，没有请填写'无'"
                :rows="2"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="24">
            <el-form-item label="既往病史" prop="medicalHistory">
              <el-input
                v-model="patientForm.medicalHistory"
                type="textarea"
                placeholder="请输入患者既往病史"
                :rows="2"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">
            提交
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const patientForm = reactive({
  name: '',
  idCard: '',
  gender: '',
  birthDate: '',
  phone: '',
  email: '',
  address: '',
  allergies: '',
  medicalHistory: ''
})

const formRules = reactive<FormRules>({
  name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  idCard: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  birthDate: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
})

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 这里应该调用 API 提交数据
    // await api.post('/patients', patientForm)
    
    ElMessage.success('患者信息添加成功')
    router.push('/patients')
  } catch (error: any) {
    ElMessage.error(error.message || '提交失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formRef.value?.resetFields()
}
</script>

<style scoped>
.add-patient-page {
  padding: 20px;
}

.page-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.patient-form {
  margin-top: 20px;
}
</style>