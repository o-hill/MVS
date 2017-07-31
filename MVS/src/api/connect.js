import axios from 'axios'

// NEED TO FIGURE OUT HOW TO DEAL WITH MULTIPLE
//  VIDEO SERVERS - UP TO SIX.
const BASE_URL = 'http://localhost:1492'

// Basic API for communicating between front and back end.

export default {

  get_static(resource_name) {
    var url = BASE_URL + '/' + resource_name
    return axios.get(url)
  },

  get_resource(resource_name, id) {
    var url = BASE_URL + '/' + resource_name + '/' + id
    return axios.get(url)
  },

  list_resource(resource_name) {
    var url = BASE_URL + '/' + resource_name
    return axios.get(url)
  },

  delete_resource(resource_name, id) {
    var url = BASE_URL + '/' + resource_name + '/' + id
    return axios.delete(url)
  },

  post_resource(resource_name, data) {
    var url = BASE_URL + '/' + resource_name
    return axios.post(url, data)
  },

  put_resource(resource_name, data) {
    var url = BASE_URL + '/' + resource_name + '/' + data.id
    return axios.put(url, data)
  },

  // stream_resource(resource_name, data) {
  //   var url = BASE_URL + '/' + resource_name + '/' + data.id
  //   url += '/stream'
  //   url += '?' + 'min=' + data['min_time']
  //   url += '&' + 'max=' + data['max_time']
  //   return axios.get(url, data)
  // },

  get_history(resource_name, data) {
    var url = BASE_URL + '/' + resource_name + '/' + data.id
    url += '/history'
    return axios.get(url, data)
  }
}
