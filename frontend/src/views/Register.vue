<template>
  <div class="register-container">
    <div class="register-box">
      <h1 class="logo">LOGO</h1>
      <el-form
          ref="ruleFormRef"
          :model="ruleForm"
          :rules="rules"
          class="register-form"
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
              type="password"
              placeholder="密码"
              show-password
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="checkPass">
          <el-input
              v-model="ruleForm.checkPass"
              type="password"
              placeholder="确认密码"
              show-password
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="register-options">
          <el-radio-group v-model="ruleForm.mode">
            <el-radio :label="0">管理员</el-radio>
            <el-radio :label="1" style="margin-left: 70px">用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="register-button" @click="submitForm(ruleFormRef)">
            注册
          </el-button>
        </el-form-item>
        <div class="login-link">
          <a @click="jumpToLogin">已有账号？立即登录</a>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import router from "@/router";
import API from "@/plugins/axios"

const ruleFormRef = ref<FormInstance>()

const data = reactive({
  username: '',
  password: '',
  usertype: 1,
})

const checkName = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入用户名'))
  } else {
    callback()
  }
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== ruleForm.pass) {
    callback(new Error("密码不一致！"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  name: '',
  pass: '',
  checkPass: '',
  mode: 1,
})

const rules = reactive<FormRules<typeof ruleForm>>({
  name: [{ validator: checkName, trigger: 'blur' }],
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      data.username = ruleForm.name
      data.password = ruleForm.pass
      data.usertype = ruleForm.mode
      API.post('/user_register', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(function (response) {
        console.log("successfully registered")
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
          router.push('/')
        } else {
          console.log(response.data.code)
          ElMessage.error(response.data.message)
        }
      }).catch(function () {
        console.log("error!")
      })
    } else {
      console.log('error submit!')
    }
  })
}

const jumpToLogin = () => {
  router.push('/');
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
  background-position: center;
}

.register-box {
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

.register-form :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 20px;
}

.register-form :deep(.el-input__inner) {
  height: 30px;
}

.register-button {
  width: 100%;
  border-radius: 20px;
}

.register-options {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.login-link {
  text-align: center;
  margin-top: 15px;
}

.login-link a {
  color: #409EFF;
  text-decoration: none;
  cursor: pointer;
}

.login-link a:hover {
  text-decoration: underline;
}

.register-form :deep(.el-input__prefix) {
  display: flex;
  align-items: center;
  color: #909399;
}

.register-form :deep(.el-input__prefix-inner) {
  display: flex;
}

.register-form :deep(.el-input__icon) {
  height: auto;
}
</style>