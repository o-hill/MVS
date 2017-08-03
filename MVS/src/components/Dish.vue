<template>
  <v-layout row wrap>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>Live Video Feed</v-card-text>
        <!-- <img src = 'http://0.0.0.0:1493/video_feed' height = "200" width = "350"> -->
      </v-card>
    </v-flex>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text class = "grey--text">Target Representation/Coordinates</v-card-text>
        <v-flex xs12>
          <v-card-text align = "left" class = "grey--text">Current Position: </v-card-text>
        </v-flex>
        <v-layout row wrap>
            <v-flex xs3>
              <v-card-text class = "teal--text">X: {{ this.x_curr.toPrecision(4) }}</v-card-text>
            </v-flex>
            <v-flex xs3>
              <v-card-text class = "teal--text">Y: {{ this.y_curr.toPrecision(4) }}</v-card-text>
            </v-flex>
            <v-flex xs3>
              <v-card-text class = "teal--text">Z: {{ this.z_curr.toPrecision(4) }}</v-card-text>
            </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
    <v-flex xs7>
      <v-card class = "secondary ma-2">
        <v-card-text>Target List</v-card-text>
        <v-flex xs10 offset-xs1>
          <v-data-table v-if = 'items.length > 0'
            :headers = 'table_headers'
            :items = 'items'
            class = "elevation-1"
          >
            <template slot = 'items' scope = 'props'>
              <td>
                <router-link
                  :to = "{ name: 'target', params:{ id: props.item._id }}">
                  {{ props.item.number }}
                </router-link>
              </td>
              <td>{{ props.item._id }}</td>
              <td>{{ props.item.numImages }}</td>
            </template>
          </v-data-table>
          <v-card-text class = "text-xs-center white--text" v-else>
            There are no targets currently associated with this dish.
            Add one using the card to the right.
          </v-card-text>
        </v-flex>
      </v-card>
    </v-flex>
    <v-flex xs5>
      <v-card class = "secondary ma-2">
        <v-card-text>Controls</v-card-text>
        <v-flex xs12>
          <v-btn fab outline dark small class = "teal"
            @click.native = 'move(this.x_curr, this.y_curr + 1, this.z_curr)'>
            <v-icon dark>arrow_upward</v-icon>
          </v-btn>
        </v-flex>
        <v-flex xs12>
          <span class = "group">
            <v-btn fab outline dark small class = "teal"
              @click.native = 'move(this.x_curr - 1, this.y_curr, this.z_curr)'>
              <v-icon dark>arrow_back</v-icon>
            </v-btn>
            <v-btn fab outline dark small class = "teal"
              @click.native = 'move(0, 0, 0)'>
              <v-icon dark>home</v-icon>
            </v-btn>
            <v-btn fab outline dark small class = "teal"
              @click.native = 'move(this.x_curr + 1, this.y_curr, this.z_curr)'>
              <v-icon dark>arrow_forward</v-icon>
            </v-btn>
          </span>
        </v-flex>
        <v-flex xs12>
          <v-btn fab outline dark small class = "teal"
            @click.native = 'move(this.x_curr, this.y_curr - 1, this.z_curr)'>
            <v-icon dark>arrow_downward</v-icon>
          </v-btn>
        </v-flex>
        <v-flex xs12>
          <v-text-field
            v-model = 'x_cord'
            name = "input-1"
            label = "X Coordinate"
            hint = "Required"
            dark
            required></v-text-field>
          <v-text-field
            v-model = 'y_cord'
            name = "input-2"
            label = "Y Coordinate"
            hint = "Required"
            dark
            required></v-text-field>
          <v-text-field
            v-model = 'z_cord'
            name = "input-3"
            label = "Z Coordinate"
            hint = "Required"
            dark
            required></v-text-field>
          <v-text-field
            v-model = 'time'
            name = "input-4"
            label = "Total Time"
            hint = "Required"
            dark
            required></v-text-field>
          <v-text-field
            v-model = 'interval'
            name = "input-5"
            label = "Interval"
            hint = "Required"
            dark
            required></v-text-field>
        </v-flex>
        <v-btn outline fab class = "teal--text" @click.native='add_target()'>Add Target</v-btn>
      </v-card>
    </v-flex>
  </v-layout>

</template>



<script>

  export default {

    props: ['id'],

    data() {
      return {
        table_headers: [
          { text: 'Target Number', left: true, value: 'number' },
          { text: 'Target ID', left: true, value: '_id' },
          { text: 'Number of Images', left: true, value: 'numImages' }
        ],
        x_cord: null,
        y_cord: null,
        z_cord: null,
        time: null,
        interval: null,
        error_message: '',
        show_message: false,
        x_curr: null,
        y_curr: null,
        z_curr: null
      }
    },

    computed: {

      items() {
        return this.$store.state.current_camera['targets']
      }
    },

    methods: {

      add_target() {
        if (!this.x_cord || !this.y_cord || !this.z_cord
                                         || !this.time || !this.interval) {
                                           debugger;
          this.error_message = "The target must have valid coordinates."
          this.show_message = true
        }
        else {
          var target_data = {
            cords: {
              x: this.x_cord,
              y: this.y_cord,
              z: this.z_cord
            },
            id: this.id,
            interval: this.interval,
            time: this.time,
            cmd: 'add'
          }
          this.$store.dispatch('add_target', target_data)
        }
      },

      move(x_in, y_in, z_in) {
        var move_cords = {
          x: x_in,
          y: y_in,
          z: z_in,
          id: this.id,
          cmd: 'move'
        }
        this.$store.dispatch('move_camera', move_cords)
        // Update local coordinates.
        this.x_curr = this.$store.state.coordinates['x']
        this.y_curr = this.$store.state.coordinates['y']
        this.z_curr = this.$store.state.coordinates['z']
      }
    },

    mounted() {

      this.$store.dispatch('get_camera', this.id)
      this.x_curr = this.$store.state.coordinates['x']
      this.y_curr = this.$store.state.coordinates['y']
      this.z_curr = this.$store.state.coordinates['z']
    }
  }

</script>
