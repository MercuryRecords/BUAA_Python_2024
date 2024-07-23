<script lang="ts" setup>
import {reactive, ref} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
import router from "@/router";
import API from '@/plugins/axios';

const ruleFormRef = ref<FormInstance>()

const data = reactive(
    {
      username: '',
      password: '',
      usertype: '',
    }
)

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
  name: [{validator: validateName, trigger: 'blur'}],
  pass: [{validator: validatePass, trigger: 'blur'}],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      data.username = ruleForm.name
      data.password = ruleForm.pass
      data.usertype = ruleForm.mode
      //TODO 告知后端 并由后端检查 获得返回值
      API.post('/user_login', data,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }).then(
          function (response) {
            console.log("successfully login!")
            if (response.data.code === 200) {
              ElMessage.success(response.data.message);
              console.log(router)
              router.push({
                    path: '/home',
                    query: {
                      username: data.username //logincard->/home，将username传给home,home的url带有username
                    },
                  }); //传入这个人的参数，它的数据库
            } else {
              console.log(response.data.code)
              ElMessage.error("Login"+response.data.message)
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


const jumpToRegister = (formEl: FormInstance | undefined) => {
  router.push('/register');
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
      background-color:white
  >
    <el-form-item label="Name" prop="name">
      <el-input v-model.number="ruleForm.name"/>
    </el-form-item>
    <el-form-item label="Password" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off"/>
    </el-form-item>
    <el-form-item label="Mode">
      <el-radio-group v-model="ruleForm.mode">
        <el-radio value=0>Admin</el-radio>
        <el-radio value=1>User</el-radio>
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