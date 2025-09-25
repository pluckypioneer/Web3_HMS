<template>
  <div class="patient-detail-page">
    <h1>患者详情</h1>
    <!-- 后续添加患者信息、关联病历等功能 -->
  </div>
</template>

<script setup lang="ts">
// 后续逻辑（可接收路由参数，如患者ID）
import { useRoute } from 'vue-router';
const route = useRoute();
const patientId = route.params.id; // 示例：获取路由参数
</script>

<style scoped>
.patient-detail-page {
  padding: 20px;
}
</style>