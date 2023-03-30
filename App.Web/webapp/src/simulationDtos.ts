//     agent_num: int
//     runtime: int | None = 10
//     map: list[CanvasEntity] | None = None

type EntityDto = {
    center_x: number,
    center_y: number,
    width: number,
    height: number,
    color?: string
}

interface SimRequestDto {
    agent_num: number,
    runtime: number,
    map?: [EntityDto]
}