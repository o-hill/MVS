<template>
  <div>
    <v-container xs12 fluid class = "text-xs-center">
      <v-layout row wrap>
        <v-flex xs4>
          <v-card class = "secondary">
            <v-card-text class = "white--text">New Session</v-card-text>
              <v-flex xs8 offset-xs2>
                <v-text-field
                  v-model = 'session_name'
                  name = "input-1"
                  label = "Session Name"
                  hint = "Required"
                  dark
                  required></v-text-field>
              </v-flex>
            <v-btn primary dark class = "mb-3"
              @click.native = 'create_session()'>Create a Session
            </v-btn>
            <v-spacer/>
          </v-card>
        </v-flex>
        <v-flex xs8>
          <v-card class = "secondary">
            <v-card-text class = "white--text">Session List</v-card-text>
            <v-flex xs10 offset-xs1>
              <v-data-table v-if = 'items.length > 0'
                :headers = 'table_headers'
                :items = 'items'
                class = "elevation-1"
              >
                <template slot = 'items' scope = 'props'>
                  <td>
                    <router-link
                      :to = "{ name: 'session', params:{ id: props.item._id }}"
                      @click.native = 'set_session(props.item._id)'>
                      {{ props.item.name }}
                    </router-link>
                  </td>
                  <td>{{ props.item._id }}</td>
                  <td>{{ props.item.createdAt }}</td>
                </template>
              </v-data-table>
              <v-card-text class = "text-xs-center white--text" v-else>
                There are no sessions currently in the database.
                Create one using the form to the left.
              </v-card-text>
            </v-flex>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>


<script>

  export default {



    data () {
      return {
        table_headers: [
          { text: 'Session Name', left: true, value: 'name' },
          { text: 'Session ID', left: true, value: '_id' },
          { text: 'Time Created', left: true, value: 'time' }
        ],
        session_name: null,
        show_message: false,
        error_message: '',
        valid_sessions: []
      }
    },

    computed: {

      items() {
        return this.$store.state.session_list
      }
    },

    methods: {

      create_session() {
        if (!this.session_name) {
          this.error_message = 'The session must have a name'
          this.show_message = true
        }
        else {
          // Create the session.
          var session_data = { name: this.session_name }
          this.$store.dispatch('create_session', session_data)
          this.$store.dispatch('list_sessions')
          this.valid_sessions = this.$store.state.session_list
        }
      },

      set_session(session_id) {
        this.$store.dispatch('get_session', session_id)
      }
    },

    mounted() {
      this.$store.dispatch('list_sessions')
      // this.valid_sessions = this.$store.state.session_list
      // console.log(this.valid_sessions)
    }
  }

</script>


<style>


</style>
