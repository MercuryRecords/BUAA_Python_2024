<template>
  <el-form
      ref="ruleFormRef"
      style="max-width: 600px"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
  >
    <el-form-item label="Name" prop="name">
      <el-input v-model.number="ruleForm.name" />
    </el-form-item>
    <el-form-item label="Password" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item label="Mode">
      <el-radio-group v-model="ruleForm.mode">
        <el-radio value=0>User</el-radio>
        <el-radio value=1>Admin</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        Login
      </el-button>
      <el-button @click="jumpToRegister(ruleFormRef)">Register</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import router from "@/router";

const ruleFormRef = ref<FormInstance>()

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the password'))
  } else {
    if (ruleForm.pass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}
const validateName = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the name'))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  name: '',
  pass: '',
  mode: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
  name: [{ validator: validateName, trigger: 'blur' }],
  pass: [{ validator: validatePass, trigger: 'blur' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!', ruleForm.name, ruleForm.mode)
      //TODO 告知后端 并由后端检查 获得返回值

    } else {
      console.log('error submit!')
    }
  })
}


const jumpToRegister = (formEl: FormInstance | undefined) => {
  router.push('/register');
}
</script>