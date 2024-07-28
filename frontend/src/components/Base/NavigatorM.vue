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
          <v-list-item prepend-icon="mdi-account" title="用户管理" value="join"
                       :to="{name:'users', query: {username: props.username}}">
          </v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="群组管理" value="join"
                       :to="{name:'groups', query: {username: props.username}}">
          </v-list-item>

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