<!-- TimeScaleMenu.vue -->
<template>
    <div class="time-scale-menu" ref="menuRef">
      <ul>
        <li v-for="scale in scales" :key="scale" @click="selectTimeScale(scale)">{{ scale }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        scales: ['1min', '5min', '30min', '1h', '2h', '6h', '12h', '1d', '3d', '1w', '2w', '1M']
      };
    },
    mounted() {
    },
    unmounted() {
    },
    methods: {
        selectTimeScale(timeScale) {
          this.$emit('close');
          this.$emit('select', timeScale);

        },
    }
  }
  </script>
  
  <style lang='scss' scoped>

  </style>
  