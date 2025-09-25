<template>
  <div class="statistics-page">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>统计分析</span>
          <div class="header-actions">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              style="width: 240px; margin-right: 10px"
            />
            <el-button type="primary" @click="fetchData">查询</el-button>
          </div>
        </div>
      </template>
      
      <div class="charts-container">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <span>就诊人数统计</span>
              </template>
              <div class="chart-wrapper">
                <v-chart class="chart" :option="visitChartOption" autoresize />
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <span>药品销售统计</span>
              </template>
              <div class="chart-wrapper">
                <v-chart class="chart" :option="drugChartOption" autoresize />
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <span>科室收入统计</span>
              </template>
              <div class="chart-wrapper">
                <v-chart class="chart" :option="departmentChartOption" autoresize />
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <span>患者性别分布</span>
              </template>
              <div class="chart-wrapper">
                <v-chart class="chart" :option="genderChartOption" autoresize />
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 确保 echarts 已正确初始化
import * as echarts from 'echarts/core'

echarts.use([
  CanvasRenderer,
  BarChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent
])

// 在组件挂载时获取初始数据
onMounted(() => {
  fetchData()
})

const dateRange = ref<[Date, Date]>([new Date('2023-05-01'), new Date('2023-05-31')])

const visitChartOption = reactive({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [120, 200, 150, 80, 70, 110, 130],
      type: 'bar'
    }
  ]
})

const drugChartOption = reactive({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%'
  },
  series: [
    {
      name: '药品销售',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      data: [
        { value: 1048, name: '阿莫西林' },
        { value: 735, name: '布洛芬' },
        { value: 580, name: '头孢' },
        { value: 484, name: '奥美拉唑' },
        { value: 300, name: '其他' }
      ]
    }
  ]
})

const departmentChartOption = reactive({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: ['内科', '外科', '儿科', '妇科', '眼科', '耳鼻喉科']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [12000, 18000, 8000, 10000, 6000, 4000],
      type: 'bar'
    }
  ]
})

const genderChartOption = reactive({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%'
  },
  series: [
    {
      name: '性别分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      data: [
        { value: 400, name: '男' },
        { value: 300, name: '女' }
      ]
    }
  ]
})

const fetchData = async () => {
  try {
    // 模拟 API 调用
    // const response = await api.get('/statistics', {
    //   params: {
    //     startDate: dateRange.value[0],
    //     endDate: dateRange.value[1]
    //   }
    // })
    // 更新图表数据
    console.log('Fetching data for date range:', dateRange.value)
  } catch (error) {
    console.error('Error fetching statistics data:', error)
  }
}
</script>

<style scoped>
.statistics-page {
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

.charts-container {
  margin-top: 20px;
}

.chart-card {
  height: 400px;
}

.chart-wrapper {
  height: 300px;
}

.chart {
  height: 100%;
  width: 100%;
}
</style>