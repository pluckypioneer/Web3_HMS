<template>
  <div class="patients-page">
    <el-card class="page-card">
      <template #header>
        <div class="flex-between">
          <h1>患者列表</h1>
          <el-button type="primary" @click="addPatient">
            <el-icon><Plus /></el-icon>
            新增患者
          </el-button>
        </div>
      </template>

      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索">
          <el-input 
            v-model="searchForm.keyword" 
            placeholder="请输入姓名、身份证号或医保卡号" 
            clearable
            @keyup.enter="searchPatients"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchPatients">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table 
        :data="patients" 
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="scope">
            {{ scope.row.gender === 'M' ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="birth_date" label="出生日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.birth_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="phone" label="联系电话" width="120" />
        <el-table-column prop="insurance_number" label="医保卡号" width="180" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewPatient(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="editPatient(scope.row.id)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deletePatient(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'
import dayjs from 'dayjs'

interface Patient {
  id: string
  name: string
  gender: string
  birth_date: string
  id_card: string
  phone: string
  insurance_number: string
  created_at: string
}

const router = useRouter()
const loading = ref(false)
const patients = ref<Patient[]>([])

const searchForm = reactive({
  keyword: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

// 获取患者列表
const fetchPatients = async () => {
  try {
    loading.value = true
    const response = await api.get('/patients', {
      params: {
        page: pagination.currentPage,
        per_page: pagination.pageSize,
        search: searchForm.keyword || undefined
      }
    })
    
    patients.value = response.data.patients
    pagination.total = response.data.total
  } catch (error) {
    ElMessage.error('获取患者列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索患者
const searchPatients = () => {
  pagination.currentPage = 1
  fetchPatients()
}

// 重置搜索
const resetSearch = () => {
  searchForm.keyword = ''
  pagination.currentPage = 1
  fetchPatients()
}

// 分页相关
const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  fetchPatients()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  fetchPatients()
}

// 格式化日期
const formatDate = (date: string) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD')
}

// 格式化时间
const formatDateTime = (date: string) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 路由跳转
const addPatient = () => {
  router.push('/patients/add')
}

const viewPatient = (id: string) => {
  router.push(`/patients/${id}`)
}

const editPatient = (id: string) => {
  router.push(`/patients/${id}/edit`)
}

const deletePatient = (id: string) => {
  ElMessageBox.confirm('确定要删除该患者吗？此操作不可恢复', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.delete(`/patients/${id}`)
      ElMessage.success('删除成功')
      fetchPatients()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

onMounted(() => {
  fetchPatients()
})
</script>

<style scoped>
.patients-page {
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