import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/connect'

// Use Vuex as the global data storage for the app.
Vue.use(Vuex)

var current_session = {}
var current_camera = {}
var session_list = []
var coordinates = {}
var current_target = {}
var latest_image = null

export default new Vuex.Store({

  // --------- STATE VARIABLES ----------

  state: {

    current_session: current_session,
    session_list: session_list,
    current_camera: current_camera,
    coordinates: coordinates,
    current_target: current_target,
    latest_image: latest_image
  },

  // --------- MUTATIONS ----------

  mutations: {

    set_current_session(state, data) {
      state.current_session = data
    },

    set_session_list(state, data) {
      state.session_list = data
    },

    set_current_camera(state, data) {
      state.current_camera = data
    },

    set_coordinates(state, data) {
      state.coordinates = data['cords']
    },

    set_target(state, data) {
      state.current_target = data
    },

    set_image(state, data) {
      state.latest_image = data['latest']
    }
  },

  // --------- ACTIONS -----------

  actions: {

    create_session(context, data) {
      // Create a new session
      api.post_resource('sessions', data).then(function(response) {
        context.commit('set_current_session', response.data)
        //router.push({ name: 'session', params: { id: response.data._id }})
        context.session_list.push(response.data)
      })
    },

    list_sessions(context) {
      // List all of the sessions in the database.
      api.list_resource('sessions').then(function(response) {
        context.commit('set_session_list', response.data)
      })
    },

    get_session(context, session_id) {
      api.get_resource('session', session_id).then((response) => {
        context.commit('set_current_session', response.data)
      })
    },

    add_camera(context, data) {
      // Add a camera to the current session, and update the
      // current session so that it reflects the change.
      api.put_resource('session', data).then((response) => {
        context.commit('set_current_session', response.data)
        context.commit('set_coordinates', reponse.data)
      })
    },

    get_camera(context, camera_id) {
      api.get_resource('camera', camera_id).then((response) => {
        context.commit('set_current_camera', response.data)
        context.commit('set_coordinates', response.data)
      })
    },

    move_camera(context, data) {
      api.put_resource('camera', data).then((response) => {
        context.commit('set_current_camera', response.data)
        context.commit('set_coordinates', response.data)
      })
    },

    add_target(context, data) {
      api.put_resource('camera', data).then((response) => {
        context.commit('set_current_camera', response.data)
      })
    },

    get_target(context, target_id) {
      api.get_resource('target', target_id).then((response) => {
        context.commit('set_target', response.data)
        context.commit('set_coordinates', response.data)
        context.commit('set_image', response.data)
      })
    },

    start_target(context, data) {
      api.put_resource('target', data)
    }
  }
})
