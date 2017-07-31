import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/connect'

// Use Vuex as the global data storage for the app.
Vue.use(Vuex)

var current_session = {}
var current_camera = {}
var session_list = []

export default new Vuex.Store({

  // --------- STATE VARIABLES ----------

  state: {

    current_session: current_session,
    session_list: session_list,
    current_camera: current_camera
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
      })
    },

    get_camera(context, camera_id) {
      api.get_resource('camera', camera_id).then((reponse) => {
        context.commit('set_current_camera', response.data)
      })
    }
  }
})
