<template>


  <v-layout row wrap>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text">Schedule</h5>
        </v-card-text>
        <v-flex xs12>
          <v-card-text align = "left" class = "grey--text">Coordinates: </v-card-text>
        </v-flex>
        <v-layout row wrap>
          <v-flex xs3>
            <v-card-text class = "teal--text">X: {{ cords.x }}</v-card-text>
          </v-flex>
          <v-flex xs3>
            <v-card-text class = "teal--text">Y: {{ cords.y }}</v-card-text>
          </v-flex>
          <v-flex xs3>
            <v-card-text class = "teal--text">Z: {{ cords.z }}</v-card-text>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>
          <h5 class = "grey--text">Latest Image</h5>
        </v-card-text>
        <v-card-media>
          <img src = latest_image height = "200" width = "350" v-if = 'latest_image != null'>
          <v-card-text v-else class = "teal--text">No images to display yet!</v-card-text>
        </v-card-media>
        <v-card-media>
          <v-btn fab outline class = "teal--text" @click.native = 'reload()'>Reload</v-btn>
        </v-card-media>
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
      }
    },

    computed: {

      cords() {
        return this.$store.state.coordinates
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
