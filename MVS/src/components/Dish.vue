<template>
  <v-layout row wrap>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>Live Video Feed</v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs6>
      <v-card class = "secondary ma-2">
        <v-card-text>Target Representation/Coordinates</v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs7>
      <v-card class = "secondary ma-2">
        <v-card-text>Target List</v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs5>
      <v-card class = "secondary ma-2">
        <v-card-text>Controls</v-card-text>
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
        ]
      }
    },

    methods: {

      add_target() {
        debugger;
      }
    },

    mounted() {

      this.$store.dispatch('get_camera', this.id)
      debugger;
    }
  }

</script>
