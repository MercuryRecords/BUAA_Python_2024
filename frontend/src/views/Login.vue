<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="logo">Liberal Shared Platform</h1>
      <el-form
          ref="ruleFormRef"
          :model="ruleForm"
          :rules="rules"
          class="login-form"
      >
        <el-form-item prop="name">
          <el-input
              v-model="ruleForm.name"
              placeholder="用户名"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="pass">
          <el-input
              v-model="ruleForm.pass"
              :type="passwordVisible ? 'text' : 'password'"
              placeholder="密码"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
            <template #suffix>
              <el-icon class="password-icon" @click="togglePasswordVisibility">
                <View v-if="passwordVisible" />
                <Hide v-else />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="submitForm(ruleFormRef)">
            登录
          </el-button>
        </el-form-item>
        <el-form-item class="login-options">
          <el-radio-group v-model="ruleForm.mode">
            <el-radio :label="0">管理员</el-radio>
            <el-radio :label="1" style="margin-left: 70px">用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <div class="register-link">
          <a @click="jumpToRegister">注册账号</a>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'
import router from "@/router";
import API from '@/plugins/axios';

const ruleFormRef = ref<FormInstance>()
const passwordVisible = ref(false)

const data = reactive({
  username: '',
  password: '',
  usertype: 1,
})

const ruleForm = reactive({
  name: '',
  pass: '',
  mode: 1, // 默认选中用户模式
})

const rules = reactive<FormRules<typeof ruleForm>>({
  name: [{ required: true, message: '请输入用户名', trigger: 'none' }],
  pass: [{ required: true, message: '请输入密码', trigger: 'none' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      data.username = ruleForm.name
      data.password = ruleForm.pass
      data.usertype = ruleForm.mode
      console.log(data)
      API.post('/user_login', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(function (response) {
        console.log("successfully login!")
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
          router.push({
            path: '/home',
            query: {
              username: data.username,
              mode: data.usertype
            },
          });
        } else {
          console.log(response.data.code)
          ElMessage.error("Login" + response.data.message)
        }
      }).catch(function () {
        console.log("error!")
      })
    } else {
      console.log('error submit!')
    }
  })
}

const jumpToRegister = () => {
  router.push('/register');
}

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
  background-position: center;
}

.login-box {
  width: 400px;
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.logo {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.login-form :deep(.el-input__prefix) {
  display: flex;
  align-items: center;
  color: #909399;
}

.login-form :deep(.el-input__prefix-inner) {
  display: flex;
}

.login-form :deep(.el-input__icon) {
  height: auto;
}

.login-form :deep(.password-icon) {
  cursor: pointer;
}

/* 新增：当鼠标悬停在密码图标上时，显示为点击样式 */
.login-form :deep(.password-icon:hover) {
  cursor: pointer;
}

.login-button {
  width: 100%;
  border-radius: 20px;
}

.login-form :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 20px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.register-link {
  text-align: center;
  margin-top: 15px;
}

.register-link a {
  color: #409EFF;
  text-decoration: none;
  cursor: pointer;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>