<template>
  <div class="ChartView">
    <SearchBar />
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
      </div>
      <div id="chart-container"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// https://www.tradingview.com/lightweight-charts/
import { createChart, CrosshairMode, PriceScaleMode } from 'lightweight-charts';
import TimeScaleMenu from '../components/TimeScaleMenu.vue'
import SearchBar from '../components/SearchBar.vue'
export default {
  components: {
    TimeScaleMenu,
    SearchBar
  },
  data() {
    return {
      chart: null,
      view: 'day',
      data: null,
      selectedTimeScale: '1d',
      isTimeScaleMenuOpen: false,
    };
  },
  methods: {
    toggleTimeScaleMenu() {
      console.log(this.isTimeScaleMenuOpen);
      this.isTimeScaleMenuOpen = !this.isTimeScaleMenuOpen;
      console.log(this.isTimeScaleMenuOpen);

    },
    setTimeScale(timeScale) {
      this.selectedTimeScale = timeScale;
      // Update the chart with the selected time scale
      // Your logic to update the chart here
      // You can use the selectedTimeScale value in your chart configuration or pass it to a method that handles the chart update
      // Example: this.updateChart(this.selectedTimeScale);
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
    async getHistoricalData() {
      let data = []
      await axios.get('http://localhost:6500/historical/BTCUSDT')
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

    async createChart(container) {
      this.chart = createChart(container, {
        width: 1000,
        height: 600,
        layout: {
          background: {
            color: '#1e293b', // Set background color
          },
          textColor: '#FFFFFF', // Set text color
        },
        grid: {
          vertLines: {
            color: 'rgba(197, 203, 206, 0.5)', // Set vertical grid line color
          },
          horzLines: {
            color: 'rgba(197, 203, 206, 0.5)', // Set horizontal grid line color
          },
        },
        timeScale: {
          timeVisible :true,
          secondsVisible : false,
        },
        // rightPriceScale: {
        //   borderVisible: false,
        // },
        // crosshair: {
        //   horzLine: {
        //     visible: false,
        //   },
	      // },
        // handleScroll: {
        //   vertTouchDrag: false,
        // },

        // other configuration options
      });

      var data = [];
      
      // Generate random data
      // const startDate = new Date('2021-01-01').getTime();
      // var value = 0;
      // for (let i = 0; i < 100; i++) {
      //   const date = new Date(startDate + i * 5 * 60 * 1000);
      //   value = value + Math.ceil(Math.random() * 99) * (Math.round(Math.random()) ? 1 : -1);
      //   data.push({ time: date/1000, value });
      // }
      // this.data = data

      // Generate fake data for line series

      // Add necessary elements to the chart
      const lineSeries = this.chart.addLineSeries({
        color: 'rgba(4, 111, 232, 1)',
	      lineWidth: 2,
        crosshairMarkerVisible: false,
        lastValueVisible: false,
        priceLineVisible: false,
      });
      lineSeries.setData(dataa);

      // var avgPriceLine = {
      //   price: 26000,
      //   color: '#be1238',
      //   lineWidth: 2,
      //   lineStyle: LightweightCharts.LineStyle.Solid,
      //   axisLabelVisible: true,
      //   title: 'average price',
      // };

      // lineSeries.createPriceLine(avgPriceLine);
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
        const resolution = this.getResolution();
        console.log(resolution)
        this.chart.timeScale().setVisibleRange(resolution);
      }
    },
    getResolution() {
      const startDate = new Date('2021-01-01').getTime();
      switch (this.view) {
        case 'day':
          return { from: new Date(startDate -24 * 60 * 60).getTime() / 1000, to: new Date(startDate).getTime() /1000 };
        case 'week':
          return { from: new Date(startDate -7 * 24 * 60 * 60).getTime() / 1000, to: new Date(startDate).getTime() / 1000 };
          // return { from: -7 * 24 * 60 * 60, to: 0 };
        case 'month':
          return { from: -30 * 24 * 60 * 60, to: 0 };
        default:
          return { from: -24 * 60 * 60, to: 0 };
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
    const container = document.getElementById('chart-container');
    // await this.createChart(container);
    

    
    var chart = createChart(container, {
      // width: 1000,
      // height: 600,
      autoSize: true,
      rightPriceScale: {
        visible: true,
        borderVisible: false,
        mode: PriceScaleMode.Normal,
        // borderColor: 'rgba(197, 203, 206, 1)',
      },
      // leftPriceScale: {
      //   visible: true,
      //   mode: PriceScaleMode.Normal,

      // },
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
    let data = await this.getHistoricalData();
    var areaSeries = chart.addAreaSeries({
      topColor:    'rgba(41, 98, 255, 0.56)',
      bottomColor: 'rgba(41, 98, 255, 0.04)',
      lineColor:   'rgba(41, 98, 255, 1)',
      lineWidth: 2,
	  });
    areaSeries.setData(data)

    

    const chartElement = document.getElementById('chart-container');
    const tableCell = chartElement.querySelector('table tr td:nth-child(2)');
    const mycanvas = tableCell.querySelectorAll('canvas')[1];

    function handler(pram){
      console.log(pram)
    }
    mycanvas.addEventListener("mousedown", (eventData) => {
      if (eventData.button === 2){
        console.log("click on canvas")
        chart.applyOptions({handleScroll: {
                              pressedMouseMove: false
                            }})
        chart.subscribeCrosshairMove(handler)
      }
      
    })
    mycanvas.addEventListener("mouseup", () => {
      console.log("unclick on canvas")
      chart.unsubscribeCrosshairMove(handler)
    })


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
</style>
