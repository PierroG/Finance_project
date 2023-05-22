<template>
  <div class="ChartView">
    <SearchBar @select="initSymbol"/>
    <h1>This is a Chart page</h1>
    <div class="chart-layout">
      <div id='ici' class="button-container">
        <div class="timescale-selector-container">
          <span >Time Scale</span>
          <span class="timescale_btn" ref="timescale" @click.stop="toggleTimeScaleMenu">
            {{ selectedTimeScale }}
            <span class="material-icons">expand_more</span>
            <time-scale-menu
              v-if="isTimeScaleMenuOpen"
              @select="setTimeScale"
              @close="closeTimeScaleMenu"
          ></time-scale-menu>
          </span>
        </div>

        <span class="separator"></span>
        <button title="Fit content" class="material-icons" style="font-size: 1.5rem;" @click="fitContent()">fit_screen</button>
        <button title="Reset price scale" class="material-icons" style="font-size: 1.5rem;" @click="resetYAxis()">height</button>
        <span class="separator"></span>
        <div>
        <IndicatorSelector
          @add="computeIndicator"/>
        </div>
        <button @click="deleteSeries">delete</button>
      </div>
      <div id="chart-container"></div>
    </div>
    
    <div class="indicList">
      <div @mouseenter="hoverElem(index)" @mouseleave="unhoverElem(index)" class="indic" v-for="(series, index) in lineSeries_list" :key="index">
        <div class="circle" :style="{ backgroundColor: series.color }"></div>
        <p>{{ series.name }}</p>
        <p>{{ series.options }}</p>
        <!-- <ul>
          <li v-for="(value, key) in series.options" :key="key">
            {{ key }}: {{ value }}
          </li>
        </ul> -->
        <button class="material-icons" @click="deleteSeries(index)">
            close
        </button>
        <!-- Add any other display or control elements you need -->
      </div>

    </div>

  </div>
</template>

<script>
import axios from 'axios';

