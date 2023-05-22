<!-- TimeScaleMenu.vue -->
<template>
    <div >
      <span @click="toggleMenu" class="button" :class="isMenuOpen ? 'open' : ''">indicators</span>
      <div v-if="isMenuOpen" class="menu" ref="menuRef">
        <ul v-show="selectedIndicatorIndex==null">
          <li v-for="(indicator, index) in indic" :key="indicator" @click="selectIndicator(index)">
            {{ indicator.name }}
            <!-- <span class="material-icons star"  @click.stop="() => {}">star_border</span> -->
          </li>
        </ul>
        <div v-show="selectedIndicatorIndex!=null" class="optionMenu">
          <div style="display: flex">
            <span class="material-icons back-button"  @click="() => {this.selectedIndicatorIndex=null;}">arrow_back</span>
            <span>{{ selectedIndicator.name }}</span>
          </div>

          <div v-for="(option, index) in selectedIndicator.option" :key="index">

            {{ option.name }}:  
            <input type="number" v-model="optionValues[option.name]" style="display: inline; width: 4rem;">
           
          </div>
          <button class="add-button" @click="add(selectedIndicator.name, optionValues)">add</button>
          <!-- <div v-for="(option, index) in indidactorOption" :key="index">
            -------------
            {{  option  }} {{  index  }}
          </div> -->
        </div>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      indicators: ['EMA', 'EMA Double', 'EMA triple'],
      indic: [
        {
          name: 'EMA',
          option: [
            {
              name: 'timeperiod',
              default: 14
            }
          ]
        },
        {
          name: 'EMA Double',
          option: [
            {
              name: 'timeperiod',
              default: 14
            }
          ]
        },
        {
          name: 'EMA triple',
          option: [
            {
              name: 'timeperiod',
              default: 14
            }
          ]
        }
      ],
      optionValues: {},
      selectedIndicatorIndex: null,
      isMenuOpen: false,
      currentIndicator: [
        {

        }
      ],
    };
  },
  mounted() {
  },
  unmounted() {
  },
  computed: {
    selectedIndicator() {
      if (this.selectedIndicatorIndex == null) {
        return {}
      }
      return this.indic[this.selectedIndicatorIndex]
    },
    selectedIndicatorOptions() {
      return this.selectedIndicator.option.map(option => option.default || 10);
    },
  },
  methods: {
    removeSeries(index) {
      // this.lineSeries.splice(index, 1);
      console.log("remove")
    },
    add(indicator, optionValues) {
      console.log("emit for:" + indicator)
      console.log("optionValue:" + this.optionValues)
      this.$emit('add', indicator, JSON.stringify(this.optionValues))
    },
    doStuff() {
      console.log("doStuff")
    },
    toggleMenu() {
      if (this.isMenuOpen == false) {
        this.isMenuOpen = true;
        console.log("open")
        document.addEventListener('click', this.handleOutsideClick);
      }
      else {
        this.isMenuOpen = false;
        console.log("close")
        document.removeEventListener('click', this.handleOutsideClick);
      }
    },
    selectIndicator(index) {
      console.log(index)
      this.selectedIndicatorIndex = index;
      this.selectedIndicator.option.forEach(option => {
        this.optionValues[option.name] = option.default;
      });
    },
    handleOutsideClick(event) {
        if (!this.$el.contains(event.target)) {
          this.toggleMenu()
        }
    }
  }
}
</script>

<style lang="scss" scoped>
.button {
  padding: 5px;
  border-radius: 3px;
  cursor: pointer;
  user-select: none;

  &:hover {
    background-color: rgb(255, 255, 255, .35);
  }
  &.open{
    background-color: rgb(255, 255, 255, .35);
  }
}
.menu {
  min-width: 160px;
  z-index: 10;
  position: absolute;
  top: 30px;
  left: 0;
  background-color: #1e293b;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;

    li{
      cursor: pointer;
      padding: 4px 8px;
      display: flex;
      justify-content: space-between;

      &:hover{
        background-color: rgba(0, 0, 0, 0.35);

        .star {
          color: rgba(255, 255, 255, 0.5);
        }

      }

      .star {
        color: #1e293b;

        &:hover{
          color: red;
        }
      }
    }
  }
}
.optionMenu {
  display: flex;
  flex-direction: column;
  div {
    padding: 2px;
  }
}
.back-button {
  cursor: pointer;

  &:hover{
        background-color: rgba(255, 255, 255, 0.35);

      }
}

.add-button {
  flex-grow: 0;
  align-items: center;
  color: green;
  padding: 2px;
  border: solid green 2px;
  border-radius: 3px;
  align-self: center;
}
</style>
  