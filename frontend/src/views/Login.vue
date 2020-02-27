<template>
  <v-app>
    <v-content v-show="false">
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login to {{$store.state.appName}}</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="formSubmit">
                  <v-text-field
                    id="password"
                    prepend-icon="fa-lock"
                    name="password"
                    label="Password"
                    type="password"
                    required
                    v-model="password"
                    autocomplete="off"
                    placeholder="Password"
                    @keypress.enter="formSubmit()"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" :disabled="!valid" @click.stop="login()">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Api from "@/api"

export default {
  data: () => ({
    email: "",
    password: "",
    valid: true
  }),
  created() {
    let url = new URL(window.location.href)
    let token = url.searchParams.get('token')
    if (token) {
      localStorage.setItem('jwt_token', token)
      this.$router.push({name: 'home'})
    }
  },
  methods: {
    login() {
      if (this.$refs.form.validate()) {
        Api.post('/api/auth/login', {
          password: this.password
        })
        .then(success => {
          Api.setToken(success.data.token)
          this.$router.push({ name: "home" })
        })
        .catch(error => {
          this.$store.commit('showErrorSnackbar', error.response.data.message)
        });
      }
    },

    formSubmit() {
      this.login();
    }
  }
};
</script>
