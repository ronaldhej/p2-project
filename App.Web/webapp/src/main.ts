import './style.css'
import './simulationDtos'
import setupChart, { clearGraph, updateGraphAddData, updateGraphRange } from './simCharts'
import { setupDensityMap } from './densityMap'
const SIM_SIZE = 512;

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div id="content">
    <div>
      <div class="progress-bar" id="progress-bar"></div>
      <img id="img-preview" src="">
    </div>
    <input type="number" id="simAgentNum" name="simAgentNum" placeholder="new agents per frame">
    <input type="number" id="simRuntime" name="simRuntime" placeholder="runtime in seconds">
    <button id="form-sim-btn" type="submit">begin simulation 🚀</button>
  </div>
  <div id="results">
    <canvas id="density-map"></canvas>
    <div id="density-map-select">
      <span class="unselectable"></span>
    </div>
    <canvas id="density-chart"></canvas>
    <canvas id="population-chart"></canvas>
    <canvas id="runtime-chart"></canvas>
  </div>
`
setupChart();
setupDensityMap("density-map");

const app: HTMLElement | null = document.getElementById("app");
const preview: HTMLImageElement | null = document.getElementById("img-preview") as HTMLImageElement;
const progressBar: HTMLDivElement | null = document.getElementById("progress-bar") as HTMLDivElement;
const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;

//simulation input
const simAgentNum: HTMLInputElement | null = document.getElementById("simAgentNum") as HTMLInputElement;
const simRuntime: HTMLInputElement | null = document.getElementById("simRuntime") as HTMLInputElement;
const getSimBtn: HTMLButtonElement | null = document.getElementById("form-sim-btn") as HTMLButtonElement;

getSimBtn.addEventListener('click', e => {
  e.preventDefault()
  clearGraph()
  updateGraphRange(parseInt(simRuntime.value) * 30)
  preview!.style.opacity = "0.2";
  results.style.width = '100%';

  let simRequest: SimRequestDto = {
    agent_num: parseInt(simAgentNum.value),
    runtime: parseInt(simRuntime.value),
    map: [
      {
        center_x: 0,
        center_y: 0,
        width: 0,
        height: 0,
        color: "White"
      }
    ]
  }


  let ws = new WebSocket("ws://localhost:8000/ws");
  ws.onopen = () => ws.send(JSON.stringify(simRequest));
  ws.onmessage = function (event) {
    let data = JSON.parse(event.data);

    switch (data.type) {
      case 0:
        let b64_gif: string = "data:image/gif;base64,";
        b64_gif += data.sim_gif;
        preview!.src = b64_gif;
        preview!.style.opacity = "1";
        progressBar.style.opacity = "0";
        progressBar.style.width = "0px";
        break

      case 1:
        updateGraphAddData(data);
        let prog = data.progress / (parseInt(simRuntime.value) * 30);
        progressBar.style.opacity = "0.2";
        progressBar.style.width = (prog * SIM_SIZE).toString() + 'px';
        break

      default:
        break
    }
  };
  ws.onclose = () => {
    progressBar.style.opacity = "0";
    progressBar.style.width = "0px";
    console.log("connection closed");
  }
})
