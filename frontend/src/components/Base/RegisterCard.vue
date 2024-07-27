<script lang="ts" setup>
import {reactive, ref} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
import router from "@/router";
import API from "@/plugins/axios"

const ruleFormRef = ref<FormInstance>()

const data = reactive(
    {
      username: '',
      password: '',
      usertype: '',
    }
) //匹配后端接口

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
  pass: '',
  checkPass: '',
  name: '',
  mode: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
  pass: [{validator: validatePass, trigger: 'blur'}],
  checkPass: [{validator: validatePass2, trigger: 'blur'}],
  name: [{validator: checkName, trigger: 'blur'}],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      data.username = ruleForm.name
      data.password = ruleForm.pass
      data.usertype = ruleForm.mode
      // TODO 向后端返回注册信息 根据成功与否执行以下操作：
      API.post('/user_register', data,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }).then(
          function (response) {
            console.log("successfully registered")
            if (response.data.code === 200) {
              ElMessage.success(response.data.message);
              console.log(router)
              router.push('/')
            } else {
              console.log(response.data.code)
              ElMessage.error(response.data.message)
            }
          })
          .catch(
              function () {
                console.log("error!")
              })
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

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
      <el-input v-model="ruleForm.name"/>
    </el-form-item>
    <el-form-item label="Password" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off"/>
    </el-form-item>
    <el-form-item label="Confirm" prop="checkPass">
      <el-input
          v-model="ruleForm.checkPass"
          type="password"
          autocomplete="off"
      />
    </el-form-item>
    <el-form-item label="Mode">
      <el-radio-group v-model="ruleForm.mode">
        <el-radio value=0>Admin</el-radio>
        <el-radio value=1>User</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        Submit
      </el-button>
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

