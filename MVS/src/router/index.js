import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Homepage'
import Session from '@/components/Session'
import Dish from '@/components/Dish'
import Target from '@/components/Target'


Vue.use(Router)

const home_route = { path: '/', name: 'Home', component: Home }

const session_route = { path: '/session/:id', name: 'session',
  component: Session, props: true }

const camera_route = { path: '/camera/:id', name: 'camera', component: Dish,
  props: true }

const target_route = { path: '/target/:id', name: 'target', component: Target,
  props: true }



const routes = [home_route, session_route, camera_route, target_route ]

export default new Router({
  routes: routes
})


// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'Hello',
//       component: Hello
//     }
//   ]
// })
