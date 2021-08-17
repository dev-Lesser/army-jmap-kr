<template>
    <v-container fluid grid-list-md>
        <v-layout wrap style="display:flex;justify-content:center;">
            <v-flex xs12 sm12 md12>
                <Map />
                
                
            </v-flex>
                
   
          
        </v-layout>
    </v-container>
</template>
<script>
import Map from "@/components/Map"
export default {
    components:{
        Map
    },
    setup() {
        
    },
}
</script>