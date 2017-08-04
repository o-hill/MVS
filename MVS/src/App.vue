<template>
  <v-app id = "app">
    <v-toolbar class = "elevation-0 blue-grey darken-4">
      <v-toolbar-side-icon></v-toolbar-side-icon>
      <v-toolbar-title>MVS Microscope</v-toolbar-title>
      <v-toolbar-logo>
        <a href = '/'>
	         <img src = "./assets/logo.jpg" class = 'logo'>
         </a>
      </v-toolbar-logo>
    </v-toolbar>
    <router-view></router-view>
  </v-app>
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

.logo {
  height: 60px;
  text-align: left;
}
</style>
