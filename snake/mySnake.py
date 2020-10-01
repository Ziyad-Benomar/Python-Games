from tkinter import *
import time
from random import randrange
fen=Tk()
fen.title('mySnake')
can=Canvas(fen,height=500,width=500)
nl=20
nc=20
u=20
dt=100
score=0
Score=Label(fen,text='Score   :  '+str(score),font=('Agency FB',25),fg='red',bg='black')
Score.grid(column=1,row=3,columnspan=3)

img = PhotoImage(file="data/deco.gif")
cn_im=Canvas(fen,height=120,width=170)
cn_im.grid(column=1,row=1,columnspan=3)
cn_im.create_image(0,0,image=img,anchor=NW)

perdre = PhotoImage(file="data/perdre.gif")

def proie00() :
    global PROIE,GRID
    if type(PROIE)!=int :
        i,j=PROIE
        can.delete(GRID[i][j])
        GRID[i][j]=None
        PROIE=0
        proie()
    
def proie() :
    global PROIE,GRID
    A=set()
    for e in SNAKE :
        A.add((e[2],e[1]))
    i,j=SNAKE[0][2],SNAKE[0][1]
    while (i,j) in A :
        i,j=randrange(nl),randrange(nc)
    if PROIE<4 :
        GRID[i][j]=can.create_oval(j*u+2,i*u+2,(j+1)*u-2,(i+1)*u-2,width=0,fill='yellow')
        PROIE+=1
    else :
        GRID[i][j]=can.create_oval(j*u-2,i*u-2,(j+1)*u+2,(i+1)*u+2,width=2,outline='yellow',fill='red')
        PROIE=(i,j)
        can.after((nl+nc)*dt//2,proie00)

def move() :
    global SNAKE,PROIE,DIR,score,Score
    A=set()
    i,j=SNAKE[len(SNAKE)-1][2],SNAKE[len(SNAKE)-1][1]
    for e in SNAKE :
        if e[2]<nl and e[1]<nc and type(GRID[e[2]][e[1]])==tuple :
            e[3]=GRID[e[2]][e[1]]
        if 0<=e[1]+e[3][0]<nc and 0<=e[2]+e[3][1]<nl :
            e[1]=e[1]+e[3][0]
            e[2]=e[2]+e[3][1]
        elif 0<=e[2]+e[3][1]<nl :
            e[1]=nc-e[1]-1
            e[2]=e[2]+e[3][1]
        else :
            e[2]=nl-e[2]-1
            e[1]=e[1]+e[3][0]
        can.coords(e[0],e[1]*u,e[2]*u,(e[1]+1)*u,(e[2]+1)*u)
        A.add((e[1],e[2]))
    if len(A)!=len(SNAKE) :
        DIR=[True]*4
        PROIE=0
        can.create_image(nc*u/2,nl*u/2,image=perdre)
    elif MOVE[m0]==True :
        can.after(dt,move)
    if GRID[SNAKE[0][2]][SNAKE[0][1]]!=None :
        score+=(160-dt+150-nc-nl)//3+14
        can.delete(GRID[SNAKE[0][2]][SNAKE[0][1]])
        l=len(SNAKE)-1
        xl,yl=SNAKE[l][1]-SNAKE[l][3][0],SNAKE[l][2]-SNAKE[l][3][1]
        SNAKE+=[[can.create_rectangle(xl*u,yl*u,(xl+1)*u,(yl+1)*u,fill='red',width=0),xl,yl,SNAKE[l][3]]]
        if type(PROIE)==tuple :
            score+=int((160-dt+150-nc-nl)*1.5)-5
            i,j=PROIE
            can.delete(GRID[i][j])
            GRID[i][j]=None
            PROIE=0
        Score.configure(text='Score   :  '+str(score))
        proie()
    GRID[i][j]=None

def alterner() :
    global m,MOVE,d
    m=1-m
    MOVE=[False,False]
    MOVE[m]=True
    d=0
def UP(event) :
    global DIR
    if DIR[0]==False :
        global GRID,m0
        i,j=SNAKE[0][2],SNAKE[0][1]
        GRID[i][j]=(0,-1)
        alterner()
        move()
        m0=m
        DIR=[True,True,False,False]

def DOWN(event) :
    global DIR
    if DIR[1]==False :
        global GRID,m0
        i,j=SNAKE[0][2],SNAKE[0][1]
        GRID[i][j]=(0,1)
        alterner()
        move()
        m0=m
        DIR=[True,True,False,False]
    
def RIGHT(event) :
    global DIR
    if DIR[2]==False :
        global GRID,m0
        i,j=SNAKE[0][2],SNAKE[0][1]
        GRID[i][j]=(1,0)
        alterner()
        move()
        m0=m
        DIR=[False,False,True,True]
def LEFT(event) :
    global DIR
    if DIR[3]==False :
        global GRID,m0
        i,j=SNAKE[0][2],SNAKE[0][1]
        GRID[i][j]=(-1,0)
        alterner()
        move()
        m0=m
        DIR=[False,False,True,True]

def NEW_GAME() :
    global can,SNAKE,d,GRID,m,m0,MOVE,DIR,PROIE,score,Score
    score=0
    Score.configure(text='Score   :  0')
    MOVE=[False,False]
    DIR=[False,False,False,True]
    m=0
    m0=1
    PROIE=0
    can.destroy()
    SNAKE=[]
    GRID=[[None]*nc for i in range(nl)]
    can=Canvas(fen,height=nl*u,width=nc*u,bg='black')
    can.grid(column=0,row=0,rowspan=10)
    for i in range(nc) :
        can.create_line(i*u,0,i*u,nl*u,fill='green')
    for i in range(nl) :
        can.create_line(0,i*u,nc*u,i*u,fill='green')
    for i in range(3) :
        SNAKE=[[can.create_rectangle((nc//2+i)*u,(nl//2-1)*u,(nc//2+i+1)*u,(nl//2)*u,fill='red',width=0),(nc//2+i),(nl//2-1),(1,0)]]+SNAKE 
    fen.bind("<Up>",UP)
    fen.bind("<Down>",DOWN)
    fen.bind("<Right>",RIGHT)
    fen.bind("<Left>",LEFT)
    proie()
NEW_GAME()

##/ Personnaliser  :
T=Label(fen,text='  personnaliser la partie  : ',font=('Agency FB',15))
T.grid(column=2,row=4,columnspan=3)

vl=StringVar()
el=Entry(fen, textvariable=vl,font=('Agency FB',15),width=5,relief=GROOVE)
el.grid(column=3,row=5)
T1=Label(fen,text='Nombre de lignes',font=('Agency FB',15))
T1.grid(column=2,row=5,sticky=E)
vl.set("20")

vc=StringVar()
ec=Entry(fen, textvariable=vc,font=('Agency FB',15),width=5,relief=GROOVE)
ec.grid(column=3,row=6)
T2=Label(fen,text='Nombre de colonnes',font=('Agency FB',15))
T2.grid(column=2,row=6,sticky=E)
vc.set("20")

vv=StringVar()
ev=Entry(fen, textvariable=vv,font=('Agency FB',15),width=5,relief=GROOVE)
ev.grid(column=3,row=7)
T3=Label(fen,text='Vitesse',font=('Agency FB',15))
T3.grid(column=2,row=7,sticky=E)
vv.set("4")

vu=StringVar()
eu=Entry(fen, textvariable=vu,font=('Agency FB',15),width=5,relief=GROOVE)
eu.grid(column=3,row=8)
Tu=Label(fen,text='Taille',font=('Agency FB',15))
Tu.grid(column=2,row=8,sticky=E)
vu.set("2")

def valider() :
    global vl,vc,vv,vu,u,nl,nc,dt
    if int(vu.get())>5 :
        vu.set('5')
        u=50
    elif  int(vu.get())<1:
        vu.set('1')
        u=10
    else :
        u=10*int(vu.get())
    if int(vl.get())*u>650 :
        vl.set(str(650//u))
        nl=650//u
    elif int(vl.get())<10 :
        vl.set('10')
        nl=10
    else :
        nl=int(vl.get())
    if int(vc.get())*u>1000 :
        vc.set(str(1000//u))
        nc=1000//u
    elif int(vc.get())<10 :
        vc.set('10')
        nc=10
    else :
        nc=int(vc.get())
    if int(vv.get())>6 :
        dt=30
        vv.set('6')
    elif int(vv.get())<1 :
        dt=150
        vv.set('1')
    else :
        dt=160-20*(int(vv.get())-1)
    NEW_GAME()

V=Button(fen,text='   Valider   ',font=('Agency FB',15),command=valider)
V.grid(column=1,row=9,columnspan=3)
B=Button(fen,text='Nouvelle Partie',font=('Agency FB',15),bg='Honeydew3',command=NEW_GAME)
B.grid(column=0,row=10,sticky=E,padx=50)
Q=Button(fen,text='Quitter',font=('Agency FB',15),bg='Honeydew3',command=fen.destroy)
Q.grid(column=0,row=10,sticky=W,padx=50)

fen.mainloop()
    
