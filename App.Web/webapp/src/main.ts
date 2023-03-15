import './style.css'
import axios, { AxiosHeaders } from 'axios'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <img id="img-preview" src="./placeholder.png">
    <form id="form-sim" action="/image" method="post">
      <button id="form-sim-btn" type="submit">submit simulation 🚀</button>
    </form>
  <img src="https://www.freepnglogos.com/uploads/rubber-duck-png/rubber-duck-duck-png-transparent-images-pictures-photos-1.png" id="loading">
`

const elApp: HTMLElement | null = document.getElementById("app");
const preview: HTMLImageElement | null = document.getElementById("img-preview") as HTMLImageElement;
const getSimBtn: HTMLButtonElement | null = document.getElementById("form-sim-btn") as HTMLButtonElement;
const imgLoading: HTMLImageElement | null = document.getElementById("loading") as HTMLImageElement;



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

getSimBtn.addEventListener('click', e => {
  e.preventDefault()
  getSimulation();
})
