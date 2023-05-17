//     agent_num: int
//     runtime: int | None = 10
//     map: list[CanvasEntity] | None = None

export interface EntityDto {
    center_x: number,
    center_y: number,
    width: number,
    height: number,
    color?: string
}

export interface SimRequestDto {
    agent_num: number,
    runtime: number,
    map?: [EntityDto]
}