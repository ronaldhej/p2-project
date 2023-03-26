//     agent_num: int
//     runtime: int | None = 10
//     map: list[CanvasEntity] | None = None

type Entity = {
    center_x: number,
    center_y: number,
    width: number,
    height: number,
    color?: string
}

type SimRequest = {
    agent_num: number,
    runtime: number,
    map?: [Entity]
}