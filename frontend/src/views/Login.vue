<script setup lang="ts">
import LoginCard from "@/components/Base/LoginCard.vue";
</script>

<template>
  <div class="container">
    <LoginCard></LoginCard>
  </div>
</template>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box; /* 确保padding不会增加容器的总宽度或高度 */
  width: auto;
}


</style>
