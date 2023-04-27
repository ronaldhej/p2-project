import './style.css'
import axios, { AxiosHeaders } from 'axios'
import navbar, { setupNavbar } from './navbar'
import './simulationDtos'
import setupChart, { clearGraph, updateGraphAddData, updateGraphRange } from './simCharts'
const SIM_SIZE = 512;

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  ${navbar()}
  <div id="content">
    <div>
      <div class="progress-bar" id="progress-bar"></div>
      <img id="img-preview" src="">
    </div>
    <input type="number" id="simAgentNum" name="simAgentNum" placeholder="number of agents">
    <input type="number" id="simRuntime" name="simRuntime" placeholder="runtime in seconds">
    <button id="form-sim-btn" type="submit">begin simulation 🚀</button>
  </div>
  <div id="results">
    <canvas id="density-chart"></canvas>
    <canvas id="population-chart"></canvas>
    <canvas id="runtime-chart"></canvas>
  </div>
`
//setupNavbar();
setupChart();

const elApp: HTMLElement | null = document.getElementById("app");
const preview: HTMLImageElement | null = document.getElementById("img-preview") as HTMLImageElement;
const progressBar: HTMLDivElement | null = document.getElementById("progress-bar") as HTMLDivElement;
const results: HTMLDivElement | null = document.getElementById("results") as HTMLDivElement;

//simulation input
const simAgentNum: HTMLInputElement | null = document.getElementById("simAgentNum") as HTMLInputElement;
const simRuntime: HTMLInputElement | null = document.getElementById("simRuntime") as HTMLInputElement;
const getSimBtn: HTMLButtonElement | null = document.getElementById("form-sim-btn") as HTMLButtonElement;


function testSim(simRequest: SimRequestDto) {
  axios("http://127.0.0.1:8000/simulate", { method: 'post', data: JSON.stringify(simRequest) }).then(res => {
    console.log(res.data);
  })
}

function postSimRequest(simRequest: SimRequestDto) {

  const result = axios.post("http://127.0.0.1:8000/simulate", simRequest).then(res => {
    let b64_gif: string = "data:image/gif;base64,";
    b64_gif += res.data.sim_gif;
    setupChart()


    preview!.src = b64_gif;
    preview!.style.opacity = "1";


  }).catch(err => {
    console.log("fetch failed: " + err.message);
  });
  console.log(result)
}

let testObj: SimRequestDto = {
  "agent_num": 0,
  "runtime": 10,
  "map": [
    {
      "center_x": 0,
      "center_y": 0,
      "width": 0,
      "height": 0,
      "color": "White"
    }
  ]
}

getSimBtn.addEventListener('click', e => {
  e.preventDefault()
  clearGraph()
  updateGraphRange(parseInt(simRuntime.value)*30)
  preview!.style.opacity = "0.2";
  results.style.width = 512 + 'px';
  
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
  ws.onopen = () => ws.send(JSON.stringify(simRequest))
  ws.onmessage = function(event) { 
    let data = JSON.parse(event.data)

    switch (data.type) {
      case 0:
        let b64_gif: string = "data:image/gif;base64,";
        b64_gif += data.sim_gif;
        preview!.src = b64_gif;
        preview!.style.opacity = "1";
        progressBar.style.opacity = "0"
        progressBar.style.width = "0px"
        break

      case 1:
        updateGraphAddData(data);
        let prog = data.progress/(parseInt(simRuntime.value)*30)
        progressBar.style.opacity = "0.2"
        progressBar.style.width = (prog*SIM_SIZE).toString() + 'px';
        
        break

      default:
        break
    }
  };
  ws.onclose = () => {
    progressBar.style.opacity = "0"
    progressBar.style.width = "0px"
    console.log("connection closed");
  }


  //postSimRequest(simRequest);
})
