<template>
  <v-app-bar
      app
      color="blue-grey darken-3"
      dark
    >
      <v-card-title>전문연구요원 회사</v-card-title>
    </v-app-bar>
</template>

<script>
import axios from 'axios'
  export default {
    data: () => ({
      
    }),
    async mounted(){
      var res = await axios('http://localhost:9999/companies');
      this.$store.state.tableData = res.data
    }
  }
</script>
