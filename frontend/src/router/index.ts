import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue')
    },
    {
      path: '/teams',
      name: 'Teams',
      component: () => import('../views/Teams.vue')
    },
    {
      path: '/players',
      name: 'Players',
      component: () => import('../views/Players.vue')
    },
    {
      path: '/prediction',
      name: 'Prediction',
      component: () => import('../views/Prediction.vue')
    },
    {
      path: '/bracket',
      name: 'Bracket',
      component: () => import('../views/Bracket.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/player',
      name: 'Player',
      component: () => import('../views/Player.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫：全局登录拦截
router.beforeEach((to, from, next) => {
  // 如果前往的是登录页，直接放行
  if (to.path === '/login') {
    next()
    return
  }
  
  // 对于其他所有页面，检查本地是否有 token
  const token = localStorage.getItem('sjb_token')
  if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
