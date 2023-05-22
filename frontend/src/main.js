import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.directive('click-outside', {
    beforeMount(el, binding) {
      el.clickOutsideEvent = (evt) => {
        evt.stopPropagation();
        if (!(el === evt.target || el.contains(evt.target))) {
          binding.value(evt, el);
        }
      };
      window.requestAnimationFrame(() => {
        document.addEventListener("click", el.clickOutsideEvent);
      });
    },
    unmounted(el) {
      document.removeEventListener("click", el.clickOutsideEvent);
    },
  });

app.use(router)

app.mount('#app')


