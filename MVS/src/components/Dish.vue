<template>
  <v-layout row wrap>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text ma-3">Live Video Feed</h5>
        </v-card-text>
        <v-card-media class = "ma-3">
          <img src = 'http://0.0.0.0:1493/video_feed' height = "350" width = "500">
        </v-card-media>
      </v-card>
    </v-flex>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text ma-3">Target Representation/Coordinates</h5>
        </v-card-text>
        <v-flex xs12>
          <svg width = "350" height = "350">
            <circle cx = "175" cy = "175" r = "175"
            style = "fill:#737373"></circle>
          </svg>
        </v-flex>
        <v-flex xs12>
          <v-card-text align = "left" class = "grey--text">Current Position: </v-card-text>
        </v-flex>
        <v-layout row wrap>
            <v-flex xs3>
              <v-card-text class = "teal--text">X: {{ cords.x.toPrecision(4) }}</v-card-text>
            </v-flex>
            <v-flex xs3>
              <v-card-text class = "teal--text">Y: {{ cords.y.toPrecision(4) }}</v-card-text>
            </v-flex>
            <v-flex xs3>
              <v-card-text class = "teal--text">Z: {{ cords.z.toPrecision(4) }}</v-card-text>
            </v-flex>
        </v-layout>
        <v-flex xs12>
          <v-btn fab outline class = "teal--text" @click.native = 'start_manual()'>Manual Mode</v-btn>
        </v-flex>
      </v-card>
    </v-flex>
    <v-flex xs7>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text ma-3">Target List</h5>
        </v-card-text>
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
              <td>
		            <v-btn icon='icon' dark small class='grey lighten-1'
		              @click.native='start_interval(props.item._id)'>
		              <v-icon>photo_camera</v-icon>
		            </v-btn>
		          </td>
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
        <v-card-text>
          <h5 class = "grey--text ma-3">Controls</h5>
        </v-card-text>
        <v-layout row wrap v-if = 'manual'>
          <v-flex xs12>
            <v-btn fab outline dark small class = "teal"
              @click.native = 'move(cords.x, cords.y + 1, cords.z)'>
              <v-icon dark>arrow_upward</v-icon>
            </v-btn>
          </v-flex>
          <v-flex xs12>
            <span class = "group">
              <v-btn fab outline dark small class = "teal"
                @click.native = 'move(cords.x - 1, cords.y, cords.z)'>
                <v-icon dark>arrow_back</v-icon>
              </v-btn>
              <v-btn fab outline dark small class = "teal"
                @click.native = 'move(0, 0, 0)'>
                <v-icon dark>home</v-icon>
              </v-btn>
              <v-btn fab outline dark small class = "teal"
                @click.native = 'move(cords.x + 1, cords.y, cords.z)'>
                <v-icon dark>arrow_forward</v-icon>
              </v-btn>
            </span>
          </v-flex>
          <v-flex xs12>
            <v-btn fab outline dark small class = "teal">
              <v-icon dark>arrow_downward</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
        <v-layout row wrap v-else>
          <v-flex xs12>
            <v-btn fab outline dark small disabled class = "teal">
              <v-icon dark>arrow_upward</v-icon>
            </v-btn>
          </v-flex>
          <v-flex xs12>
            <span class = "group">
              <v-btn fab outline dark small disabled class = "teal">
                <v-icon dark>arrow_back</v-icon>
              </v-btn>
              <v-btn fab outline dark small disabled class = "teal">
                <v-icon dark>home</v-icon>
              </v-btn>
              <v-btn fab outline dark small disabled class = "teal">
                <v-icon dark>arrow_forward</v-icon>
              </v-btn>
            </span>
          </v-flex>
          <v-flex xs12>
            <v-btn fab outline dark small disabled class = "teal">
              <v-icon dark>arrow_downward</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
        <v-flex xs12>
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
        time: null,
        interval: null,
        error_message: '',
        show_message: false
      }
    },

    computed: {

      items() {
        return this.$store.state.current_camera['targets']
      },

      cords() {
        return this.$store.state.coordinates
      },

      manual() {
        return this.$store.state.manual_mode
      }
    },

    methods: {

      add_target() {
        if (!this.time || !this.interval) {
          this.error_message = "The target must have valid time and intervals."
          this.show_message = true
        }
        else {
          var target_data = {
            cords: {
              x: cords.x,
              y: cords.y,
              z: cords.z
            },
            id: this.id,
            interval: this.interval,
            time: this.time,
            cmd: 'add'
          }
          this.$store.dispatch('add_target', target_data)
        }
      },

      start_manual() {
        var manual_data = {
          id: this.id,
          cmd: 'manual'
        }
        this.$store.dispatch('start_manual', manual_data)
      },

      start_interval(target_id) {
        var start_data = {
          cmd: 'start',
          target_id: target_id
        }
        this.$store.dispatch('start_target', start_data)
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
      }
    },

    mounted() {
      this.$store.dispatch('get_camera', this.id)
    }
  }

</script>
