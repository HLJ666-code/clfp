import { defineStore } from 'pinia'
import { getMe } from '../api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    loaded: false
  }),
  getters: {
    isLogin: (state) => !!state.user,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  actions: {
    async fetchMe() {
      if (!localStorage.getItem('clfp_token')) {
        this.user = null
        this.loaded = true
        return null
      }
      try {
        this.user = await getMe()
      } catch (e) {
        this.user = null
      }
      this.loaded = true
      return this.user
    },
    setUser(user) {
      this.user = user
    },
    logout() {
      this.user = null
      localStorage.removeItem('clfp_token')
    }
  }
})
