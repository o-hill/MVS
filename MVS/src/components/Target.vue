<template>


  <v-layout row wrap>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text">Schedule</h5>
        </v-card-text>
        <v-flex xs12>
          <v-card-text align = "left" class = "grey--text">
            Timing:
          </v-card-text>
        </v-flex>
        <v-layout row wrap>
          <v-flex xs5>
            <v-card-text class = "teal--text">
              Total Time (seconds): {{ time }}
            </v-card-text>
          </v-flex>
          <v-flex xs5>
            <v-card-text class = "teal--text">
              Interval (seconds): {{ interval }}
            </v-card-text>
          </v-flex>
          <v-flex xs5>
            <v-card-text class = "teal--text">
              Elapsed Time (seconds): {{ end - start }}
            </v-card-text>
          </v-flex>
        </v-layout>
        <v-flex xs12>
          <v-card-text align = "left" class = "grey--text">
            Coordinates:
          </v-card-text>
        </v-flex>
        <v-layout row wrap>
          <v-flex xs3>
            <v-card-text class = "teal--text">
              X: {{ cords.x.toPrecision(4) }}
            </v-card-text>
          </v-flex>
          <v-flex xs3>
            <v-card-text class = "teal--text">
              Y: {{ cords.y.toPrecision(4) }}
            </v-card-text>
          </v-flex>
          <v-flex xs3>
            <v-card-text class = "teal--text">
              Z: {{ cords.z.toPrecision(4) }}
            </v-card-text>
          </v-flex>
          <v-flex xs12>
            <v-btn fab outline class = "red--text" @click.native = 'debug()'>
              Debug
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text">Latest Image</h5>
        </v-card-text>
        <v-flex xs12>
          <v-card-media>
            <img src = latest_image height = "200" width = "350"
              v-if = 'latest_image.length > 0'>
            <v-card-text v-else class = "red--text">
              No images to display yet!  Start the time lapse in the
              camera module.
            </v-card-text>
          </v-card-media>
        </v-flex>
        <v-flex xs12>
          <v-card-media>
            <v-btn fab outline class = "teal--text" @click.native = 'reload()'>
              Reload
            </v-btn>
          </v-card-media>
        </v-flex>
      </v-card>
    </v-flex>
    <v-flex xs12>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text">Notes</h5>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>


</template>


<script>


  export default {

    props: ['id'],

    data() {
      return {

      }
    },

    methods: {

      reload() {
        this.$store.dispatch('get_target', this.id)
      },

      debug() {
        debugger;
      }
    },

    computed: {

      cords() {
        return this.$store.state.coordinates
      },

      time() {
        return this.$store.state.current_target['time']
      },

      start() {
        return this.$store.state.current_target['start']
      },

      end() {
        return this.$store.state.current_target['end']
      },

      interval() {
        return this.$store.state.current_target['interval']
      },

      latest_image() {
        return this.$store.state.latest_image
      }
    },

    mounted() {
      this.$store.dispatch('get_target', this.id)
    }
  }


</script>
