import arcade
import pymunk
import math
import random

MAX_COST = 65535
class Cell:
    '''
    Cell
    ---
    Flowfields are made up of cells

    A cell contains a cost, direction and weight

    Args:
        x (int) x-coordinate of the cell
        
        y (int) y-coordinate of the cell
    '''
    def __init__(self, x:int, y:int) -> None:
        self.direction = 0
        self.weight:int = 1
        self.density:int = 0
        self.cost:int = 0
        self.x:int = x
        self.y:int = y
        self.neighbors:list[Cell] = []
        self.direct_neighbors = 0


class FlowField:
    '''
    FlowField
    ---
    A matrix of Cells, allowing for cheap pathfinding during simulation of large amounts of entities/agents

    Pathfinding is done using a modified version of Dijkstra's algorithm, using an open list

    Args:
        width       (int) the width of the field in pixels

        height      (int) the height of the field in pixels

        resolution  (int) desired amount of columns/rows

    '''
    def __init__(self, width: int, height: int, resolution: int, dest:tuple[int,int]) -> None:
        self.width = width
        self.height = height
        self.cell_width: int = 0
        self.cell_height: int = 0
        self.cell_x: int = 0
        self.cell_y: int = 0
        self.resolution = resolution
        self.field:list[list[Cell]] = []
        self.destination_cell:tuple[int,int] = dest


    def setup(self, wall_list: list[pymunk.Poly]):
        '''
        Initialise cell arrays

        Cells inside obstacles are assigned a cost greater than MAX_COST

        Sets up a list of available neighbors for each cell
        '''
        print("setting up flowfield")
        self.cell_width = round(self.width/self.resolution)
        self.cell_height = round(self.width/self.resolution)
        self.field = [[Cell]*self.resolution for _ in range(self.resolution)]
        for x in range(self.resolution):
            for y in range(self.resolution):
                print("initialising cell: ", x,y)
                new_cell:Cell = Cell(x,y)
                new_cell.direction = math.radians(random.random()*360)
                
                for w in wall_list:
                    point = (x*self.cell_width + (self.cell_width/2), y*self.cell_width + (self.cell_width/2))
                    if w.point_query(point).distance < 0:
                        new_cell.cost = MAX_COST + 1

                self.field[x][y] = new_cell


        #add neighbors
        for x in range(self.resolution):
            for y in range(self.resolution):
                cell:Cell = self.field[x][y]
                #direct neighbors
                if cell.y > 0:
                    cell.neighbors.append(self.field[cell.x][cell.y - 1]) #N
                    cell.direct_neighbors += 1
                if cell.y < self.resolution-1:
                    cell.neighbors.append(self.field[cell.x][cell.y + 1]) #S
                    cell.direct_neighbors += 1
                if cell.x > 0:
                    cell.neighbors.append(self.field[cell.x - 1][cell.y]) #W
                    cell.direct_neighbors += 1
                if cell.x < self.resolution-1:
                    cell.neighbors.append(self.field[cell.x + 1][cell.y]) #E
                    cell.direct_neighbors += 1

                #diagonal neighbors
                if cell.x > 0 and cell.y > 0:                                       cell.neighbors.append(self.field[cell.x - 1][cell.y - 1])
                if cell.x < self.resolution-1 and cell.y > 0:                       cell.neighbors.append(self.field[cell.x + 1][cell.y - 1])
                if cell.x > 0 and cell.y < self.resolution-1:                       cell.neighbors.append(self.field[cell.x - 1][cell.y + 1])
                if cell.x < self.resolution-1 and cell.y < self.resolution-1:       cell.neighbors.append(self.field[cell.x + 1][cell.y + 1])

        self.update()

    def update(self):
        '''
        Updates direction of cells in the flowfield

        Cells inside obstacles (cost=MAX_COST) are ignored
        '''
        (dest_x, dest_y) = self.destination_cell
        open_list:list[Cell] = []
        current_cell:Cell = None
        for x in range(self.resolution):
            for y in range(self.resolution):
                cell = self.field[x][y]

                if cell == self.field[dest_x][dest_y]:
                    cell.cost = 0
                    open_list.append(cell)
                elif cell.cost <= MAX_COST:
                    cell.cost = MAX_COST


        while len(open_list) > 0:
            current_cell:Cell = open_list.pop(0)
            for cell in current_cell.neighbors[:current_cell.direct_neighbors]:

                if cell.cost > MAX_COST:
                    continue

                if cell not in open_list and cell.cost == MAX_COST:
                    open_list.append(cell)

                new_cost:int = current_cell.cost + (cell.weight*(cell.density+1))
                if new_cost < cell.cost:
                    cell.cost = new_cost


        for x in range(self.resolution):
            for y in range(self.resolution):
                cell = self.field[x][y]

                best:Cell = cell.neighbors[0]
                for n in cell.neighbors:
                    if n.cost < best.cost: best = n
                xdir = best.x - cell.x
                ydir = best.y - cell.y
                cell.direction = math.atan2(ydir,xdir)


    def get_cell(self, x, y) -> Cell:
        '''
        convert global coordinates to field index using the field resolution
        
        return corrosponding cell
        '''
        cell_x:int = math.floor(x / self.cell_width)
        cell_y:int = math.floor(y / self.cell_height)
        return self.field[cell_x][cell_y]


    def draw(self):
        '''
        Draw flow field for debugging purposes

        Draws the direction of each cell at their center

        Direction lines are colored based on cost going from blue to green, blue being closer to target

        Red lines are cells inside an obstacle
        '''
        radius = self.resolution*2
        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                cell:Cell = self.field[x][y]
                center_x = self.cell_width*cell.x + self.cell_width/2
                center_y = self.cell_height*cell.y + self.cell_height/2
                color:arcade.Color = (0,int(cell.cost/radius*255),255-int(cell.cost/radius*255)) if cell.cost <= MAX_COST else (255,55,55)
                if (x,y) == self.destination_cell:
                    color = (255,255,255)
                arcade.draw_line(center_x,
                                 center_y,
                                 center_x+math.cos(cell.direction)*8,
                                 center_y+math.sin(cell.direction)*8,
                                 color,1)
                #arcade.draw_text(str(cell.cost),center_x, center_y, color, 10)
            #arcade.draw_line(x*self.cell_width,SPACE_HEIGHT,x*self.cell_width,0, (55,55,55))

    def get_density_field(self) -> list[list[int]]:
        """return a matrix, representing density of each cell in flowfield"""
        res: int = self.resolution
        d_field = [ [0]*res for _ in range(res)]
        
        for x in range(res):
            for y in range(res):
                d_field[x][y] += self.field[x][y].density

        return d_field
    
    def clear_density(self):
        """reset density of all cells in field"""
        res: int = self.resolution
        for x in range(res):
            for y in range(res):
                self.field[x][y].density = 0