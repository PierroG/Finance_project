<template>
  <div>
    <div class="search-container">
      <input
        type="text"
        v-model="searchTerm"
        @blur="closeDropdown"
        placeholder="Search ticker..."
        @focus="openSearch"
      />
      
      <button>
        <span class="material-icons">search</span>
      </button>
    </div>

    <div v-if="isDropdownOpen" class="dropdown">
      <ul>
        <li class="crypto" v-for="(ticker, index) in filteredTickers" :key="index" @click="selectTicker(ticker.symbol)">
          <img class="cryptoLogo" :src="getSvgPath(ticker.symbol)" alt="" />
          {{ ticker.symbol }} | {{ ticker.price }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchTerm: '',
      Tickers: [],
      isDropdownOpen: false,
      filenames: null
    };
  },
  computed: {
    filteredTickers() {
      return this.Tickers.filter(ticker =>
        ticker.symbol.toLowerCase().startsWith(this.searchTerm.toLowerCase())
        // includes
      ).slice(0,50);
    }
  },
  mounted() {
    let filenames =  import.meta.glob('@/assets/cryptologos-svg/*.svg',);
    this.filenames = Object.keys(filenames).map((key) => {
        // Extract the name from the key
        const matches = key.match(/\/([^/]+)\.svg$/);
        return matches ? matches[1] : '';
    });
    console.log(this.filenames)
  },
  methods: {
    getSvgPath(symbol) {
      const matchingFilename = this.findMatchingFilename(symbol);
      if (matchingFilename) {
        return `src/assets/cryptologos-png/${matchingFilename}.png`;
      }
      // Return a default SVG path if no match is found
      return 'src/assets/cryptologos-png/default.png';
    },
    findMatchingFilename(symbol) {
      // const filenames = require.context('@/assets/cryptologos-svg', false, /\.svg$/).keys();
      const matchingFilename = this.filenames.find(filename => symbol.startsWith(filename));
      return matchingFilename;
    },
    openSearch() {
      this.openDropdown()
      if (!this.Tickers.length > 0) {
        this.fetchTickers()
        
      }
    },

    fetchTickers() {
      console.log("fetch")
      // Simulate API request to fetch Tickers
      // Replace 'your-api-url' with the actual API URL

      fetch('http://localhost:6500/tickers')
        .then(response => response.json())
        .then(data => {
          console.log(data)
          this.Tickers = data
          // this.Tickers = this.Tickers.sort((tickerA, tickerB) => {
          //   // Sort by ticker.price in ascending order
          //   return tickerB.price - tickerA.price;
          // });
          this.isDropdownOpen = true;
        })
        .catch(error => {
          console.error(error);
        });
    },
    selectTicker(symbol) {
      console.log("select");
      console.log(symbol);
      // this.searchTerm = symbol;
      this.$emit('select', symbol)
      // this.isDropdownOpen = false;
    },
    openDropdown() {
      this.isDropdownOpen = true;
    },
    closeDropdown() {
      console.log("ici")
      setTimeout(() => {
        this.isDropdownOpen = false;

      }, 100)
    }
  }
};
</script>

<style lang="scss">
.search-container {
  position: relative;
  background-color: black;
  border-radius: 2rem;
  display: flex;
  overflow: hidden;

  input {
    flex: 1;
    padding: .7em;
    background-color: transparent;
    border: inherit;
    color: white;
    font-size: 1em;
    &:focus {
      outline: none;
    }
  }

  button {
    padding: 0 1em;
    color: rgba(255, 255, 255, 0.7);

    // &:hover {
    //   color: white
    //   background-color: rgba(255, 255, 255, 0.1);
    // }
    span {
      position: relative;
      top: 2px;

    }
  }
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  // background-color: #313131;
  background-color: #000000;
  border: 1px solid #1b1b1b;
  color: white;
  border-top: none;
  padding: 10px;
  border-radius: 15px;
  z-index: 500;
  max-height: 500px;
  overflow-y: scroll;
}

.dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown li {
  padding: 5px;
  cursor: pointer;
}

.dropdown li:hover {
  background-color: rgb(255, 255, 255, .1);
}

.crypto {
  display: flex;
  align-items: center;
}

.cryptoLogo {
  width: 1rem;
  height: 1rem;
  margin-right: 6px;
}

</style>
