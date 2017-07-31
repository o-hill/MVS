import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/connect'

// Use Vuex as the global data storage for the app.
Vue.use(Vuex)

var current_session = {}
var session_list = []
var camera_list = []

export default new Vuex.Store({

  // --------- STATE VARIABLES ----------

  state: {

    current_session: current_session,
    session_list: session_list,
    camera_list: camera_list
  },

  // --------- MUTATIONS ----------

  mutations: {

    set_current_session(state, data) {
      state.current_session = data
    },

    set_session_list(state, data) {
      state.session_list = data
    },

    set_session_cameras(state, data) {
      state.camera_list = data
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

    set_session(context, session_id) {
      api.get_resource('session', 'session', session_id).then((response) => {
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

    list_cameras(context, session_id) {
      // Get all of the cameras currently associated
      // the given session id.
      api.get_resource('session', 'cameras', session_id).then((response) => {
        context.commit('set_session_cameras', response.data)
      })
    }
  }
})
