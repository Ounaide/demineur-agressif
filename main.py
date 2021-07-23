
import pgzrun
from random import randint
from easygui import msgbox, ynbox
import os
import sys
from gtts import gTTS
from playsound import playsound

position = 10000, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

TITLE = "Démineur agressif par WG"
HEIGHT = 400
WIDTH = 400
color = 0, 0, 0


g=globals()
global cells

global w
w=20
global r
r = range(int(HEIGHT/w))

totalbombs=50

class Cell():
    def __init__(self,i,j,w):
        self.i = i
        self.j = j
        self.x = i*w
        self.y = j*w
        self.w = w
        self.isBomb = False
        self.revealed = False
        self.box = Rect((self.x,self.y),(w,w))
        self.boxD = Rect((self.x+w/20,self.y+w/20),(0.9*w,0.9*w))
        self.neighbours = 0
        self.flagged = False

    def reveal(self):
        self.revealed = True
        if self.neighbours == 0:
            self.floodfill()
          
    def floodfill(self):
        d=[-1,0,1]
        for a in d:
            for b in d:
                if self.i+a>=0 and self.j+b<=len(cells)-1 and self.j+b>=0 and self.i+a<=len(cells)-1 and not(cells[self.i+a][self.j+b].revealed):
                    cells[self.i+a][self.j+b].reveal()
                    
def reset():

    for i in r:
        for j in r:
            cells[i][j].flagged = False
            cells[i][j].revealed = False
            cells[i][j].isBomb = False
            cells[i][j].neighbours = 0
            screen.draw.rect(cells[i][j].box, color)
    addbombs(totalbombs)
    AN()


    

cells=[[Cell(i,j,w) for j in r] for i in r]

global index
index=[]
def addbombs(totalbombs):
    while totalbombs !=0:
        x,y=randint(1,len(cells)-2),randint(1,len(cells)-2)
        
        if (x,y) not in index:
            cells[x][y].isBomb = True
            index.append((x,y))
            totalbombs-=1
addbombs(totalbombs)
bombs = [cells[i][j] for i,j in index]
print(index)
notbombs = [[cell for cell in cells[i] if not(cell.isBomb)] for i in r]

def won():
    for i in r:
        for j in r:
            if notbombs[i][j].revealed:
                return True
            else:
                return False
def AN():
    d=[-1,0,1]
    try:
        for x in range(len(cells)-1):
            for y in range(len(cells)-1):
                if cells[x][y].isBomb:
                    for i in d:
                        for j in d:
                            if x+i>=0 and y+j<=len(cells) and y+j>=0 and x+i<=len(cells):
                                cells[x+i][y+j].neighbours+=1
    except: pass
                        
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
                screen.draw.filled_rect(cells[i][j].boxD, (255,255,255))
                screen.draw.text("B", center=(i*w + w/2,j*w + w/2), color="blue")

            
                



def on_mouse_down(pos,button):
    if won():
        if not(ynbox("Victoire ! \n Rejouer ?")):
            sys.exit(0)
        else:
            reset()
    d=[-1,0,1]
    x = int(pos[0]/w)
    y = int(pos[1]/w)
    print(f"Clic {button} sur case {x},{y}")
    print(cells[x][y].neighbours)
    if button == 1:
        if not(cells[x][y].flagged) and not(cells[x][y].isBomb):
            cells[x][y].reveal()
            """if cells[x][y].neighbours == 0:
                clist=[]
                for i in d:
                    for j in d:
                        if x+i>=0 and y+j<=len(cells)-1 and y+j>=0 and x+i<=len(cells)-1:
                            clist.append(cells[x+i][y+j])
                            for cell in clist:
                                try:
                                    if not(cell.isBomb) and x+i>=0 and y+j<=len(cells)-1 and y+j>=0 and x+i<=len(cells)-1:
                                        
                                        cell.reveal()
                                        
                                except: pass"""
        if cells[x][y].isBomb and not(cells[x][y].flagged) and not(won()):
            try:
                for i in r:
                    for j in r:
                        cells[i][j].reveal() 
            finally:
                try:
                    insultes = ["Tu pues tes morts","ok le dog", "viens me voir de profil si t'es un homme"]
                    tts = gTTS(insultes[randint(0,len(insultes)-1)],lang="fr")
                    tts.save("insulte.mp3")
                    playsound("insulte.mp3")
                    os.remove("insulte.mp3")
                except: pass
                if not(ynbox("Game over ! \n Rejouer ?")):
                    sys.exit(0)
                else:
                    reset()
    if button == 3:
        if not(cells[x][y].revealed):
            cells[x][y].flagged ^= 1
        

pgzrun.go()











