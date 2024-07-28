<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <!-- 头部内容可以在这里添加 -->
      </el-header>

      <el-container>
        <el-aside width="200px">
          <!-- 根据mode选择不同的导航栏 -->
          <NavigatorM v-if="$route.query.mode === '0'" :username="$route.query.username" />
          <Navigator v-else-if="$route.query.mode === '1'" :username="$route.query.username" />
        </el-aside>

        <el-container>
          <el-main>
            <RouterView></RouterView>
          </el-main>
        </el-container>
      </el-container>

    </el-container>
  </div>
</template>

<script lang="ts" setup>
import Navigator from "@/components/Base/Navigator.vue";
import NavigatorM from "@/components/Base/NavigatorM.vue";
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