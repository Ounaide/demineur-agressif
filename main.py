import numpy as np
import pgzrun
from random import randint
from numpy import matrix

TITLE = "Démineur par WG"
HEIGHT = 400
WIDTH = 400
color = 0, 0, 0


g=globals()
global cells

global w
w=20
global r
r = range(int(HEIGHT/w))

totalbombs=20

class Cell:
    def __init__(self,i,j,w):
        self.x = i*w
        self.y = j*w
        self.w = w
        self.isBomb = False
        self.revealed = False
        self.box = Rect((self.x,self.y),(w,w))
        self.neighbours = 0
        self.flagged = False

cells=[[Cell(i,j,w) for j in r] for i in r]


while totalbombs !=0:

    cells[randint(0,19)][randint(0,19)].isBomb = True
    totalbombs-=1
            

def countNeighbours():
    count = 0
    for i in r:
        for j in r:
            for x in [-1,0,-1]:
                for y in [-1,0,1]:
                    try:
                        if cells[i+x][j+y].isBomb and not(cells[i][j].isBomb):
                                
                                cells[i][j].neighbours+=1
                    except:
                        pass


            
 
countNeighbours()
def draw():
   
    screen.fill((255,255,255 ))
    for i in r:
        for j in r:
            screen.draw.rect(cells[i][j].box, color)
            if cells[i][j].flagged:
                screen.draw.text("F", (i*w + w/4,j*w + w/4), color="red")
            if cells[i][j].revealed and not(cells[i][j].flagged):
                screen.draw.text(str(cells[i][j].neighbours), (i*w + w/4,j*w + w/4), color="black")
            if cells[i][j].isBomb:
                screen.draw.text("B", (i*w + w/4,j*w + w/4), color="blue")

            
                


def update():
    pass

def on_mouse_down(pos,button):
    x = int(pos[0]/w)
    y = int(pos[1]/w)
    print(f"Clic {button} sur case {x},{y}")
    print(cells[x][y].neighbours)
    if button == 1:
        if not(cells[x][y].flagged):
            cells[x][y].revealed = True
        if cells[x][y].isBomb:
            for i in r:
                for j in r:
                    cells[i][j].revealed = True
            print("game over")
    if button == 3:
        if not(cells[x][y].revealed):
            cells[x][y].flagged ^= 1
        

pgzrun.go()







