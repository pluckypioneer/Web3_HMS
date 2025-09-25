<template>
  <div class="inventory-page">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>药品库存</span>
          <div class="header-actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索药品..."
              style="width: 200px; margin-right: 10px"
              clearable
            />
            <el-button type="primary" @click="handleAdd">新增药品</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="drugs" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="药品ID" width="100" />
        <el-table-column prop="name" label="药品名称" width="150" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="specification" label="规格" width="120" />
        <el-table-column prop="manufacturer" label="生产厂家" width="150" />
        <el-table-column prop="stock" label="库存数量" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="price" label="单价" width="100">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
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

const drugs = ref([
  {
    id: 'DR001',
    name: '阿莫西林胶囊',
    category: '抗生素',
    specification: '0.25g*24粒',
    manufacturer: '华北制药',
    stock: 100,
    unit: '盒',
    price: 25.8
  },
  {
    id: 'DR002',
    name: '布洛芬片',
    category: '解热镇痛',
    specification: '0.1g*24片',
    manufacturer: '华润三九',
    stock: 50,
    unit: '盒',
    price: 15.6
  }
])

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const handleAdd = () => {
  ElMessage.info('跳转到新增药品页面')
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑药品 ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    `确定要删除药品 ${row.name} 吗？`,
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
    // const response = await api.get('/drugs', {
    //   params: {
    //     page: pagination.currentPage,
    //     size: pagination.pageSize,
    //     keyword: searchKeyword.value
    //   }
    // })
    // drugs.value = response.data.items
    // pagination.total = response.data.total
  } catch (error: any) {
    ElMessage.error(error.message || '获取药品列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.inventory-page {
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