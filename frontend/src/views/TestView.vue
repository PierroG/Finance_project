<template>
  <div>
    <button @click="fetchHistoricalData">Fetch Historical Data</button>
    <button @click="connectRealtimeSocket">Connect Realtime Socket</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      socket: null,
    };
  },
  unmounted() {
    if (this.socket != null) {
      console.log("try to close socket")
      this.socket.close()
    }
   
  },
  methods: {
    fetchHistoricalData() {
      axios.get('http://localhost:6500/historical/BTCUSDT')
        .then(response => {
          // Process the response data
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    connectRealtimeSocket() {
      const socket = new WebSocket('ws://localhost:6500/realtime/BTCUSDT');
      this.socket = socket
      socket.onopen = () => {
        console.log('WebSocket connected');
      };
      
      socket.onmessage = event => {
        // Process the real-time data received
        console.log(event.data);
      };
      
      socket.onerror = error => {
        // this.socket = null;
        console.error(error);
      };
      
      socket.onclose = () => {
        // this.socket = null;
        console.log('WebSocket disconnected');
      };
    }
  }
};
</script>

<style lang="scss" scoped>
button {
	border: none;
	outline: none;
  padding: 6px 10px;
  margin: 1rem;
	background: white;

  &:hover{
    background: rgb(207, 207, 207);
  }
}
</style>