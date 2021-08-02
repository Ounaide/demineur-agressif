
import pgzrun
from random import randint
import PySimpleGUI as sg
import os
import sys
from gtts import gTTS
from playsound import playsound
from iteration_utilities import deepflatten


position = 10000, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

TITLE = "Démineur agressif par WG"
HEIGHT = 400
WIDTH = 400
color = 0, 0, 0

colors = {1:(0,0,255),
          2:(0,255,0),
          3:(255,0,0),
          4:(0,0,128),
          5:(170,0,255),
          6:(0,179,179)}       


sg.theme("Default1")
g=globals()
global cells

global w
w=20 #width of the cells
global r
r = range(int(HEIGHT/w))
global leftbombs

totalbombs=50 #number of bombs to play with
leftbombs = totalbombs
cbombs = totalbombs

def layout(status): #end game popup window 

    layout = [ [sg.T(f"{status} \nRejouer ?")],
               [sg.B("Oui"), sg.B("Non")]
               ]
    w = sg.Window("Écran de fin",layout)
    event, values = w.read()
    w.close()
    
    return event
    
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

    def reveal(self): #reveal chosen cell, floodfill check
        self.revealed = True
        if self.neighbours == 0:
            self.floodfill()
          
    def floodfill(self): #keep revealing empty neighbours as long as it's possible
        d=[-1,0,1]
        for a in d:
            for b in d:
                if self.i+a>=0 and self.j+b<=len(cells)-1 and self.j+b>=0 and self.i+a<=len(cells)-1 and not(cells[self.i+a][self.j+b].revealed) and not(cells[self.i+a][self.j+b].flagged):
                    cells[self.i+a][self.j+b].reveal()
                    
def reset(): #reset the game

    for i in r:
        for j in r:
            cells[i][j].flagged = False
            cells[i][j].revealed = False
            cells[i][j].isBomb = False
            cells[i][j].neighbours = 0
            screen.draw.rect(cells[i][j].box, color)
            
    addbombs(totalbombs)
    AN()
    notbombs = [[cell for cell in cells[i] if not(cell.isBomb)] for i in r]


    

cells=[[Cell(i,j,w) for j in r] for i in r] #create the 2D-array of the game's cells

global index
index=[]
def addbombs(totalbombs): #randomly add chosen number of bombs to the grid. 
    while totalbombs !=0:
        x,y=randint(1,len(cells)-2),randint(1,len(cells)-2)
        
        if (x,y) not in index: #avoid chosing twice the same cell
            cells[x][y].isBomb = True
            index.append((x,y))
            totalbombs-=1
addbombs(totalbombs)
bombs = [cells[i][j] for i,j in index]
print(index)
notbombs = [[cell for cell in cells[i] if not(cell.isBomb)] for i in r] #filter the non-bomb cells


def won(): #check for a win (called after each click/keypress)
    NBrevealed = list(deepflatten([[cell for cell in notbombs[i] if cell.revealed] for i in r]))
    if len(NBrevealed) == len(cells)**2 - cbombs:
        return True
    else:
        return False

def AN(): #increment the value "neighbours" to each of the 8 cells surronding a bomb for all cells of the grid
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
                

def draw(): #PG0 built in function. Creates the canvas and draws the game
    screen.fill((80,80,80))
    for i in r:
        for j in r:
            screen.draw.rect(cells[i][j].box, color) #draw the grid
            if cells[i][j].flagged: #draw a flag
                try:
                    screen.blit("flag", (i*w + w/8 ,j*w+w/8))
                except:
                    screen.draw.text("F", (i*w + w/4,j*w + w/4), color="red")
                
            if cells[i][j].revealed and not(cells[i][j].flagged): 
                screen.draw.filled_rect(cells[i][j].boxD, (255,255,255)) #draw the reveal effect
                if cells[i][j].neighbours !=0: #keep the cell empty if it has no neighbours at all
                    screen.draw.text(str(cells[i][j].neighbours), center=(i*w + w/2,j*w + w/2), color=colors[cells[i][j].neighbours]) # ^ otherwise, draw the number of surrounding bombs

                
            if cells[i][j].isBomb and cells[i][j].revealed: #draw a bomb
                screen.draw.filled_rect(cells[i][j].boxD, (255,255,255))
                screen.draw.text("B", center=(i*w + w/2,j*w + w/2), color="blue")

def on_key_down(key): #PG0 event hook
    if key ==  keys.SPACE:
        fullreveal(position[0],position[1]) #reveal all safe surrounding cells (should be left+right click but impossible with pg0). Can also use mouse3
    if key == keys.ESCAPE: #close the game 
        sys.exit(0)
    if key == keys.R: #reset the game at any given time
        reset()

def on_key_up(): #check for a win AFTER everything that happens in on_key_down()
    if won():
        if layout("Victoire !") == "Non": #victory popup 
            sys.exit(0)
        else:
            reset()
            
def on_mouse_move(pos): #used to store the mouse's position so that the spacebar can be used to fullreveal() just like mouse3
    global position
    x = int(pos[0]/w)
    y = int(pos[1]/w)
    position = (x,y)

                

def fullreveal(x,y): #reveal all supposably safe neighbouring cells
    if cells[x][y].revealed:
        d = [-1,0,1]
        for i in d:
            for j in d:
                 if x+i>=0 and y+j<len(cells) and y+j>=0 and x+i<len(cells) and not(cells[x+i][y+j].flagged):
                     cells[x+i][y+j].reveal()
                     if cells[x+i][y+j].isBomb or (cells[x+i][y+j].flagged and not(cells[x+i][y+j].isBomb)):
                         gameover()

def on_mouse_up(): #check for a win AFTER everything that happens in on_mouse_down()
    if won():
        if layout("Victoire !") == "Non":
            sys.exit(0)
        else:
            reset()
    
        
def on_mouse_down(pos,button): #main events of the game: left click (reveal cell), right click (flag cell), middle click (fullreveal() just like spacebar)
  
    
        
    d=[-1,0,1]
    x = int(pos[0]/w)
    y = int(pos[1]/w)


    if button == mouse.MIDDLE:
        fullreveal(x,y)
        
                             
    if button == mouse.LEFT:
        if not(cells[x][y].flagged):
            cells[x][y].reveal()
            
        if cells[x][y].isBomb and not(cells[x][y].flagged) and not(won()):
            gameover()
    if button == mouse.RIGHT:
        global leftbombs
        
        if not(cells[x][y].revealed):
            if cells[x][y].flagged: #keep track of the number of bombs that should be left (user might be wrong when placing flags)
                leftbombs+=1
            else:
                leftbombs-=1
            cells[x][y].flagged ^= 1 #switch the flag state of the cell. 
        print(leftbombs) 
        


def gameover():
    try:
        for i in r:
            for j in r:
                cells[i][j].reveal() #reveal the whole grid
    finally: #play the insult sound
        try:
            insultes = ["Tu pues tes morts","ok le dog", "viens te battre de profil si t'es un homme"]
            tts = gTTS(insultes[randint(0,len(insultes)-1)],lang="fr")
            tts.save("insulte.mp3")
            #playsound("insulte.mp3")
            os.remove("insulte.mp3")
        except: pass
        if layout("Défaite !") == "Non": #gameover popup window
            sys.exit(0)
        else:
            reset()

pgzrun.go()
