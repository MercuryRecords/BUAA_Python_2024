<script setup lang="ts" name="Home">
import {onMounted, onUnmounted} from "vue";

onMounted(()=>{
  console.log("首页组件挂载了")
})

onUnmounted(()=>{
  console.log("首页组件卸载了")
})
</script>

<template>
  <h2>welcome to our shared platform!</h2>
</template>

<style scoped>

</style>