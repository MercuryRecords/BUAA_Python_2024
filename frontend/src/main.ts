import './assets/main.css'

import {createApp} from 'vue'
import App from './App.vue'

import router from './router' //引入路由器
import API from '@/plugins/axios.js'
const app = createApp(App) //创建一个应用

app.use(router) //使用路由器

app.mount('#app') //挂载

app.config.globalProperties.$axios = API;
app.config.globalProperties.$http = API;
