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
      
      <button @click="console.log('click')">
        <span class="material-icons">search</span>
      </button>
    </div>

    <div v-if="isDropdownOpen" class="dropdown">
      <ul>
        <li v-for="(ticker, index) in filteredTickers" :key="index" @click="selectCity(city)">
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
      isDropdownOpen: false
    };
  },
  computed: {
    filteredTickers() {
      return this.Tickers.filter(ticker =>
        ticker.symbol.toLowerCase().startsWith(this.searchTerm.toLowerCase())
        // includes
      );
    }
  },
  methods: {
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
          this.Tickers = data;
          this.isDropdownOpen = true;
        })
        .catch(error => {
          console.error(error);
        });
    },
    selectCity(city) {
      this.searchTerm = city.name;
      this.isDropdownOpen = false;
    },
    openDropdown() {
      this.isDropdownOpen = true;
    },
    closeDropdown() {
      this.isDropdownOpen = false;
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
  background-color: #313131;
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

</style>
