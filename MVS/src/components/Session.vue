<template>
  <div>
    <v-container xs12 fluid class = "text-xs-center">
      <v-layout row wrap>
        <v-flex xs4>
          <v-card class = "secondary">
            <v-card-text class = "white--text">Add a camera</v-card-text>
            <v-btn outline fab class="teal--text" @click.native='add_camera(0)'>One</v-btn>
            <v-btn outline fab class = "blue--text" @click.native='add_camera(1)'>Two</v-btn>
            <v-btn outline fab class = "indigo--text" @click.native='add_camera(2)'>Three</v-btn>
            <v-btn outline fab class = "red--text" @click.native='add_camera(3)'>Four</v-btn>
            <v-btn outline fab class = "pink--text" @click.native='add_camera(4)'>Five</v-btn>
            <v-btn outline fab class = "green--text" @click.native='add_camera(5)'>Six</v-btn>
          </v-card>
        </v-flex>
        <v-flex xs8>
          <v-card class = "secondary">
            <v-card-text class = "grey--text">Active Cameras</v-card-text>
            <v-flex xs10 offset-xs1>
              <v-data-table v-if = 'cameras > 0'
                :headers = 'table_headers'
                :items = 'cameras'
                class = "elevation-1"
              >
                <template slot = 'items' scope = 'props'>
                  <td>
                    <router-link
                      :to = "{ name: 'camera', params:{ id: props.item._id }}"
                      @click.native = 'set_camera(props.item._id)'>
                      {{ props.item.source }}
                    </router-link>
                  </td>
                  <td>{{ props.item._id }}</td>
                  <td>{{ props.item.num_targets }}</td>
                </template>
              </v-data-table>
              <v-card-text class = "text-xs-center white--text" v-else>
                There are no cameras currently associated with this session.
                Add one using the card to the left.
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

    data() {
      return {
        table_headers: [
          { text: 'Camera Number', left: true, value: 'number' },
          { text: 'Camera ID', left: true, value: '_id' },
          { text: 'Number of Targets', left: true, value: 'targets' }
        ],
        session_id: this.$store.state.current_session['_id']
      }
    },

    computed: {

      cameras() {
        return this.$store.state.camera_list
      }
    },

    methods: {

      add_camera(src) {
        var camera_data = {
          source: src,
          cmd: 'add',
          id: this.$store.state.current_session['_id']
        }
        debugger;
        this.$store.dispatch('add_camera', camera_data)
      }
    }

    // mounted() {
    //
    //   //this.cameras = this.$store.state.current_session['cameras']
    // }
  }


</script>




<style>

</style>
