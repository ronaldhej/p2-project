import Chart from 'chart.js/auto'

// label: 'density',
// data: data.map(row => row.count),
// fill: true,
// backgroundColor: "#e44f2210",
// borderColor: "#e44f22",
// tension: 0.1,

const data1 = [...Array(120).keys()].map(i => Math.max(0, Math.round((i / 120) * 10 + (Math.random() * 10 - 5) + 5)));


let densityChart: Chart;
const CLIP_DENSITY = 14

densityChart: Chart;

export default function setupChart(data: number[]) {

  const xAxis = [...Array(data.length).keys()].map(i => i + 1);
  densityChart = new Chart("density-chart", {
    type: 'line',
    data: {
      labels: xAxis,
      datasets: [
        {
          borderWidth: 1,
          label: "Amount of agents",
          data: data,
          stepped: false,
          borderColor: "#e44f22",
          backgroundColor: ['#e44f2210', '#f18b3710'],
          fill: true,
          pointRadius: 0,
          // segment: {
          //   borderColor: (ctx) => {
          //     let val = ctx.p0.parsed.y;
          //     return val >= CLIP_DENSITY ? '#e44f22' : "#f18b37"
          //   },
          //   backgroundColor: (ctx) => {
          //     let val = ctx.p0.parsed.y;
          //     return val >= CLIP_DENSITY ? '#e44f22' : "#ffffff00"
          //   },
          //   borderWidth: (ctx) => {
          //     let val = ctx.p0.parsed.y;
          //     return val >= CLIP_DENSITY ? 4 : 2
          //   },
          // }
        }
      ]
    },
    options: {
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
      scales: {
        x: {
          grid: {
            color: '#2C323F'
          }
        },
        y: {
          grid: {
            color: '#2C323F',
          },
        }
      }
    }
  })
}

export function updateGraph() {
  densityChart.data
}