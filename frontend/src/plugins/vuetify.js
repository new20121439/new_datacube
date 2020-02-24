import Vue from 'vue'
import Vuetify from 'vuetify'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify)

const options = {
  icons: {
    iconfont: 'fa',
    values: {
      next: 'fas fa-caret-right',
      prev: 'fas fa-caret-left'
    }
  },

  theme: {
    primary: colors.teal.darken1,
    accent: '#343a40'
  }
}

export default new Vuetify(options)