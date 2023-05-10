<template>
  <div class="ChartView">
    <h1>This is a Chart page</h1>
    <div class="chart-layout">
      <div class="button-container">
        <button  @click="setView('day')">Day</button>
        <button @click="setView('week')">Week</button>
        <button @click="setView('month')">Month</button>

        <button ref="timescale" @click.stop="toggleTimeScaleMenu">Time Scale</button>
        <time-scale-menu
          v-if="isTimeScaleMenuOpen"
          @select="setTimeScale"
          @close="closeTimeScaleMenu"
        ></time-scale-menu>

        <span class="separator"></span>
        <button title="Fit content" class="material-icons" style="font-size: 1.5rem;" @click="fitContent()">fit_screen</button>
        <button title="Reset price scale" class="material-icons" style="font-size: 1.5rem;" @click="resetYAxis()">height</button>
      </div>
      <div id="chart-container"></div>
    </div>
  </div>
</template>

<script>
import { createChart } from 'lightweight-charts';
import TimeScaleMenu from '../components/TimeScaleMenu.vue'
export default {
  components: {
    TimeScaleMenu
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

    doIt() {
      console.log(`Hello ${this.name}`);
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
    createChart(container) {
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
        }

        // other configuration options
      });

      // Generate random data
      const data = [];
      const startDate = new Date('2021-01-01').getTime();
      var value = 0;
      for (let i = 0; i < 100; i++) {
        const date = new Date(startDate + i * 5 * 60 * 1000);
        value = value + Math.ceil(Math.random() * 99) * (Math.round(Math.random()) ? 1 : -1);
        data.push({ time: date/1000, value });
      }
      this.data = data

      // Generate fake data for line series

      // Add necessary elements to the chart
      const lineSeries = this.chart.addLineSeries();
      lineSeries.setData(data);
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
  mounted() {
    this.doIt();

    const container = document.getElementById('chart-container');
    this.createChart(container);

  },

};
</script>

<style>



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
  padding-top: 28px;
  padding-left: 28px;
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
</style>
