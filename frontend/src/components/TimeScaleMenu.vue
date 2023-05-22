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
        scales: ['1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M']
      };
    },
    mounted() {
        console.log("mounted")
        this.$nextTick(() => {
            document.addEventListener('click', this.handleOutsideClick);
        })
    },
    unmounted() {
        document.removeEventListener('click', this.handleOutsideClick);
    },
    methods: {
        selectTimeScale(timeScale) {
          this.$emit('close');
          this.$emit('select', timeScale);

        },
        handleOutsideClick(event) {
            if (!this.$el.contains(event.target)) {
                this.$emit('close');
                console.log("outside click")
            }
        }
    }
  }
  </script>
  
  <style scoped>
 .time-scale-menu {
  z-index: 500;
  position: absolute;
  top: 40px;
  left: 0;
  background-color: #1f1f1f;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
}

.time-scale-menu ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.time-scale-menu ul li {
  cursor: pointer;
  padding: 4px 8px;
}

.time-scale-menu ul li:hover {
  background-color: #363636;
}
  </style>
  