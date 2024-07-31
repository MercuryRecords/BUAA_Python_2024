<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
          expand-on-hover
          rail
          style="background-color: rgb(52, 73, 94); color: rgb(221, 221, 221);"
      >
        <v-list>
          <v-list-item
              :prepend-avatar='picture'
              :title="props.username"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-account" title="用户管理" value="join"
                       :to="{name:'users', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="群组管理" value="join"
                       :to="{name:'groups', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-bookmark-check" title="题单管理" value="bookmark"
                       :to="{name:'problemGroups', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-folder" title="题库管理" value="join"
                       :to="{name:'questions', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-shield-alert-outline" title="敏感词管理" value="join"
                       :to="{name:'sensitive_words', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-account-cog" title="个人中心" value="account-cog"
                       :to="{name:'adminCenters' ,query: {username: props.username}}"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main style=""></v-main>
    </v-layout>
  </v-card>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from "vue";
import API from "@/plugins/axios";
import picture from "@/assets/default.png"

const props = defineProps(['username']) //Navigator拿到一直传进来的username，之后的函数操作都要有
</script>