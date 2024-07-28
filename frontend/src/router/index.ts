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
            path: '/myQuestionSheet',
            name: 'myQuestionSheet',
            component: () => import('@/views/SheetCreated.vue'),
        },
        {
            path: '/groupQuestion',
            name: 'QuestionBank4SpecificGroup',
            component: () => import('@/views/groupQuestion.vue'),
        },
        {
            path: '/upload',
            name: 'upload',
            component: () => import('@/views/QuestionUploaded.vue'),
        },
        {
            path: '/sheet',
            name: 'sheet',
            component: () => import('@/views/Sheet.vue'),
        },
        {
            path: '/solveQuestion',
            name: 'solve',
            component: () => import('@/views/SolveQuestion.vue')
        },
        {
            // 管理员的用户管理页面
            path: '/users',
            name: 'users',
            component: () => import('@/views/UserManagement.vue')
        },
        {
            // 管理员的用户组管理页面
            path: '/groups',
            name: 'groups',
            component: () => import('@/views/GroupManagement.vue')
        },
        {
            // 管理员的用户组管理页面
            path: '/questions',
            name: 'questions',
            component: () => import('@/views/QuestionManagement.vue')
        },
        {
            path: '/sheetViewed',
            name: 'sheetViewed',
            component: () => import('@/views/SheetViewed.vue')
        },
        {
            path: '/userCenters',
            name: 'userCenters',
            component: () => import('@/views/UserCenters.vue')
        },
        {
            path: '/wrongQuestionSet',
            name: 'wrongQuestionSet',
            component: () => import('@/views/WrongQuestionSet.vue')
        }
    ]
})

export default router //暴露router