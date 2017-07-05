// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuetify from 'vuetify'

Vue.config.productionTip = false

// Use Vuetify for CSS library

/* eslint-disable no-new */
var app = new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

Vue.use(Vuetify)

// SPRINTF filter.  Not sure what it does! Haha
Vue.filter('sprintf', function(value, formatString) {
	return sprintf(formatString, value)
})
