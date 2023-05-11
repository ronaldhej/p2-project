let canvas: HTMLCanvasElement;
let selection: HTMLDivElement;
let densityTooltip: HTMLSpanElement;
let ctx: CanvasRenderingContext2D | null;
const RES = 32

let densityFieldFrame: number[][];
let selectionCellPos = {
    x: 0,
    y: 0
};

const colorLow: number[] = [30, 33, 45];
const colorHigh: number[] = [255, 255, 255];
const riskLow: number[] = [241, 139, 55];
const riskHigh: number[] = [228, 79, 34];

const mapSize = 512;
const meterPixels = 8;
const mapResoultion = 32;
const mapCellSize = mapSize / mapResoultion;

export function setupDensityMap(id: string) {
    canvas = document.getElementById(id) as HTMLCanvasElement ?? null;
    selection = document.getElementById(id + "-select") as HTMLDivElement ?? null;
    densityTooltip = selection.children[0] as HTMLSpanElement;
    canvas.width = RES;
    canvas.height = RES;
    ctx = canvas.getContext("2d");

    canvas.addEventListener('click', (e) => {
        let cellWidth = canvas.scrollWidth / RES;
        selection.style.width = cellWidth + "px";
        selection.style.height = cellWidth + "px";

        let cellX = Math.floor((e.clientX - canvas.offsetLeft) / cellWidth)
        let cellY = Math.floor((e.clientY - canvas.offsetTop) / cellWidth)

        let selectionX = canvas.offsetLeft + (cellX * cellWidth)
        let selectionY = canvas.offsetTop + (cellY * cellWidth)

        if (selectionCellPos.x == cellX &&
            selectionCellPos.y == cellY &&
            selection.style.opacity == "1") {
            selection.style.opacity = "0";
        } else {
            selection.style.opacity = "1";
        }
        selectionCellPos.x = cellX;
        selectionCellPos.y = cellY;

        selection.style.left = selectionX + 2 + "px";
        selection.style.top = selectionY + 2 + "px";

        updateDensityTooltip(cellX, cellY)

        e.stopPropagation();
        e.preventDefault();
    });
}

export function updateDensityMap(densityField: number[][]) {

    densityFieldFrame = densityField;
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    if (ctx == null) return

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    let id = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
    let pixels = id.data;

    for (let xx = 0; xx < RES; xx++) {
        for (let yy = 0; yy < RES; yy++) {
            let x = xx;
            let y = yy;

            let agentCount = densityField[x][y];
            let density = agentCountToDensity(agentCount);
            let densityValue = Math.min(density / 7, 1);

            if (density >= 7) {
                densityValue = Math.min((density - 7) / 5, 1);
            }

            let r = 0;
            let g = 0;
            let b = 0;

            if (density >= 7) {
                r = riskLow[0] + densityValue * (riskHigh[0] - riskLow[0]);
                g = riskLow[1] + densityValue * (riskHigh[1] - riskLow[1]);
                b = riskLow[2] + densityValue * (riskHigh[2] - riskLow[2]);
            } else {
                r = colorLow[0] + densityValue * (colorHigh[0] - colorLow[0]);
                g = colorLow[1] + densityValue * (colorHigh[1] - colorLow[1]);
                b = colorLow[2] + densityValue * (colorHigh[2] - colorLow[2]);
            }

            let off = (y * id.width + x) * 4;

            pixels[off] = Math.floor(r);
            pixels[off + 1] = Math.floor(g);
            pixels[off + 2] = Math.floor(b);
            pixels[off + 3] = 255;
        }
        updateDensityTooltip();
    }
    ctx.putImageData(id, 0, 0);
}

function updateDensityTooltip(cx?: number, cy?: number) {
    let cellX = cx ?? selectionCellPos.x;
    let cellY = cy ?? selectionCellPos.y;
    try {
        //subtract y index from field height, since the 2D array is flipped
        let agentCount = densityFieldFrame[cellX][densityFieldFrame[cellX].length - cellY - 1];
        densityTooltip.innerText = `agents: ${agentCount.toString()}\ndensity: ${agentCountToDensity(agentCount)} agents/m²`;
    } catch (e) {
        console.log("Something went wrong with density map: " + e);
    }

}

function agentCountToDensity(count: number) {
    return count * (meterPixels / (mapSize / mapCellSize));
}