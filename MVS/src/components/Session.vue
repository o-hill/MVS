<template>
  <div>
    <v-container xs12 fluid class = "text-xs-center">
      <v-layout row wrap>
        <v-flex xs2>
          <v-card class = "secondary">
            <v-card-text class = "white--text">Add a dish</v-card-text>
            <v-btn outline fab class="teal--text" @click.native='add_camera(0)'>One</v-btn>
            <v-btn outline fab class = "blue--text" @click.native='add_camera(1)'>Two</v-btn>
            <v-btn outline fab class = "indigo--text" @click.native='add_camera(2)'>Three</v-btn>
            <v-btn outline fab class = "red--text" @click.native='add_camera(3)'>Four</v-btn>
          </v-card>
        </v-flex>
        <v-flex xs10>
          <v-card fluid class = "secondary">
            <v-card-text class = "grey--text">Active Dishes</v-card-text>
            <v-flex xs10 offset-xs1>
              <v-data-table v-if = 'items.length > 0'
                :headers = 'table_headers'
                :items = 'items'
                class = "elevation-1"
              >
                <template slot = 'items' scope = 'props'>
                  <td>
                    <router-link
                      :to = "{ name: 'camera', params:{ id: props.item._id }}">
                      {{ props.item.source }}
                    </router-link>
                  </td>
                  <td>{{ props.item._id }}</td>
                  <td>{{ props.item.numTargets }}</td>
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

    props: ['id'],

    data() {
      return {
        table_headers: [
          { text: 'Dish Number', left: true, value: 'source' },
          { text: 'Dish ID', left: true, value: '_id' },
          { text: 'Number of Targets', left: true, value: 'numTargets' }
        ]
      }
    },

    computed: {

      items() {
        return this.$store.state.current_session['cameras']
      }
    },

    methods: {

      add_camera(src) {
        var camera_data = {
          source: src,
          id: this.id,
          cmd: 'add'
        }
        this.$store.dispatch('add_camera', camera_data)
      }
    },

    mounted() {

      this.$store.dispatch('get_session', this.id)
    }
  }


</script>




<style>

</style>
