import axios from 'axios'

const API = axios.create({

    timeout: 20000,                  //请求超时设置，单位ms
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    baseURL: 'http://localhost:8000/api/',
    withCredentials : true
})

//导出我们建立的axios实例模块，ES6 export用法
export default API