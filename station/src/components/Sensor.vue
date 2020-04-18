<template>
  <div class="sensor" v-on:click="paused ^= 1; updateStatus();" >
    Sensor type:{{ type }} Status:{{ status }} 
      <p/>
       <div class="meassure" v-for="item in sensordata" :key="item.measure">
            <div v-on:click="track(item.measure)">{{item.measure}}: {{ item.value }} </div>

      </div>

    
  <CChartLine
    style="height:300px" v-bind:datasets="cdata"    
    :options="{ maintainAspectRatio: false,  
                borderWidth: 10, 
                backgroundColor: '#000000' }"
  />
  </div>
</template>

<script>
const refreshPeriod = 100;
import axios from "axios";
export default {
  name: "Sensor",
  props: {
    type: String,
    endpoint: String
  },
  data: () => {
    return { 
      status: "",
      sensordata: {} ,
      cdata: [{ data:[], label:"" }],
      chartlen: 250,
      trackmeasure: "Presión",
      paused: 0
    };
  },
  mounted() {
    this.updateStatus();
  },
  methods: {
    updateStatus: function() {
      axios
        .get(this.endpoint)
        .then(res => {
          var measures=[];
          for (var measure in res.data) {
            //console.log(measure) ;
            //console.log(res.data[measure]) ;
            measures.push( { 'measure': measure, 'value' : res.data[measure]} )
            if (measure == this.trackmeasure ) {              
              if (this.cdata[0].data.length > this.chartlen ) {                 
                this.cdata[0].data.shift() 
                }
              this.cdata[0].data.push(res.data[measure]) ;
              
            }
          }
          this.sensordata = measures ;
          this.status = "OK " + ( (this.paused == 1) ? "Paused" : "" );
          
        })
        .catch(error => (this.status = error));      
      if (this.paused != 1 ) {
        setTimeout(() => this.updateStatus(), refreshPeriod);
      }
    },

    track: function(measure) {
      console.log("Now tracking " + measure);
      this.trackmeasure=measure;
      this.cdata[0].label=measure ;
      this.cdata[0].data=[];
    }
  }
};

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 0 10px;
}
a {
  color: #42b983;
}
.sensor {
  float: left;
}
.meassure{
  font-size: 14px;
  float:left;
  padding: 5px 5px 5px 5px;
}
</style>
