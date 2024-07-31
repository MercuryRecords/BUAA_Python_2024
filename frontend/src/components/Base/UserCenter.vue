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
          <el-link type="primary" class="footer-link" @click="showChangePasswordDialog">修改密码</el-link>
          <el-link type="primary" class="footer-link" @click="handleLogout">退出登录</el-link>
        </div>
      </div>
    </el-card>
    <el-dialog
        title="修改密码"
        v-model="changePasswordDialogVisible"
        width="30%"
        :close-on-click-modal="false"
    >
      <el-form :model="passwordForm" label-width="80px">
        <el-form-item label="旧密码">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="handleChangePassword">确认修改</el-button>
          <el-button @click="changePasswordDialogVisible = false">取消修改</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import API from "@/plugins/axios";
import {useRouter} from 'vue-router';

const router = useRouter();
const data = defineProps(['username'])
const userInfo = reactive({
  name: data.username,
  avatar: 'path_to_avatar_image',
  studentId: '22371500',
  role: 'User',
  email: '22371500@buaa.edu.cn',
  createdAt: '2024-02-19',
  currentCourse: '2024春-操作系统'
})

const userInfoDisplay = {
  studentId: data.username,
  role: userInfo.role,
}

const iconMap = {
  studentId: 'el-icon-user',
  role: 'el-icon-s-custom',
}

const labelMap = {
  studentId: '用户名',
  role: '用户身份',
}

const handleAvatarChange = (file: any) => {
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

  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('avatar', file.raw)

  API.post('/edit_avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    if (response.data.code === 200) {
      // 创建一个 FileReader 对象来读取文件
      const reader = new FileReader()
      reader.readAsDataURL(file.raw)
      reader.onload = (e) => {
        if (e.target && e.target.result) {
          // Update the avatar
          userInfo.avatar = e.target.result as string;
          ElMessage.success('头像更新成功');
          console.log(file.raw);
        } else {
          ElMessage.error('头像加载失败');
        }
      }
    } else {
      ElMessage.error('头像更新失败: ' + response.data.message)
    }
  }).catch(error => {
    console.error('Error:', error)
    ElMessage.error('头像更新失败，请稍后重试')
  })
}

onMounted(async () => showPicture());

function showPicture() {
  API.post('/get_avatar', {
    username: data.username
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(response => {
    if (response.data.code === 200) {
      userInfo.avatar = response.data.avatar
      console.log(response.data.message)
    } else {
      console.log('Failed to fetch avatar:', response.data.message)
      // 设置默认头像
      userInfo.avatar = 'path_to_default_avatar_image'
    }
  }).catch(error => {
    console.error('Error fetching avatar:', error)
    // 设置默认头像
    userInfo.avatar = 'path_to_default_avatar_image'
  })
}

const handleLogout = () => {
  // 这里可以添加退出登录的逻辑，比如清除本地存储的用户信息、token等
  API.post('/user_logout',
      {
        username: data.username,
      }, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(
      function (response) {
        if (response.data.code === 200) {
          console.log('退！')
          ElMessage.success('退出成功！')
          setTimeout(() => {
            router.push('/login')
          }, 1000); // 延迟1000毫秒（1秒）
        } else {
          console.log('Failed to logout:', response.data.message)
        }
      }
  ).catch(
      function () {
        console.log('error')
      }
  )
}

const changePasswordDialogVisible = ref(false)
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showChangePasswordDialog = () => {
  changePasswordDialogVisible.value = true
}

const handleChangePassword = () => {
  // 这里添加修改密码的逻辑
  // 可以进行表单验证、API调用等
  console.log('修改密码', passwordForm)
  // 示例：
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('新密码和确认密码不一致')
    return
  }
  // 调用API修改密码
  API.post('/user_change_password', {
    username: data.username,
    password: passwordForm.oldPassword,
    new_password: passwordForm.newPassword,
    usertype: '1'
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => {
    if (response.data.code === 200) {
      ElMessage.success('密码修改成功')
      changePasswordDialogVisible.value = false
    } else {
      ElMessage.error('密码修改失败: ' + response.data.message)
    }
  }).catch(error => {
    console.error('Error:', error)
    ElMessage.error('密码修改失败，请稍后重试')
  })
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>