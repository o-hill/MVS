<template>
  <div>
    <v-card>
      <v-card-text>
        <div>{{ card_text }}</div>
      </v-card-text>
    </v-card>

    <v-card class = "blue darken-1 white--text mt-3">
      <v-card-text>
        <div>{{ card_text }}</div>
      </v-card-text>
    </v-card>
  </div>
</template>


<script>

  export default {

    data () {
      return {
        card_text: "This is the text in the card"
      }
    }
  }

</script>
