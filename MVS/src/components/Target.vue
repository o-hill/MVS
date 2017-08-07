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
        <v-btn @click.native = 'move()'>Debug</v-btn>
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

      move() {
        debugger;
      }
    },

    computed: {

      cords() {
        return this.$store.state.coordinates
      }
    },

    mounted() {
      this.$store.dispatch('get_target', this.id)
    }
  }


</script>
