<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <!--          <h1>Shared Platform</h1>-->
      </el-header>

      <el-container>
        <el-aside width="200px">
          <!--            导航栏-->
          <Navigator :username="$route.query.username"></Navigator> <!--将username向下传给Navigator组件-->
        </el-aside>

        <el-container>
          <el-main>
            <!--              主体内容-->
            <RouterView></RouterView>
          </el-main>
        </el-container>
      </el-container>

    </el-container>
  </div>
</template>

<script lang="ts" setup>

import Navigator from "@/components/Base/Navigator.vue";

</script>

<style>
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