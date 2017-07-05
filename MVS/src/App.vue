<template>
  <div id="app">
	  <img src = "./assets/logo.jpg" class = 'logo'>
<!--	<img width = "650" height = "350"
	src = "http://0.0.0.0:1492/video_feed">
	  <img width = "800" height = "350"
	  src = "http://0.0.0.0:1493/microscope_feed"> -->

    <router-view></router-view>
  </div>
</template>


<script>
  export default {
    name: 'app'
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
