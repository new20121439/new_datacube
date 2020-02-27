import Vue from 'vue'
import Vuex from 'vuex'
import main from './main'
import user from './user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    navigation: null,
    loginPath: undefined,
    title: '',
    snackbar: false,
    snackbarColor: undefined,
    notificationText: '',
    progress: false,
    downloadRef: undefined,
    appName: 'GeoAi Admin'
  },
  mutations: {
    setAppName (state, name) {
      state.appName = name
    },
    setNavigation (state, visible) {
      state.navigation = visible
    },
    toggleNavigation (state) {
      state.navigation = !state.navigation
    },
    setLoginPath (state, to) {
      state.loginPath = to
    },
    setTitle (state, name) {
      state.title = name
    },
    setSnackbar (state, val) {
      state.snackbar = val
    },
    setProgress (state, val) {
      state.progress = val
    },
    showInfoSnackbar (state, val) {
      state.snackbarColor = undefined
      state.notificationText = val
      state.snackbar = true
    },
    showErrorSnackbar (state, val) {
      state.snackbarColor = 'error'
      state.notificationText = val
      state.snackbar = true
    },
    setDownloadRef (state, val) {
      state.downloadRef = val
    }
  },
  actions: {
    downloadUrl ({state}, url) {
      state.downloadRef.href = url
      state.downloadRef.click()
    }
  },
  modules: {
    main,
    user
  }
})
