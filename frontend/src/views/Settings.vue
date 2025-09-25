<template>
  <div class="settings-page">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>系统设置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form :model="basicSettings" label-width="120px" class="settings-form">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" />
            </el-form-item>
            
            <el-form-item label="默认主题">
              <el-select v-model="basicSettings.theme">
                <el-option label="默认主题" value="default" />
                <el-option label="暗色主题" value="dark" />
                <el-option label="蓝色主题" value="blue" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="语言">
              <el-select v-model="basicSettings.language">
                <el-option label="中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="通知设置" name="notification">
          <el-form :model="notificationSettings" label-width="120px" class="settings-form">
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationSettings.emailEnabled" />
            </el-form-item>
            
            <el-form-item label="短信通知">
              <el-switch v-model="notificationSettings.smsEnabled" />
            </el-form-item>
            
            <el-form-item label="微信通知">
              <el-switch v-model="notificationSettings.wechatEnabled" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="安全设置" name="security">
          <el-form :model="securitySettings" label-width="120px" class="settings-form">
            <el-form-item label="密码策略">
              <el-select v-model="securitySettings.passwordPolicy">
                <el-option label="简单（至少6位）" value="simple" />
                <el-option label="中等（字母+数字）" value="medium" />
                <el-option label="复杂（字母+数字+特殊字符）" value="complex" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="会话超时">
              <el-select v-model="securitySettings.sessionTimeout">
                <el-option label="30分钟" :value="30" />
                <el-option label="1小时" :value="60" />
                <el-option label="2小时" :value="120" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSecuritySettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('basic')

const basicSettings = reactive({
  systemName: 'Web3 医院管理系统',
  theme: 'default',
  language: 'zh-CN'
})

const notificationSettings = reactive({
  emailEnabled: true,
  smsEnabled: true,
  wechatEnabled: false
})

const securitySettings = reactive({
  passwordPolicy: 'medium',
  sessionTimeout: 60
})

const saveBasicSettings = () => {
  ElMessage.success('基本设置已保存')
  // 这里应该调用 API 保存设置
}

const saveNotificationSettings = () => {
  ElMessage.success('通知设置已保存')
  // 这里应该调用 API 保存设置
}

const saveSecuritySettings = () => {
  ElMessage.success('安全设置已保存')
  // 这里应该调用 API 保存设置
}
</script>

<style scoped>
.settings-page {
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

.settings-form {
  max-width: 600px;
  margin-top: 20px;
}
</style>