<template>
  <div class="personal-center">
    <el-card class="info-card">
      <template #header>
        <div class="card-header">
          <span>查看您的信息</span>
        </div>
      </template>
      <div class="info-content">
        <div class="avatar-section">
          <el-avatar :size="100" :src="userInfo.avatar"></el-avatar>
          <h2>{{ userInfo.name }}</h2>
          <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :on-change="handleAvatarChange"
              :auto-upload="false"
              :accept="'.jpg,.png'"
          >
            <el-link type="primary" class="edit-avatar">修改头像</el-link>
          </el-upload>
        </div>
        <div class="user-details">
          <el-row class="info-row" v-for="(value, key) in userInfoDisplay" :key="key">
            <el-col :span="8" class="info-label">
              <i :class="iconMap[key]"></i>
              {{ labelMap[key] }}
            </el-col>
            <el-col :span="16" class="info-value">{{ value }}</el-col>
          </el-row>
        </div>
      </div>
      <div class="card-footer">
        <el-link type="danger" class="footer-link">* 若您的个人信息有误，请联系系统管理员</el-link>
        <div>
          <el-link type="primary" class="footer-link">修改密码</el-link>
          <el-link type="primary" class="footer-link">退出登录</el-link>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue'
import {ElMessage} from 'element-plus'

const userInfo = reactive({
  name: 'July',
  avatar: 'path_to_avatar_image',
  studentId: '22371500',
  role: '学生',
  email: '22371500@buaa.edu.cn',
  createdAt: '2024-02-19',
  currentCourse: '2024春-操作系统'
})

const userInfoDisplay = {
  studentId: userInfo.studentId,
  role: userInfo.role,
  email: userInfo.email,
  createdAt: userInfo.createdAt,
  currentCourse: userInfo.currentCourse
}

const iconMap = {
  studentId: 'el-icon-user',
  role: 'el-icon-s-custom',
  email: 'el-icon-message',
  createdAt: 'el-icon-date',
  currentCourse: 'el-icon-reading'
}

const labelMap = {
  studentId: '学工号',
  role: '用户身份',
  email: '个人邮箱',
  createdAt: '创建时间',
  currentCourse: '当前课程'
}

const handleAvatarChange = (file) => {
  const isJPG = file.raw.type === 'image/jpeg'
  const isPNG = file.raw.type === 'image/png'
  const isLt2M = file.raw.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像图片只能是 JPG 或 PNG 格式!')
    return
  }
  if (!isLt2M) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return
  }

  // 创建一个 FileReader 对象
  const reader = new FileReader()
  reader.readAsDataURL(file.raw)
  reader.onload = (e) => {
    // 更新头像
    userInfo.avatar = e.target.result
    ElMessage.success('头像更新成功')
  }
}
</script>

<style scoped>
.personal-center {
  padding: 20px;
}

.info-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-weight: bold;
}

.info-content {
  display: flex;
  align-items: flex-start;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 40px;
}

.avatar-section h2 {
  margin: 10px 0;
}

.edit-avatar {
  margin-top: 5px;
}

.user-details {
  flex-grow: 1;
}

.info-row {
  margin-bottom: 15px;
}

.info-label {
  color: #606266;
}

.info-label i {
  margin-right: 5px;
}

.info-value {
  color: #303133;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.footer-link {
  margin-left: 15px;
}

.footer-link:first-child {
  margin-left: 0;
}
</style>