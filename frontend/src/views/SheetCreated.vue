<script setup lang="ts">
// @ts-ignore
import Navigator from "@/components/Base/Navigator.vue";
import CreateSheet from "@/components/Base/CreateSheet.vue";
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <!--          <h1>Shared Platform</h1>-->
      </el-header>

      <el-container>
        <el-aside width="200px">
          <!--            导航栏-->
          <Navigator :username="$route.query.username"></Navigator> <!--挂上导航栏，点击即可跳转,现在的位置是home/username=?-->
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <!--              主体内容-->
            <CreateSheet :username="$route.query.username"></CreateSheet>
          </el-main>
        </el-container>
      </el-container>

    </el-container>
  </div>

</template>

<style scoped>
.shifted-content {
  margin-left: 80px;
  margin-right: 80px;
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