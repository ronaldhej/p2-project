import Chart from 'chart.js/auto'
import baseChart from './lineChartBase';
import { max } from 'd3';
import { updateDensityMap } from './densityMap';

// label: 'density',
// data: data.map(row => row.count),
// fill: true,
// backgroundColor: "#e44f2210",
// borderColor: "#e44f22",
// tension: 0.1,

let simData:any[] = []

const CLIP_DENSITY = 14

Chart.defaults.color = "#5C6B80";
Chart.defaults.interaction.mode = 'nearest';
Chart.defaults.interaction.axis = 'x';
Chart.defaults.interaction.intersect = false;

let densityChart: Chart;
let runtimeChart: Chart;
let populationChart: Chart;


export default function setupChart() {
   densityChart = baseChart("density-chart", "density", 0);
   populationChart = baseChart("population-chart", "population", 0);

   runtimeChart = baseChart("runtime-chart", "runtime", 0);
   runtimeChart.data.datasets = [{
    borderWidth: 1,
    label: "update",
    data: [],
    stepped: false,
    borderColor: "#e44f22",
    backgroundColor: '#e44f2210',
    fill: true,
    pointRadius: 0,
  },{
    borderWidth: 1,
    label: "draw",
    data: [],
    stepped: false,
    borderColor: "#f18b37",
    backgroundColor: '#f18b3710',
    fill: true,
    pointRadius: 0,
  }]
}

export function updateGraphRange(range: number) {
  const xAxisFrames = [...Array(range).keys()].map(i => i + 1);
  densityChart.data.labels = xAxisFrames;
  populationChart.data.labels = xAxisFrames;
  runtimeChart.data.labels = xAxisFrames;

  densityChart.options.scales = {
    y: {
      title: {
        display: true,
        text: "agents / m²"
      }
    }
  }
  populationChart.options = {
    scales: {
        y: {
            suggestedMin: 0,
            suggestedMax: 500,
            title: {
              display: true,
              text: "agents"
            }
        }
    }
  }
  runtimeChart.options.scales = {
    y: {
      title: {
        display: true,
        text: "milliseconds"
      }
    }
  }

  densityChart.update();
  populationChart.update();
  runtimeChart.update();
}

export function updateGraphAddData(data: any) {
  updateDensityMap(data.densityField)
  simData.push(data);
  
  //var maxRow = arr.map(function(row){ return Math.max.apply(Math, row); });
  //var max = Math.max.apply(null, maxRow);
  const maxRowDensity:number[] = data.densityField.map(function(row:number[]){ return Math.max.apply(Math, row); })
  const maxDensity = Math.max.apply(null, maxRowDensity) * (8/(512/32))
  
  densityChart.data.datasets[0].data.push(maxDensity ?? 0);
  populationChart.data.datasets[0].data.push(data?.population ?? 0);

  runtimeChart.data.datasets[0].data.push(data?.update * 1000 ?? 0);
  runtimeChart.data.datasets[1].data.push(data?.draw * 1000 ?? 0);
  densityChart.update('none');
  populationChart.update('none');
  runtimeChart.update('none');

}

export function clearGraph() {
  densityChart.data.labels = [];
  populationChart.data.labels = [];
  runtimeChart.data.labels = [];

  densityChart.data.datasets[0].data = [];
  populationChart.data.datasets[0].data = [];
  runtimeChart.data.datasets[0].data = [];
  runtimeChart.data.datasets[1].data = [];
  simData = [];
  densityChart.update();
  populationChart.update();
  runtimeChart.update();
}