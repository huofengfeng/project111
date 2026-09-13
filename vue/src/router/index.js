import {createRouter, createWebHistory} from 'vue-router'
import heritageConfirm from '@/utils/heritageConfirm.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/front/frontview/FrontPage.vue') },
    {
      path: '/manager',
      component: () => import('@/views/Manager.vue'),
      redirect: '/manager/home',
      children: [
        { path: 'person', component: () => import('@/views/manager/Person.vue')},
        { path: 'password', component: () => import('@/views/manager/Password.vue')},
        { path: 'home', component: () => import('@/views/manager/Home.vue')},
        { path: 'admin', component: () => import('@/views/manager/Admin.vue')},
        { path: 'user', component: () => import('@/views/manager/User.vue')},
        { path: 'artifact', component: () => import('@/views/manager/Artifact.vue')},
        { path: 'tombsMap', component: () => import('@/views/manager/TombsMap.vue')},
        { path: 'timeline', component: () => import('@/views/manager/Timeline.vue')},
        { path: 'knowledge-graph', component: () => import('@/views/manager/KnowledgeGraph.vue')},
      ]
    },
    { path: '/login', component: () => import('@/views/Login.vue')},
    { path: '/register', component: () => import('@/views/Register.vue')},
    { path: '/profile', component: () => import('@/views/front/Profile.vue'), meta: { requiresAuth: true }},
    { path: '/appreciation', component: () => import('@/views/front/ArtifactAppreciation.vue'), meta: { requiresAuth: true }},
    { path: '/artifact/:id', component: () => import('@/views/front/ArtifactDetail.vue'), meta: { requiresAuth: true }},
    { path: '/quiz', component: () => import('@/views/front/QuizGame.vue'), meta: { requiresAuth: true }},
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = sessionStorage.getItem('access_token')
    if (!token) {
      heritageConfirm({
        title: '访问受限',
        message: '该页面需要登录后才能访问，请先登录',
        confirmText: '前往登录',
        cancelText: '继续浏览',
      }).then((confirmed) => {
        if (confirmed) {
          next('/login')
        } else {
          next(false)
        }
      })
      return
    }
  }
  next()
})

export default router
