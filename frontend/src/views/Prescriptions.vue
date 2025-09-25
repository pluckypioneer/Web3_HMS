<template>
  <div class="prescriptions-page">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>处方管理</span>
          <div class="header-actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索处方..."
              style="width: 200px; margin-right: 10px"
              clearable
            />
            <el-button type="primary" @click="handleAdd">新增处方</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="prescriptions" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="处方ID" width="100" />
        <el-table-column prop="patientName" label="患者姓名" width="120" />
        <el-table-column prop="doctorName" label="开方医生" width="120" />
        <el-table-column prop="createdAt" label="开方时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">查看</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const searchKeyword = ref('')

const prescriptions = ref([
  {
    id: 'RX001',
    patientName: '张三',
    doctorName: '李医生',
    createdAt: '2023-05-01 10:30:00',
    status: 'active'
  },
  {
    id: 'RX002',
    patientName: '李四',
    doctorName: '王医生',
    createdAt: '2023-05-02 14:20:00',
    status: 'completed'
  }
])

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const getStatusType = (status: string) => {
  switch (status) {
    case 'active': return 'primary'
    case 'completed': return 'success'
    case 'cancelled': return 'danger'
    default: return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active': return '有效'
    case 'completed': return '已完成'
    case 'cancelled': return '已取消'
    default: return '未知'
  }
}

const handleAdd = () => {
  ElMessage.info('跳转到新增处方页面')
}

const handleView = (row: any) => {
  ElMessage.info(`查看处方 ${row.id}`)
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑处方 ${row.id}`)
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    `确定要删除处方 ${row.id} 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('删除成功')
  }).catch(() => {
    // 用户取消删除
  })
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  fetchData()
}

const fetchData = async () => {
  loading.value = true
  try {
    // 模拟 API 调用
    // const response = await api.get('/prescriptions', {
    //   params: {
    //     page: pagination.currentPage,
    //     size: pagination.pageSize,
    //     keyword: searchKeyword.value
    //   }
    // })
    // prescriptions.value = response.data.items
    // pagination.total = response.data.total
  } catch (error: any) {
    ElMessage.error(error.message || '获取处方列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.prescriptions-page {
  padding: 20px;
}

.page-card {
  max-width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>