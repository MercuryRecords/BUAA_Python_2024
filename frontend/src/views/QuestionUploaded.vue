<script setup lang="ts">
// @ts-ignore
import Navigator from "@/components/Base/Navigator.vue";
import UploadQuestion from "@/components/Base/UploadQuestion.vue";
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <!--          <h1>Shared Platform</h1>-->
      </el-header>

      <el-container class="main-container">
        <el-aside width="200px" class="navigation-aside">
          <!--            导航栏-->
          <Navigator :username="$route.query.username"></Navigator> <!--挂上导航栏，点击即可跳转,现在的位置是home/username=?-->
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <!--              主体内容-->
            <UploadQuestion :username="$route.query.username" :sheetId="$route.query.sheetId"></UploadQuestion>
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
  height: calc(100vh - 60px); /* 假设 header 高度为 60px */
  overflow: hidden;
}

.navigation-aside {
  position: relative;
  z-index: 10;
  height: 100%;
  overflow-y: auto;
}

.shifted-content {
  margin-left: 0;
  margin-right: 80px;
  overflow-y: auto;
  height: 100%;
}

.el-menu {
  border-right: none;
}

.el-main {
  padding: 0;
}

.toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>