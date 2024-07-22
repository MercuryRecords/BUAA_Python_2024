<script setup lang="ts">
// @ts-ignore
import CreateGroup from "@/components/Base/CreateGroup.vue";
import Navigator from "@/components/Base/Navigator.vue";
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
          <Navigator></Navigator> <!--挂上导航栏，点击即可跳转,现在的位置是home/username=?-->
        </el-aside>

        <el-container>
          <el-main>
            <h1>我创建的群组</h1>
            <!--              主体内容-->
            <RouterView></RouterView>
          </el-main>
        </el-container>
      </el-container>

    </el-container>
  </div>



  <CreateGroup :username="$route.query.username"></CreateGroup>
</template>

<style scoped>
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