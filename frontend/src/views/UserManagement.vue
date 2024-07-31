<script setup lang="ts">
import { ref } from 'vue';
import NavigatorM from "@/components/Base/NavigatorM.vue";
import Users from "@/components/Base/Users.vue";

const isNavigatorOpen = ref(false);

const toggleNavigator = () => {
  isNavigatorOpen.value = !isNavigatorOpen.value;
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-button @click="toggleNavigator" class="menu-button">
          <i class="el-icon-menu"></i>
        </el-button>
      </el-header>

      <el-container class="main-container">
        <div class="navigator-overlay" :class="{ 'active': isNavigatorOpen }">
          <NavigatorM :username="$route.query.username"></NavigatorM>
        </div>

        <el-container class="content-container">
          <el-main>
            <Users :username="$route.query.username"></Users>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100vh;
  overflow: hidden;
}

.main-container {
  height: calc(100vh - 60px); /* 假设 el-header 高度为 60px */
  overflow: hidden; /* 添加这一行 */
}

.content-container {
  width: 100%;
  max-width: 1200px; /* 或者您想要的任何最大宽度 */
  margin: 0 auto 0 12%;
  padding: 0 20px;
  overflow-y: auto; /* 添加这一行 */
}

.el-main {
  padding: 20px 0;
}

.navigator-overlay {
  position: fixed;
  top: 60px; /* 与 el-header 高度相同 */
  left: -200px; /* 默认隐藏 */
  bottom: 0;
  width: 200px;
  z-index: 1000;
  background-color: #fff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
}

.navigator-overlay.active {
  left: 0;
}

.menu-button {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
}

</style>