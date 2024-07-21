<script setup lang="ts" name="App">
import {RouterView, RouterLink} from 'vue-router'
import axios from 'axios'
import {reactive, ref} from "vue"
import API from "@/plugins/axios"

const username = ref('')
const password = ref('')
const usertype = ref('')
const data = reactive(
    {
      username: '',
      password: '',
      usertype: '',
    }
)
const returnValue = reactive(
    {
      code: '',
      message: '',
    }
)

function userRegister() {
  data.username = username.value
  data.password = password.value
  data.usertype = usertype.value
  console.log(data)
  API.post('/user_register/', data,
      {
        // headers: {
        //   'Content-Type': 'application/x-www-form-urlencoded'
        // }
      }).then(
      function (response) {
        returnValue.code = response.data.code
        returnValue.message = response.data.message
        console.log("successfully registered")
        alert(returnValue.message)
      })
      .catch(
          function () {
            console.log("error!")
          })
  username.value = ''
  password.value = ''
  usertype.value = ''
}
</script>

<template>
  <div>
    <div>
      <input type="text" class="username" v-model="username" placeholder="请输入用户名">
    </div>
    <div>
      <input type="password" class="password" v-model="password" placeholder="请输入密码">
    </div>
    <div>
      <input type="text" class="usertype" v-model="usertype" placeholder="请输入用户类型">
    </div>
    <button @click="userRegister">注册</button>
  </div>
</template>

<style scoped>

</style>
