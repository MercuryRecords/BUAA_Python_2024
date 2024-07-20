<script setup lang="js" name="App">
import {RouterView, RouterLink} from 'vue-router'
import axios from 'axios'
import {reactive, ref} from "vue"
import API from "@/plugins/axios"

const inputValue = ref('')
const data = reactive(
    {
      message: ''
    }
)

function sendMessage(inputValue) {
  console.log('hello,world')
  /*axios.post('/api/register/',data).then(
      function(){
        console.log("successfully registered")
      })
      .catch(
          function(){
            console.log("error!")
          })*/
  data.message = inputValue
  API.post('/message', data).then(
      function () {
        console.log("successfully registered")
      })
      .catch(
          function () {
            console.log("error!")
          })
  inputValue.value = ''
}
</script>

<template>
  <div class="navigate">
    <!--    <RouterLink to="/home">首页</RouterLink>-->
    <input v-model="inputValue" type="text">
    <button @click="sendMessage(inputValue)">sendMessage</button>
  </div>

  <div class="main-content">
    <RouterView></RouterView>
  </div>
</template>

<style scoped>

</style>
