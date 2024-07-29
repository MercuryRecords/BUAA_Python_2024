import axios from 'axios'

const API = axios.create({

    timeout: 50000,                  //请求超时设置，单位ms
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    baseURL: 'http://localhost:8000/api/',
    // baseURL: 'http://192.168.137.1:8000/api/', // 服务器 IP 地址
    withCredentials : true
})

// 作为服务器运行时，在 package.json 文件中的 scripts 中添加服务器地址
//"scripts": {
//    "dev": "vite --host 192.168.137.1",
//    ...
//}

//导出我们建立的axios实例模块，ES6 export用法
export default API