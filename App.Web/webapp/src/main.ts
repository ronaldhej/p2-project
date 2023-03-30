import './style.css'
import axios, { AxiosHeaders } from 'axios'
import navbar, { setupNavbar } from './navbar'
import './simulationDtos'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  ${navbar()}
  <div id="content">
    <img id="img-preview" src="./placeholder.png">
    <input type="number" id="simAgentNum" name="simAgentNum" placeholder="number of agents">
    <input type="number" id="simRuntime" name="simRuntime" placeholder="runtime in seconds">
    <button id="form-sim-btn" type="submit">submit simulation 🚀</button>
    <img src="https://www.freepnglogos.com/uploads/rubber-duck-png/rubber-duck-duck-png-transparent-images-pictures-photos-1.png" id="loading">
  </div>
`
//setupNavbar();

const elApp: HTMLElement            | null = document.getElementById("app");
const preview: HTMLImageElement     | null = document.getElementById("img-preview") as HTMLImageElement;
const imgLoading: HTMLImageElement  | null = document.getElementById("loading") as HTMLImageElement;

//simulation input
const simAgentNum: HTMLInputElement | null = document.getElementById("simAgentNum") as HTMLInputElement;
const simRuntime: HTMLInputElement  | null = document.getElementById("simRuntime") as HTMLInputElement;
const getSimBtn: HTMLButtonElement  | null = document.getElementById("form-sim-btn") as HTMLButtonElement;


function testSim(simRequest: SimRequestDto) {
  axios("http://127.0.0.1:8000/simulate", {method: 'post', data: JSON.stringify(simRequest)}).then(res => {
    console.log(res.data);
  })
}

function postSimRequest(simRequest: SimRequestDto) {
  if (imgLoading) imgLoading.style.opacity = "1";
  
  const result = axios.post("http://127.0.0.1:8000/simulate", simRequest).then(res => {
    let b64_gif: string = "data:image/gif;base64,";
    b64_gif += res.data.image_gif;

    preview!.src = b64_gif;
    preview!.style.opacity = "1";
    imgLoading!.style.opacity = "0";

  }).catch(err => {
    if (imgLoading) imgLoading.style.opacity = "0";
    console.log("fetch failed! 😭: " + err.message);
  });
  console.log(result)
}


function getSimulation() {
  console.log("fetching simulation");

  if (imgLoading) imgLoading.style.opacity = "1";
  axios("http://127.0.0.1:8000/image", {
    method: 'get'
  }).then(res => {
    let b64_gif: string = "data:image/gif;base64,";
    b64_gif += res.data.image_gif;

    if (preview) preview.src = b64_gif;
    if (preview) preview.style.opacity = "1";
    if (imgLoading) imgLoading.style.opacity = "0";

  }).catch(err => {
    if (imgLoading) imgLoading.style.opacity = "0";
    console.log("fetch failed! 😭: " + err.message);
  });
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
  //getSimulation();
  //testSim(testObj);
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



  postSimRequest(simRequest);
})
