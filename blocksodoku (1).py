import pygame
import random
import numpy
import math


class Figure:
    x = 0
    y = 0
    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Gerade
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # Rev L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
        [[1, 2, 5, 6]],  # BLOCK
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Reverse S
    ]
    brick_colors = [
        (0, 0, 0),
        (0, 240, 240),  # 4 in einer Reihe
        (0, 0, 240),  # Reverse L
        (240, 160, 0),  # L
        (240, 240, 0),  # Block
        (0, 240, 0),  # S
        (160, 0, 240),  # T
        (240, 0, 0),  # Reverse S
    ]
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0,len(self.Figures)-1)
        self.color = self.brick_colors[self.type+1]
        self.rotation = 0

    def move(self, x, y):
        self.x=x
        self.y=y

    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.Figures[self.type]))

    def image(self):
        return self.Figures[self.type][self.rotation]


class BlockSudoku:
    field = []
    score = 0
    #wwidth is the width of the window
    #whigth is the hight of the window
    #rboarder is the right boarder mof the gamefield
    def __init__(self, _height, _width, wwidth, whight, lboarder, uboarder):
        self.height = _height
        self.width = _width
        self.lboarder=lboarder
        self.uboarder=uboarder
        self.field = []
        self.score = 0
        self.blocks = []

        #if zero no block is selected with the mouse
        self.blocktomove=0

        self.rboarder=lboarder+9*50
        blockhightdif=(whight-(3*200))/4
        blockxpos=self.rboarder+(wwidth-self.rboarder-200)/2
        self.blockpos = [[blockxpos,blockhightdif], [blockxpos,200+2*blockhightdif], [blockxpos,400+3*blockhightdif]]

        self.grid=numpy.zeros((self.height,self.width))
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)

        for i in range(3):
            self.blocks.append(Figure(self.blockpos[i][0],self.blockpos[i][1]))

    def checkcursorinblocks(self, cursorx, cursory):

        trigger=False

        for i in range(len(self.blockpos)):

            if (self.blockpos[i][0] < cursorx and self.blockpos[i][0] + 200 > cursorx) and (self.blockpos[i][1] < cursory and self.blockpos[i][1] + 200 > cursory):
                self.blocktomove=i
                trigger = True
        return trigger

    def checkblockingrid(self):
        blockx=0
        blocky=0
        resx=0
        resy=0
        #holds track of the distance to a square in the grid, used to find the closest square

        tolerance=20
        blockcounter=0
        ingridcounter=0
        for j in range(4):
            for i in range(4):
                p = j * 4 + i
                if p in self.blocks[self.blocktomove].image():
                    blockcounter+=1
                    blockx = self.blocks[self.blocktomove].x + i * 50
                    blocky = self.blocks[self.blocktomove].y + j * 50

                    if      (blockx > self.lboarder-tolerance and   (blockx+50) < self.lboarder+9*50 +tolerance  ) and \
                            (blocky > self.uboarder-tolerance and   (blocky+50) < self.uboarder+9*50 +tolerance  ):
                        ingridcounter+=1

        if ingridcounter==blockcounter:
            freetrigger=True

            resx=[]
            resy=[]
            for j in range(4):
                for i in range(4):
                    p = j * 4 + i

                    if p in self.blocks[self.blocktomove].image():
                        resultx = 9 * 50
                        resulty = 9 * 50
                        blockx = self.blocks[self.blocktomove].x + i * 50
                        blocky = self.blocks[self.blocktomove].y + j * 50
                        #checks collumn
                        for k in range(9):
                            dx=abs(blockx - (self.lboarder+k*50))
                            if dx<resultx:
                                resultx = dx
                                tempx=k
                        resx.append(tempx)
                        #checks row
                        for l in range(9):
                            dy=abs(blocky - (self.uboarder+l * 50))
                            if dy< resulty:
                                resulty=dy
                                tempy=l
                        resy.append(tempy)
                        if not self.grid[resx[-1],resy[-1]]==0:
                            freetrigger=False

            if not freetrigger==False:
                for i in range(len(resx)):
                    self.grid[resx[i],resy[i]]=1
                self.blocks[self.blocktomove]=Figure(self.blockpos[self.blocktomove][0],self.blockpos[self.blocktomove][1])
                self.score+=1

            else:
                self.blocks[self.blocktomove].move(self.blockpos[self.blocktomove][0],self.blockpos[self.blocktomove][1])
                print("fields occupied")

        else:
            self.blocks[self.blocktomove].move(self.blockpos[self.blocktomove][0], self.blockpos[self.blocktomove][1])
            print("Block not entirely in grid")

    def restart(self):
        self.grid=numpy.zeros((self.height,self.width))
        self.score=0
        for i in range(len(self.blocks)):
            self.blocks[i]=Figure(self.blockpos[i][0],self.blockpos[i][1])

    def removepatterns(self):
        #arrays that hold the coordinate of occupied cells registert by the following patternchecks
        xcoordinates=[]
        ycoordinates=[]
        # check all columns and rows at the same time
        for i in range(9):
            #the trigger for a row or collumn gets set to false if an empty spot was found
            collumntrigger=True
            rowtrigger = True
            for j in range(9):
                #check collumn
                if self.grid[i,j]<1:
                    collumntrigger=False
                #check row
                if self.grid[j, i] < 1:
                    rowtrigger = False
            #append every cell in the grid that is on a fully occupied row or collumn
            if collumntrigger:
                for k in range(9):
                    xcoordinates.append(i)
                    ycoordinates.append(k)
            if rowtrigger:
                for k in range(9):
                    xcoordinates.append(k)
                    ycoordinates.append(i)
        #check all 9 3x3 blocks in the 9x9 grid for complete occupation
        for i in range(3):
            for j in range(3):
                occtrigger = True
                #the trigger gets set to false, if one of the cells in the 3x3 block is unoccupied
                for k in range(9):
                    if self.grid[k%3+3*i, math.floor(k/3)+j*3] < 1:
                        occtrigger=False
                #if a 3x3 block is fully occupied append all coordinates of its cells
                if occtrigger:
                    for k in range(9):
                        xcoordinates.append(k % 3 + 3 * i)
                        ycoordinates.append(math.floor(k / 3) + 3*j)
        #iterating through all coordinates, resetting the grid at that position and increasing the score
        for i in range(len(xcoordinates)):
            self.score+=1
            self.grid[xcoordinates[i],ycoordinates[i]]=0
        return len(xcoordinates)


