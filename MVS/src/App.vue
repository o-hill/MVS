<template>
  <div id="app">
	  <img src = "./assets/logo.jpg" class = 'logo'>
<!--	<img width = "650" height = "350"
	src = "http://0.0.0.0:1492/video_feed">
	  <img width = "800" height = "350"
	  src = "http://0.0.0.0:1493/microscope_feed"> -->

    <div>
      <v-card>
        <v-card-text>
          <div>{{ card_text }}</div>
        </v-card-text>
      </v-card>

      <!-- <v-card class = "blue darken-1 white--text mt-3">
        <v-card-text>
          <div>{{ card_text }}</div>
        </v-card-text>
      </v-card> -->
    </div>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',

  data() {
    return {
      card_text: "This is the text in the card"
    }
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