// https://www.tradingview.com/lightweight-charts/
import { createChart, CrosshairMode, PriceScaleMode } from 'lightweight-charts';
import TimeScaleMenu from '../components/TimeScaleMenu.vue'
import IndicatorSelector from '../components/IndicatorSelector.vue'
import SearchBar from '../components/SearchBar.vue'
export default {
  components: {
    TimeScaleMenu,
    IndicatorSelector,
    SearchBar
  },
  data() {
    return {
      chart: null,
      view: 'day',
      data: null,
      selectedTimeScale: '1d',
      isTimeScaleMenuOpen: false,
      lineSeries: null,
      areaSeries: null,
      series: [],
      lineSeries_list: [],

    };
  },
  methods: {
    randomColor() {
      return '#' + Math.floor(Math.random()*16777215).toString(16);
    },
    async computeIndicator(indicator, option, color) {
      let symbol = 'BTCUSDT'
      let interval = this.selectedTimeScale
      let options = JSON.parse(option)
      await axios.get(`http://localhost:6500/stocks/${symbol}/indicators/${indicator}`, { params: { interval : interval, option:  option }}) //
        .then(response => {
          // Process the response data
          let data = response.data
          console.log(data);
          let color = this.randomColor()
          let newLineSeries = this.chart.addLineSeries({
            color: color,
            lineWidth: 2,
          })
          newLineSeries.setData(data);

          // Push the new line series object into the lineSeries array
          this.lineSeries_list.push({name: indicator, options: options, color: color, serieObject: newLineSeries}); //

        })
        .catch(error => {
          console.error(error);
      });
    },
    deleteSeries(index) {
      console.log(this.lineSeries_list[index].serieObject)
      this.chart.removeSeries(this.lineSeries_list[index].serieObject)
      this.lineSeries_list.splice(index, 1)
    },
    hoverElem(index) {
      console.log("hover")
      this.lineSeries_list[index].serieObject.applyOptions({
        lineWidth: 3
      })
    },
    unhoverElem(index) {
      console.log("hover")
      this.lineSeries_list[index].serieObject.applyOptions({
        lineWidth: 1
      })
    },
    toggleTimeScaleMenu() {
      console.log(this.isTimeScaleMenuOpen);
      this.isTimeScaleMenuOpen = !this.isTimeScaleMenuOpen;
      console.log(this.isTimeScaleMenuOpen);

    },
    async setTimeScale(timeScale) {
      this.selectedTimeScale = timeScale;
      await this.updateChartData('BTCUSDT', timeScale)

    },
    closeTimeScaleMenu() {
      this.isTimeScaleMenuOpen = false;
    },

    fitContent() {
      const chart = this.chart;
      const timeScale = chart.timeScale();
      timeScale.fitContent();
    },
    resetYAxis() {
      const chart = this.chart;
      const priceScale = chart.priceScale();
      chart.priceScale('right').applyOptions({
        autoScale: true,
      });
    },
    async getHistoricalData(symbol, interval) {
      let data = []
      // symbol = 'BTCUSDT'
      await axios.get(`http://localhost:6500/stocks/${symbol}/historical-data`, { params: { interval : interval }})
        .then(response => {
          // Process the response data
          console.log(response.data);
          data = response.data
        })
        .catch(error => {
          console.error(error);
      });
      var dataa = []
      console.log(data.length)
      for (let i = 0; i < data.length; i++) {
        dataa.push({ time: data[i][0]/1000, value: parseFloat(data[i][1])})
      };
      console.log(dataa)
      return dataa
    },
    async getTickers() {
      let data = []
      await axios.get('http://localhost:6500/tickers')
        .then(response => {
          // Process the response data
          console.log(response.data);
          data = response.data
        })
        .catch(error => {
          console.error(error);
      });
      return data
    },

    async initChart() {
      const container = document.getElementById('chart-container');

      this.chart = createChart(container, {
        // width: 1000,
        // height: 600,
        autoSize: true,
        rightPriceScale: {
          visible: true,
          borderVisible: false,
          mode: PriceScaleMode.Normal,
          // borderColor: 'rgba(197, 203, 206, 1)',
        },
        layout: {
          background: {
                type: 'solid',
                color: '#000000',
              },
          textColor: '#d1d4dc',
        },
        grid: {
          horzLines: {
            color: 'rgba(42, 46, 57, 0.5)',
          },
          vertLines: {
            visible: false,
            color: 'rgba(42, 46, 57, 0.5)',
          },
        },
        crosshair: {
          mode: CrosshairMode.Normal,
        },

        timeScale: {
          borderVisible: false,
          borderColor: 'rgba(197, 203, 206, 1)',
          timeVisible: true
        },
        handleScroll: {
          vertTouchDrag: false,
        },

        // vertTouchDrag : false,
      });
      // const line = chart.addLineSeries({
      //   color: 'rgba(4, 111, 232, 1)',
      //   lineWidth: 2,
      // })
      // line.setData(data);
      
    },
    async updateChartData(symbol, interval) {
      if (this.areaSeries!=null) {
        this.chart.removeSeries(this.areaSeries)

      }
      let data = await this.getHistoricalData(symbol, interval);
      this.areaSeries = this.chart.addAreaSeries({
        topColor:    'rgba(41, 98, 255, 0.56)',
        bottomColor: 'rgba(41, 98, 255, 0.04)',
        lineColor:   'rgba(41, 98, 255, 1)',
        lineWidth: 2,
      });
      this.areaSeries.setData(data)

    },
    async initSymbol(symbol) {
      console.log("ini symbol: "+ symbol)
      await this.updateChartData(symbol, '1d')
    },
    setView(view) {
      this.view = view;
      if (view === 'custom') {
        this.setCustomView();
      } else {
        this.updateChartView();
      }
    },
    updateChartView() {
      if (this.chart) {
        console.log(resolution)
        this.chart.timeScale().setVisibleRange(resolution);
      }
    },
    setCustomView() {
      console.log("custom")
      // const data = this.getData(); // Get the data for the custom view
      const data = this.data;
      const visibleData = data.filter((_, index) => index % 3 === 0); // Filter data for every 3rd point
      const from = visibleData[0].time;
      const to = visibleData[visibleData.length - 1].time;
      const resolution = { from, to };
      this.chart.timeScale().setVisibleRange(resolution);
    },
  },
  async mounted() {
    await this.initChart()
    await this.updateChartData('BTCUSDT', '1d')

    // const chartElement = document.getElementById('chart-container');
    // const tableCell = chartElement.querySelector('table tr td:nth-child(2)');
    // const mycanvas = tableCell.querySelectorAll('canvas')[1];

    // function handler(pram){
    //   console.log(pram)
    // }
    // mycanvas.addEventListener("mousedown", (eventData) => {
    //   if (eventData.button === 2){
    //     console.log("click on canvas")
    //     chart.applyOptions({handleScroll: {
    //                           pressedMouseMove: false
    //                         }})
    //     chart.subscribeCrosshairMove(handler)
    //   }
      
    // })
    // mycanvas.addEventListener("mouseup", () => {
    //   console.log("unclick on canvas")
    //   chart.unsubscribeCrosshairMove(handler)
    // })

  },

};
</script>

<style lang="scss" scoped>

.separator {
  width: 2px;
  height: 16px;
  background-color: rgba(255, 255, 255, 0.25);
  margin: 0 8px;
  display: inline-block;
  vertical-align: middle;
}

.ChartView {
  padding: 1rem;
}
.chart-layout {
  border-radius: .4rem;
  overflow: hidden;
  background-color: #1e293b;
  padding-left: 28px;
}
#chart-container {
  width: 900px;
  height: 600px;
  
}
.button-container {
    display: flex;
    align-items: center;
    margin-top: 10px;
}
.button-container button {
  margin-right: 5px;
  color: var(--light);
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}

.timescale_btn {
  display: inline-flex;
  align-items: flex-end;
  margin-left: 5px;

  padding: 5px 8px;
  border-radius: 5px;
  border: rgba(255, 255, 255, 0.1) 2px solid;
  cursor: pointer;

  
  &:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
}

.circle {
  align-self: center;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 5px;
}

.indicList{

  
  button {
    visibility: hidden;
    color: rgba(255, 255, 255, 0.75);
    border-radius: 50%;
    &:hover{
      color: rgb(255, 38, 38);
    }
  }
  .indic {
    padding: 1px 4px ;
    border-radius: 3px;
    display: flex;
    width: fit-content;
    border: solid 1px transparent;

  
    &:hover {
      border: solid 1px rgba(255, 255, 255, 0.5);
      // background-color: rgba(255, 255, 255, 0.10);
      button {
        visibility: visible;

      }
    }
  }
}
</style>
