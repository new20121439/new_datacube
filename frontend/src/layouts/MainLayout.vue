<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
      class="main-layout"
    >
      <v-list dense>
        <template v-for="item in menu">
          <v-row
            v-if="item.heading"
            :key="item.heading"
            align="center"
          >
            <v-col cols="6">
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-col>
            <v-col
              cols="6"
              class="text-center"
            >
              <a
                href="#!"
                class="body-2 black--text"
              >EDIT</a>
            </v-col>
          </v-row>
          <v-list-group
            v-else-if="item.children"
            :key="item.text"
            v-model="item.model"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon=""
          >
            <template v-slot:activator>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ item.text }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
            <v-list-item
              v-for="(child, i) in item.children"
              :key="i"
              link
              class="custom-list-item"
              :to="child.link"

            >
              <v-list-item-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>
                  {{ child.text }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
          <v-list-item
            v-else
            :key="item.text"
            link
            v-model="item.model"
            :to="item.link"
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="white"
      flat
      style="border-bottom: solid 1px rgba(0,0,0,0.2)!important"
    >
      <v-btn icon @click.stop="drawer = !drawer"><v-icon>fa-bars</v-icon></v-btn>

      <v-toolbar-title
        style="width: 300px"
        class="ml-0 pl-4"
      >
        <span class="hidden-sm-and-down">GeoAI Admin</span>
      </v-toolbar-title>
      <v-spacer/>
      <v-btn text @click="logout">
        LOGOUT
        <v-icon right>fas fa-sign-out-alt</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content style="background-color: white">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
  import api from '@/api'
  import {mapState} from 'vuex'

  export default {
    props: {
      source: String,
    },
    data: () => ({
      dialog: false,
      drawer: null
    }),
    computed: {
      ...mapState('main', [
        'menu'
      ])
    },
    mounted() {

    },
    methods: {
      goToLink(link) {
        if (this.$route.path !== link) this.$router.push({path: link})
      },

      async logout () {
        await api.post('https://auth.imagetrekk.ai/logout')
        localStorage.clear()
        window.location.href = 'https://imagetrekk.ai'
      }
    }
  }
</script>

<style>
  .main-layout .v-list-group__header .v-list-item {
    padding-left: 0;
  }

  .main-layout .custom-list-item {
    padding-left: 72px;
  }
</style>
