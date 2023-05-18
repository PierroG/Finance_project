<template>
  <div class="app">
    <Sidebar />
    <router-view />
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
export default {
  components: {
    Sidebar
  },
  data() {
    return {
      name: 'John',
    };
  },
  methods: {
    doIt() {
      console.log(`Hello ${this.name}`);
    },
  },
  mounted() {
    this.doIt();
  },
};
</script>


<style lang="scss">
:root {
	// --primary: #4ade80;
	--primary: #4aa8de;

	--primary-alt: #22c55e;
	--grey: #64748b;
	--dark: #1e293b;
	--darker: #131b25;
	--dark-alt: #334155;
	--light: #f1f5f9;
	--sidebar-width: 300px;
}

// :root {
// 	--primary: #4aa8de;
// 	--primary-alt: #22c5c5;
// 	--grey: #64748b;
// 	--dark: #292f38;
// 	--darker: #1f2429;
// 	--dark-alt: #334155;
// 	--light: #f1f5f9;
// 	--sidebar-width: 300px;
// }

// :root {
// 	// --primary: #4ade80;
// 	--primary: #256dda;

// 	--primary-alt: #22c55e;
// 	--grey: #64748b;
// 	--dark: #1e293b;
// 	--darker: #0e101b;
// 	--dark-alt: #334155;
// 	--light: #f1f5f9;
// 	--sidebar-width: 300px;
// }

body {
	background: var(--darker);
  color: var(--light);
}

button {
	cursor: pointer;
	appearance: none;
	border: none;
	outline: none;
	background: none;
}

.app {
  display: flex;
  margin: 0px;
  padding: 0px;
  
  main {
    flex: 1 1 0;
    // padding: 2rem;

    @media (max-width: 768px) {
      padding-left: 6rem;
    }
  }
}


</style>
