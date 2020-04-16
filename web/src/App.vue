<template>
  <div id="app">
    <router-view class="content" />
  </div>
</template>

<style lang="scss" scoped>
  #app {
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;
  }
  .content {
    flex: 1;
  }
</style>

<script lang="ts">
import Vue from 'vue';
import Buefy from 'buefy';

import 'buefy/dist/buefy.css';

Vue.use(Buefy);

export default Vue.extend({
});
</script>
