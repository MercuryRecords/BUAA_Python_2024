<script setup lang="ts" name="App">
import {RouterView, RouterLink} from 'vue-router'
import axios from 'axios'
import {ref} from "vue";

const data = ref('')

function sendMessage() {
  console.log('hello,world')
  axios.post('/api/register/',data).then(
      function(){
        console.log("successfully registered")
      })
      .catch(
          function(){
            console.log("error!")
          })
  data.value = ''

}
</script>

<template>
  <div class="navigate">
    <!--    <RouterLink to="/home">首页</RouterLink>-->
    <input v-model="data" type="text">
    <button @click="sendMessage">sendMessage</button>
  </div>

  <div class="main-content">
    <RouterView></RouterView>
  </div>
</template>

<style scoped>

</style>
