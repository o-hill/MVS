import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Home from '@/components/Homepage'
import Video from '@/components/Video'
import Session from '@/components/Session'

Vue.use(Router)

const home_route = { path: '/', name: 'Home', component: Home }

const video_route = { path: '/video', name: 'Video', component: Video,
  props: true }

const session_route = { path: '/session/:id', name: 'session',
  component: Session, props: true }

const routes = [home_route, video_route, session_route]

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
