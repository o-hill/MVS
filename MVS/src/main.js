// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuetify from 'vuetify'

Vue.config.productionTip = false

// Use Vuetify for CSS library
Vue.use(Vuetify);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

// SPRINTF filter.  Not sure what it does! Haha
Vue.filter('sprintf', function(value, formatString) {
	return sprintf(formatString, value)
})
