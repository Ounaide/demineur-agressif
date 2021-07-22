import pgzrun
from random import randint


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
class Cell():
    def __init__(self,i,j,w):
        self.x = i*w
        self.y = j*w
        self.w = w
        self.isBomb = False
        self.revealed = False
        self.box = Rect((self.x,self.y),(w,w))
        self.boxD = Rect((self.x+w/20,self.y+w/20),(0.9*w,0.9*w))
        self.neighbours = 0
        self.flagged = False

        

cells=[[Cell(i,j,w) for j in r] for i in r]


index=[]
while totalbombs !=0:
    x,y=randint(0,len(cells)-1),randint(0,len(cells)-1)
    
    if (x,y) not in index: cells[x][y].isBomb = True
    index.append((x,y))
    totalbombs-=1

        
            
def AN():
    d=[-1,0,1]
    for x in range(len(cells)-1):
        for y in range(len(cells)-1):
            if cells[x][y].isBomb:
                for i in d:
                    for j in d:
                        cells[x+i][y+j].neighbours+=1
                        
AN()
                

def draw():
    screen.fill((80,80,80))
    for i in r:
        for j in r:
            screen.draw.rect(cells[i][j].box, color)
            if cells[i][j].flagged:
                screen.draw.text("F", (i*w + w/4,j*w + w/4), color="red")
            if cells[i][j].revealed and not(cells[i][j].flagged):
                screen.draw.filled_rect(cells[i][j].boxD, (255,255,255))
                if cells[i][j].neighbours !=0:
                    screen.draw.text(str(cells[i][j].neighbours), center=(i*w + w/2,j*w + w/2), color="black")
                else:
                    screen.draw.text(" ", center=(i*w + w/2,j*w + w/2), color="black")
                
            if cells[i][j].isBomb and cells[i][j].revealed:
                screen.draw.text("B", center=(i*w + w/2,j*w + w/2), color="blue")

            
                



def on_mouse_down(pos,button):
    d=[-1,0,1]
    x = int(pos[0]/w)
    y = int(pos[1]/w)
    print(f"Clic {button} sur case {x},{y}")
    print(cells[x][y].neighbours)
    if button == 1:
        if not(cells[x][y].flagged) and not(cells[x][y].isBomb):
            cells[x][y].revealed = True
            if cells[x][y].neighbours == 0:
                for i in d:
                    for j in d:
                        try:
                            if not(cells[x+i][y+j].isBomb) and x+i>=0 and y+j<=len(cells)-1 and y+j>=0 and x+i<=len(cells)-1:
                                newcell = cells[x+i][y+j]
                                newcell.revealed = True
                        except: pass
        if cells[x][y].isBomb and not(cells[x][y].flagged):
            for i in r:
                for j in r:
                    cells[i][j].revealed = True 
            print("game over")
    if button == 3:
        if not(cells[x][y].revealed):
            cells[x][y].flagged ^= 1
        

pgzrun.go()







