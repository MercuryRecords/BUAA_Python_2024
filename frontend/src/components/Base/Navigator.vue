<!--<template>-->
<!--  <div class="navigator">-->
<!--    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">-->
<!--      <el-radio-button :value="false">expand</el-radio-button>-->
<!--      <el-radio-button :value="true">collapse</el-radio-button>-->
<!--    </el-radio-group>-->
<!--    <el-menu-->
<!--        default-active="2"-->
<!--        class="el-menu-vertical-demo"-->
<!--        :collapse="isCollapse"-->
<!--        @open="handleOpen"-->
<!--        @close="handleClose"-->
<!--        router-->
<!--    >-->
<!--      <el-sub-menu index="1">-->
<!--        <template #title>-->
<!--          <el-icon><location /></el-icon>-->
<!--          <span>我的题库</span>-->
<!--        </template>-->
<!--        <el-menu-item-group>-->
<!--          <template #title><span>Group One</span></template>-->
<!--          <el-menu-item index="QuestionBank">item one</el-menu-item>-->
<!--          <el-menu-item index="1-2">item two</el-menu-item>-->
<!--        </el-menu-item-group>-->
<!--        <el-menu-item-group title="Group Two">-->
<!--          <el-menu-item index="1-3">item three</el-menu-item>-->
<!--        </el-menu-item-group>-->
<!--        <el-sub-menu index="1-4">-->
<!--          <template #title><span>item four</span></template>-->
<!--          <el-menu-item index="1-4-1">item one</el-menu-item>-->
<!--        </el-sub-menu>-->
<!--      </el-sub-menu><template>-->
<!--      <v-card>-->
<!--        <v-layout>-->
<!--          <v-navigation-drawer-->
<!--              expand-on-hover-->
<!--              rail-->
<!--          >-->
<!--            <v-list>-->
<!--              <v-list-item-->
<!--                  prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"-->
<!--                  subtitle="sandra_a88@gmailcom"-->
<!--                  title="Sandra Adams"-->
<!--              ></v-list-item>-->
<!--            </v-list>-->

<!--            <v-divider></v-divider>-->

<!--            <v-list density="compact" nav>-->
<!--              <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>-->
<!--              <v-list-item prepend-icon="mdi-account-multiple" title="Shared with me" value="shared"></v-list-item>-->
<!--              <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>-->
<!--            </v-list>-->
<!--          </v-navigation-drawer>-->

<!--          <v-main style="height: 250px"></v-main>-->
<!--        </v-layout>-->
<!--      </v-card>-->
<!--    </template>-->
<!--      <el-menu-item index="Group">-->
<!--        <el-icon><icon-menu /></el-icon>-->
<!--        <template #title>群组</template>-->
<!--      </el-menu-item>-->
<!--      <el-menu-item index="3" disabled>-->
<!--        <el-icon><document /></el-icon>-->
<!--        <template #title>Navigator Three</template>-->
<!--      </el-menu-item>-->
<!--      <el-menu-item index="4">-->
<!--        <el-icon><setting /></el-icon>-->
<!--        <template #title>Navigator Four</template>-->
<!--      </el-menu-item>-->
<!--    </el-menu>-->
<!--  </div>-->
<!--</template>-->

<!--<script lang="ts" setup>-->
<!--import { ref } from 'vue'-->
<!--import LoginCard from "@/components/Base/LoginCard.vue";-->
<!--import {-->
<!--  Document,-->
<!--  Menu as IconMenu,-->
<!--  Location,-->
<!--  Setting,-->
<!--} from '@element-plus/icons-vue'-->

<!--const isCollapse = ref(true)-->
<!--const handleOpen = (key: string, keyPath: string[]) => {-->
<!--  console.log(key, keyPath)-->
<!--}-->
<!--const handleClose = (key: string, keyPath: string[]) => {-->
<!--  console.log(key, keyPath)-->
<!--}-->
<!--</script>-->

<!--<style>-->
<!--.el-menu-vertical-demo:not(.el-menu&#45;&#45;collapse) {-->
<!--  width: 200px;-->
<!--  min-height: 400px;-->
<!--}-->

<!--.navigator {-->
<!--  margin-right: auto;-->
<!--  margin-left: 0;-->
<!--}-->
<!--</style>-->

<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
          expand-on-hover
          rail
      >
        <v-list>
          <v-list-item
              prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
              title="用户名"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-folder" title="我的题库" value="myfiles">
            <v-list density="compact" nav>
              <v-list-item prepend-icon="mdi-folder" title="我创建的题单" value="create"
                           :to="{name:'myQuestionSheet', query: {username: props.username}}"
              > <!--这里把username传给groupCreated模块了-->
              </v-list-item>

              <v-list-item prepend-icon="mdi-account-multiple" title="我加入的" value="join"
                           :to="{name:'groupJoin', query: {username: props.username}}">
              </v-list-item>

              <v-list-item prepend-icon="mdi-star" title="题库" value="starred" :to="{name:'question' ,query: {username: props.username}}"></v-list-item>
            </v-list>
          </v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="" value="mygroup">
            <v-list density="compact" nav>
              <v-list-item prepend-icon="mdi-folder" title="我创建的" value="create"
                           :to="{name:'groupCreated', query: {username: props.username}}"
              > <!--这里把username传给groupCreated模块了-->
              </v-list-item>

              <v-list-item prepend-icon="mdi-account-multiple" title="我加入的" value="join"
                           :to="{name:'groupJoin', query: {username: props.username}}">
              </v-list-item>

              <v-list-item prepend-icon="mdi-star" title="我收藏的" value="starred"></v-list-item>
            </v-list>
          </v-list-item>
          <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main style=""></v-main>
    </v-layout>
  </v-card>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from "vue";

const props = defineProps(['username']) //Navigator拿到一直传进来的username，之后的函数操作都要有
onMounted(()=>console.log(props.username))
</script>