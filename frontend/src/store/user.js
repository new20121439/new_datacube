import { uniq } from 'lodash'
import api from '@/api'
import Store from "@/store/index";

export default {
  namespaced: true,
  state: {
    current: undefined
  },
  getters: {
    scopes: state => {
      let scopes = []
      if (state.current) {
        state.current.roles.forEach(role => {
          role.permissions.forEach(permission => {
            scopes.push(permission.name)
          })
        })
      }
      return uniq(scopes)
    },

    can: (state) => (name) => {
      if (!name) {
        return true
      }
      if (state.current) {
        for (let i = 0; i < state.current.roles.length; i++) {
          for (let j = 0; j < state.current.roles[i].permissions.length; j++) {
            if (state.current.roles[i].permissions[j].name === name) {
              return true
            }
          }
        }
      }
      return false
    }
  },
  mutations: {
    setUser(state, payload) {
      state.current = payload
    }
  },

  actions: {
    async getMe(context) {
      let success = await api.get('/api/auth/me')
      context.commit('setUser', success.data.result)
    }
  }
}
