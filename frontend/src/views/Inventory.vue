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
              @keyup.enter="searchDrugs"
            />
            <el-button type="primary" @click="handleAdd">新增药品</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="drugs" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="药品名称" width="150" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="specification" label="规格" width="120" />
        <el-table-column prop="manufacturer" label="生产厂家" width="150" />
        <el-table-column prop="batch_number" label="批号" width="120" />
        <el-table-column prop="stock" label="库存数量" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="unit_price" label="单价" width="100">
          <template #default="{ row }">¥{{ row.unit_price }}</template>
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

    <!-- 新增/编辑药品对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      @close="resetForm"
    >
      <el-form 
        ref="drugFormRef" 
        :model="drugForm" 
        :rules="drugFormRules" 
        label-width="100px"
      >
        <el-form-item label="药品名称" prop="name">
          <el-input v-model="drugForm.name" />
        </el-form-item>
        
        <el-form-item label="通用名" prop="generic_name">
          <el-input v-model="drugForm.generic_name" />
        </el-form-item>
        
        <el-form-item label="规格" prop="specification">
          <el-input v-model="drugForm.specification" />
        </el-form-item>
        
        <el-form-item label="生产厂家" prop="manufacturer">
          <el-input v-model="drugForm.manufacturer" />
        </el-form-item>
        
        <el-form-item label="批号" prop="batch_number">
          <el-input v-model="drugForm.batch_number" />
        </el-form-item>
        
        <el-form-item label="生产日期" prop="production_date">
          <el-date-picker
            v-model="drugForm.production_date"
            type="date"
            placeholder="请选择生产日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="有效期至" prop="expiry_date">
          <el-date-picker
            v-model="drugForm.expiry_date"
            type="date"
            placeholder="请选择有效期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="分类" prop="category">
          <el-select v-model="drugForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="药品" value="DRUG" />
            <el-option label="医疗器械" value="MEDICAL_DEVICE" />
            <el-option label="消耗品" value="CONSUMABLE" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="单位" prop="unit">
          <el-input v-model="drugForm.unit" placeholder="如：盒、片、支等" />
        </el-form-item>
        
        <el-form-item label="单价" prop="unit_price">
          <el-input-number 
            v-model="drugForm.unit_price" 
            :min="0" 
            :step="0.01" 
            controls-position="right" 
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="库存数量" prop="stock">
          <el-input-number 
            v-model="drugForm.stock" 
            :min="0" 
            controls-position="right" 
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="最低库存" prop="min_stock">
          <el-input-number 
            v-model="drugForm.min_stock" 
            :min="0" 
            controls-position="right" 
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="最高库存" prop="max_stock">
          <el-input-number 
            v-model="drugForm.max_stock" 
            :min="0" 
            controls-position="right" 
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="供应商" prop="supplier">
          <el-input v-model="drugForm.supplier" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDrugForm" :loading="submitLoading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus'
import api from '@/utils/api'

interface Drug {
  id: string
  name: string
  generic_name: string
  specification: string
  manufacturer: string
  batch_number: string
  production_date: string
  expiry_date: string
  category: string
  unit: string
  unit_price: number
  stock: number
  min_stock: number
  max_stock: number
  supplier: string
  blockchain_trace_id: string
  is_active: boolean
  created_at: string
  updated_at: string
}

const loading = ref(false)
const submitLoading = ref(false)
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增药品')
const isEdit = ref(false)
const editDrugId = ref('')

const drugs = ref<Drug[]>([])
const drugFormRef = ref<FormInstance>()

const drugForm = reactive({
  name: '',
  generic_name: '',
  specification: '',
  manufacturer: '',
  batch_number: '',
  production_date: '',
  expiry_date: '',
  category: '',
  unit: '',
  unit_price: 0,
  stock: 0,
  min_stock: 10,
  max_stock: 1000,
  supplier: ''
})

const drugFormRules = {
  name: [{ required: true, message: '请输入药品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }]
}

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const handleAdd = () => {
  dialogTitle.value = '新增药品'
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (row: Drug) => {
  dialogTitle.value = '编辑药品'
  isEdit.value = true
  editDrugId.value = row.id
  
  // 填充表单数据
  drugForm.name = row.name
  drugForm.generic_name = row.generic_name
  drugForm.specification = row.specification
  drugForm.manufacturer = row.manufacturer
  drugForm.batch_number = row.batch_number
  drugForm.production_date = row.production_date
  drugForm.expiry_date = row.expiry_date
  drugForm.category = row.category
  drugForm.unit = row.unit
  drugForm.unit_price = row.unit_price
  drugForm.stock = row.stock
  drugForm.min_stock = row.min_stock
  drugForm.max_stock = row.max_stock
  drugForm.supplier = row.supplier
  
  dialogVisible.value = true
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
  ).then(async () => {
    try {
      await api.delete(`/drugs/${row.id}`)
      ElMessage.success('删除成功')
      fetchData() // 重新加载数据
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

const searchDrugs = () => {
  pagination.currentPage = 1
  fetchData()
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  fetchData()
}

const resetForm = () => {
  drugForm.name = ''
  drugForm.generic_name = ''
  drugForm.specification = ''
  drugForm.manufacturer = ''
  drugForm.batch_number = ''
  drugForm.production_date = ''
  drugForm.expiry_date = ''
  drugForm.category = ''
  drugForm.unit = ''
  drugForm.unit_price = 0
  drugForm.stock = 0
  drugForm.min_stock = 10
  drugForm.max_stock = 1000
  drugForm.supplier = ''
}

const submitDrugForm = async () => {
  if (!drugFormRef.value) return
  
  try {
    await drugFormRef.value.validate()
    submitLoading.value = true
    
    if (isEdit.value) {
      // 编辑药品
      await api.put(`/drugs/${editDrugId.value}`, drugForm)
      ElMessage.success('药品更新成功')
    } else {
      // 新增药品
      await api.post('/drugs', drugForm)
      ElMessage.success('药品添加成功')
    }
    
    dialogVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(isEdit.value ? '药品更新失败' : '药品添加失败')
  } finally {
    submitLoading.value = false
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const response = await api.get('/drugs', {
      params: {
        page: pagination.currentPage,
        per_page: pagination.pageSize,
        keyword: searchKeyword.value
      }
    })
    drugs.value = response.data.items
    pagination.total = response.data.total
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