class Program:

    zoom = 50
    fps = 30
    primary_colors = {
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "GRAY": (128, 128, 128),
    }

    def __init__(self, windowx, windowy):
        self.default_font = pygame.font.SysFont('Calibri', 65, True, False)
        self.info_font = pygame.font.SysFont('Calibri', 30, True, False)
        self.icon = pygame.image.load('grid.png')
        self.starimage = pygame.image.load('stars.jpg')
        self.screen = pygame.display.set_mode((windowx, windowy))
        self.display_surface = pygame.display.set_mode((windowx, windowy))
        self.game=BlockSudoku(9, 9, windowx, windowy, 100, 100)
        pygame.display.set_caption('stars')
        pygame.display.set_caption("------- > BlockSodoku < -------")
        pygame.display.set_icon(self.icon)
        self.done = False
        self.combotrigger = False
        self.combostarttime = 0
        self.rectangle_draging = False
        self.offset_x = 0
        self.offset_y = 0

    def defaultbehaviour(self):
        #This function handles the draw functions and their order
        self.text_combo = self.default_font.render("Combo!", True, (255, 215, 0))
        self.text_info = self.info_font.render("Press R to restart", True, (255, 255, 255))
        self.text_score = self.default_font.render("Score:" + str(self.game.score), True, (255, 255, 255))
        self.display_surface.blit(self.starimage, (0, 0))
        self.screen.blit(self.text_score, [0, 00])
        self.screen.blit(self.text_info, [0, 575])
        self.drawgrid()
        self.drawnewblocks()
        self.drawcombo()

    def drawgrid(self):
        #This Function handles the grid drawing and the drawing of the occupied fields within it
        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.field[i][j] == 0:
                    just_border = 1
                else:
                    just_border = 0

                pygame.draw.rect(self.screen, self.primary_colors["WHITE"], [100 + j * self.zoom, 100 + i * self.zoom, self.zoom, self.zoom], just_border)

        for ix, iy in numpy.ndindex(self.game.grid.shape):
            if self.game.grid[ix, iy] > 0:
                pygame.draw.rect(self.screen, self.primary_colors["GRAY"], [self.game.lboarder + ix * 50, self.game.uboarder + iy * 50, self.zoom, self.zoom])

    def drawnewblocks(self):
        #Handels the drawing of the new blocks
        for k in range(len(self.game.blocks)):
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.game.blocks[k].image():
                        pygame.draw.rect(self.screen, self.game.blocks[k].color,
                                         [(j * self.zoom + self.game.blocks[k].x), (i * self.zoom + self.game.blocks[k].y), self.zoom, self.zoom])

    def drawcombo(self):
        #only handels the drawing of the combo banner could have been implemented in standard behaviour aswell
        if self.combotrigger and pygame.time.get_ticks() - self.combostarttime < 1000:
            self.screen.blit(self.text_combo, [400, 300])
        if self.combotrigger and pygame.time.get_ticks() - self.combostarttime > 1000:
            self.combotrigger = False

    #Here the external inputs are getting handeled
    def mousedown(self, mx, my):
        if self.game.checkcursorinblocks(mx, my):
            self.rectangle_draging = True
            self.offset_x = self.game.blocks[self.game.blocktomove].x - mouse_x
            self.offset_y = self.game.blocks[self.game.blocktomove].y - mouse_y

    def mouseup(self):
        self.game.checkblockingrid()
        amount = self.game.removepatterns()
        if amount > 9:
            self.combotrigger = True
            self.combostarttime = pygame.time.get_ticks()
        self.rectangle_draging = False
        self.game.blocktomove = 0

    def mousemovement(self, mx, my):
        self.game.blocks[self.game.blocktomove].move(mx + self.offset_x, my + self.offset_y)

    def rkey(self):
        self.game.restart()

    def spacekey(self):
        self.game.blocks[self.game.blocktomove].rotate()


if __name__ == '__main__':
    pygame.init()
    program = Program(800, 600)
    clock = pygame.time.Clock()
    while not program.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    program.mousedown(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    program.mouseup()

            elif event.type == pygame.MOUSEMOTION:
                if program.rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    program.mousemovement(mouse_x, mouse_y)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    program.rkey()
                if event.key == pygame.K_SPACE:
                    program.spacekey()
        program.defaultbehaviour()
        pygame.display.flip()
        clock.tick(program.fps)
    pygame.display.update()
    pygame.quit()



















