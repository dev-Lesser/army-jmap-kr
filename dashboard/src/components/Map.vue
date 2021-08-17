<template>
    <div id="map" style="width:100%; height:800px;" class="container"></div>
</template>
<script>
import * as maptalks from "maptalks";
// import { ThreeLayer } from 'maptalks.three';
import marker from '@/assets/company.png'
import '../../node_modules/maptalks/dist/maptalks.css';
export default {
    setup() {
        
    },
    mounted(){
        var map = new maptalks.Map("map", {
            center: [127, 37.498568],
            zoom: 10,
             baseLayer: new maptalks.TileLayer('base', {
            'urlTemplate' : 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
            'subdomains'  : ['a','b','c','d'],

            })
        });
        // const layer = new ThreeLayer('three');
        // var center = map.getCenter();

        var layer = new maptalks.VectorLayer('vector').addTo(map);
        for (var i of this.$store.state.tableData.result){
            console.log(i.latitude.String, i.longitude.String)
            var marker1 = new maptalks.Marker(
        [i.longitude.String, i.latitude.String, ],
        {
          'symbol' : {
            'markerFile'   : marker,
            'markerWidth'  : 28,
            'markerHeight' : 28,
            'markerDx'     : 0,
            'markerDy'     : 0,
            'markerOpacity': 1
          }
        }).addTo(layer);
        }
        
      
      marker1;
        console.log(map)
    }
}
</script>
<style scoped>
@import "../../node_modules/maptalks/dist/maptalks.css";
</style>