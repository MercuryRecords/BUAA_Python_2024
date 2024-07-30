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
              :prepend-avatar="picture"
              :title="props.username"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-folder" title="我的题库" value="myfiles">
            <v-list density="compact" nav>
              <v-list-item prepend-icon="mdi-folder" title="我可编辑的题单" value="create"
                           :to="{name:'myQuestionSheet', query: {username: props.username}}"
              > <!--这里把username传给groupCreated模块了-->
              </v-list-item>

              <v-list-item prepend-icon="mdi-account-multiple" title="我可查看的题单" value="join"
                           :to="{name:'sheetViewed', query: {username: props.username}}">
              </v-list-item>

              <v-list-item prepend-icon="mdi-star" title="题库" value="starred"
                           :to="{name:'question' ,query: {username: props.username}}">
              </v-list-item>
              <v-list-item prepend-icon="mdi-clock-star-four-points-outline" title="错题日志" value="wrongProblemSet"
                           :to="{name:'wrongQuestionSet' ,query: {username: props.username}}">
              </v-list-item>
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
          <v-list-item prepend-icon="mdi-medal" title="我的能力" value="medal"
                       :to="{name:'abilityShowed' ,query: {username: props.username}}"></v-list-item>
          <v-list-item prepend-icon="mdi-account-cog" title="个人中心" value="account-cog"
                       :to="{name:'userCenters' ,query: {username: props.username}}"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main style=""></v-main>
    </v-layout>
  </v-card>
</template>

<script setup lang="ts">
import {ref, onMounted, onUnmounted} from "vue";
import API from "@/plugins/axios";

const picture = ref('https://randomuser.me/api/portraits/women/85.jpg')
const props = defineProps(['username']) //Navigator拿到一直传进来的username，之后的函数操作都要有
function getPicture() {
  API.post('/get_avatar',
      {
        username: props.username,
      },
      {
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      }
  ).then(
      function (response) {
        if (response.data.code === 200) {
          console.log('successfully get!')
          console.log(response.data)
          console.log(response.data.avatar)
          picture.value = response.data.avatar
        } else {
          console.log(response.data.message)
        }
      }
  ).catch(
      function () {
        console.log('error')
      }
  )
}

onMounted(() => getPicture())
</script>