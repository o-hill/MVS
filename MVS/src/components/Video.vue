<template>
  <div>
    <v-layout row wrap>
       <v-flex
        xs6
        v-for = "card in cards"
        :key = "card"
      >
        <v-card class = "primary">
          <v-card-text>{{ card.title }}</v-card-text>
          <img :src = "card.src" height = "200" width = "350">
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>


<script>

  export default {
    data: () => ({
      cards: [
        { title: 'Camera 1', src: 'http://0.0.0.0:1492/video_feed', flex: 6, key: 0 },
        { title: 'Camera 2', src: 'http://0.0.0.0:1493/microscope_feed', flex: 6, key: 1 }
      ]
    })
  }

</script>
