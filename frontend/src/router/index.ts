import {createRouter, createWebHistory} from 'vue-router'

import Home from '@/views/Home.vue' //引入要呈现的组件

const router = createRouter({ //创建路由器
    history: createWebHistory(), //路由器的工作模式
    routes: [ //路由规则path-component
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/Login.vue'),
        },
        {
            path: '/',
            redirect: '/login',
            // component: () => import('@/views/Login.vue'),
        },
        {
            path: '/user',
            name: 'user',
            component: () => import('@/views/User.vue')
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('@/views/Home.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/views/Register.vue')
        },
        {
            path: '/group',
            name: 'group',
            component: () => import('@/views/Group.vue'),
        },
        {
            path: '/question',
            name: 'question',
            component: () => import('@/views/QuestionBank.vue'),
        },
        {
            path: '/groupC',
            name: 'groupCreated',
            component: () => import('@/views/GroupCreated.vue'),
        },
        {
            path: '/groupJ',
            name: 'groupJoin',
            component: () => import('@/views/GroupJoined.vue'),
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('@/views/Home.vue'),
        },
    ]
})

export default router //暴露router