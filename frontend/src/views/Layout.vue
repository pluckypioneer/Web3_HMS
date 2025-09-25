<template>
  <div class="app-layout">
    <div class="sidebar">
      <Sidebar />
    </div>
    <div class="main-content">
      <Navbar />
      <div class="page-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/Layout/Sidebar.vue'
import Navbar from '@/components/Layout/Navbar.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  background-color: #fff;
  border-right: 1px solid #e5e7eb;
  height: 100%;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
}
</style>