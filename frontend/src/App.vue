<script setup lang="ts" name="App">
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import User from '@/views/User.vue';
import UserQuestionBank from '@/components/Base/Navigator.vue';
import Navigator from "@/components/Base/Navigator.vue";
import GroupCreated from "./views/GroupCreated.vue";

</script>


<template>
<!--  <div class="common-layout">-->
<!--    <el-container>-->
<!--      <el-header>-->
<!--        &lt;!&ndash;          <h1>Shared Platform</h1>&ndash;&gt;-->
<!--      </el-header>-->

<!--      <el-container>-->
<!--        <el-aside width="200px">-->
<!--          &lt;!&ndash;            导航栏&ndash;&gt;-->
<!--          <Navigator></Navigator> &lt;!&ndash;挂上导航栏，点击即可跳转,现在的位置是home/username=?&ndash;&gt;-->
<!--        </el-aside>-->

<!--        <el-container>-->
            <!--              主体内容-->
            <RouterView></RouterView>
<!--        </el-container>-->
<!--      </el-container>-->

<!--    </el-container>-->

<!--  </div>-->
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
