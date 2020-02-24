import Vue from 'vue'
import Router from 'vue-router'
import MainLayout from '@/layouts/MainLayout'
import Dashboard from '@/views/Dashboard'
import Api from '@/api'
import Store from '@/store'
import Login from '@/views/Login'

Vue.use(Router)

let requiredAuth = (to, from, next) => {
  let goToLogin = () => {
    Store.commit('setLoginPath', to)
    let param = new URLSearchParams("redirect="+window.location.origin+"/login?token=")
    window.location.href = 'https://imagetrekk.ai/signIn.html?'+param.toString()
  }
  let token = Api.getToken()
  if (!token) {
    goToLogin()
  } else {
    console.log('here')
    next()
    // Api.submitOnce('get', '/api/auth/me', {}, true).then(success => {
    //   next()
    // }).catch(e => {
    //   if (e.response.status === 401) {
    //     goToLogin()
    //     return
    //   } else if (e.response.status === 403 || e.response.status === 500) {
    //     next({name: 'forbidden'})
    //     return
    //   }
    //    goToLogin()
    // })

  }
}

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      component: MainLayout,
      beforeEnter: requiredAuth,
      children: [
        { path: '', component: Dashboard, name: 'home' }
      ]
    },
    { path: '/login', component: Login, name: 'login'},
  ]
})
