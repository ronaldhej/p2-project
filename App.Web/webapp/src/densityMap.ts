let canvas:HTMLCanvasElement;
let ctx:CanvasRenderingContext2D | null;
const RES = 32

export function setupDensityMap(id: string) {
    canvas = document.getElementById(id) as HTMLCanvasElement ?? null;
    canvas.width = RES
    canvas.height = RES
    ctx = canvas.getContext("2d");
}

export function updateDensityMap(densityField: number[][]) {
    
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    if (ctx == null) return

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    var id = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
    var pixels = id.data;

    for (let xx = 0; xx < RES; xx++) {
        for (let yy = 0; yy < RES; yy++) {
            let x = xx;
            let y = yy;

            let density = densityField[x][y]
            density = Math.floor(Math.min(density/7, 1)*256)
            var r = density;
            var g = density;
            var b = density;
            var off = (y * id.width + x) * 4;

            pixels[off] = r;
            pixels[off + 1] = g;
            pixels[off + 2] = b;
            pixels[off + 3] = 255;
        }
    }
    ctx.putImageData(id, 0, 0);
}