<script setup lang="ts">
// @ts-ignore
import CreateGroup from "@/components/Base/CreateGroup.vue";
import Navigator from "@/components/Base/Navigator.vue";
import { ref } from 'vue';
import JoinGroup from "@/components/Base/JoinGroup.vue";

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
          <Navigator :username="$route.query.username"></Navigator>
        </div>

        <el-container class="content-container">
          <el-main class="shifted-content">
            <JoinGroup :username="$route.query.username"></JoinGroup>
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
}

.content-container {
  width: 100%;
  max-width: 1200px; /* 或者您想要的任何最大宽度 */
  margin: 0 auto 0 12%;
  padding: 0 20px;
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