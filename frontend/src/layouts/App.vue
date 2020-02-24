<template>
  <div>
    <router-view></router-view>
    <v-snackbar
      v-model="$store.state.snackbar"
      :color="$store.state.snackbarColor"
      bottom
      :timeout="8000"
    >
      {{ $store.state.notificationText }}
      <v-btn
        text
        @click="$store.commit('setSnackbar', false)"
      >
        Close
      </v-btn>
    </v-snackbar>
    <v-progress-linear
      v-if="$store.state.progress"
      :indeterminate="true"
      height="7px"
      color="primary"
      style="position: fixed;bottom: 0;margin: 0;z-index: 10000;">
    </v-progress-linear>
    <a v-show="false" ref="download" href="#"></a>
  </div>
</template>

<script>
  export default {
    mounted() {
      this.$store.commit('setDownloadRef', this.$refs.download)
    }
  }
</script>
