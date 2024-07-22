<script lang="ts">
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import User from '@/views/User.vue';
import UserQuestionBank from '@/components/Base/Navigator.vue';
import Navigator from "@/components/Base/Navigator.vue";

export default {
  name: "App",
  components: {Navigator, UserQuestionBank, Login, Register, User}
}
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
            <Navigator></Navigator>
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
