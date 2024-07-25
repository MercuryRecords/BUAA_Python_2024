import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'
import {createApp} from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus' // 引入ElementPlus
import 'element-plus/dist/index.css'
import router from './router' //引入路由器
import API from '@/plugins/axios.js'
// Vuetify
import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App) //创建一个应用
const vuetify = createVuetify({
    components,
    directives,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router) //使用路由器
app.use(ElementPlus) // 使用ElementPlus
app.use(vuetify)

app.mount('#app') //挂载

app.config.globalProperties.$axios = API;
app.config.globalProperties.$http = API;
