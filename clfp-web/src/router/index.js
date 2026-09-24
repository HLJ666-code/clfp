import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('../layout/Layout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('../views/Home.vue') },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('../views/user/Profile.vue'),
        meta: { auth: true }
      },
      {
        path: 'my-posts',
        name: 'my-posts',
        component: () => import('../views/user/MyPosts.vue'),
        meta: { auth: true }
      }
      // 孟炅：path 'match' 我的匹配；彭定星：path 'claim' 我的认领 —— 后续在此追加
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局登录守卫
router.beforeEach((to) => {
  const token = localStorage.getItem('clfp_token')
  if (to.meta.auth && !token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if ((to.path === '/login' || to.path === '/register') && token) {
    return { path: '/' }
  }
  return true
})

export default router
