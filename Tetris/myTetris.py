##############            TETRIS                  #################    :

from tkinter import *
from random import randrange
fen=Tk()
fen.title('TETRIS')
tet=PhotoImage(file="data/tetris.gif")
ct=Canvas(fen,height=120,width=200)
ct.grid(column=1,row=0,columnspan=3)
ct.create_image(5,5,image=tet,anchor=NW)
score=0
Score=Label(fen,text='Score  : '+str(score),font=('Agency FB',20),fg='red')
Score.grid(column=1,row=2,columnspan=3)
u=30
nl=20
nc=12
L=0
piece=[None]*4
np=0
next=randrange(1,6)
GRID=[[None]*nc for i in range(nl)]
can=Canvas(fen,height=100,width=160,bg='gray')
cn=Canvas(fen,height=100,width=160,bg='gray')
##importer images   :
i1=PhotoImage(file="data/f1.gif")
i2=PhotoImage(file="data/f2.gif")
i3=PhotoImage(file="data/f3.gif")
i4=PhotoImage(file="data/f4.gif")
i5=PhotoImage(file="data/f5.gif")
i6=PhotoImage(file="data/f6.gif")
i7=PhotoImage(file="data/f7.gif")
perdre=PhotoImage(file="data/perdre.gif")

def empty(x,y) :
    emp=False
    if (0<=x//u<nc and 0<=y//u<nl and GRID[y//u][x//u]==None) or y<0 :
        emp=True
    return emp
def move() :
    global piece
    bool=True
    for i in range(4) :
        if not empty(piece[i][1],piece[i][2]+u) :
            bool=False
            break
    if bool==True :
        for i in range(4) :
            piece[i][2]+=u
            x,y=piece[i][1],piece[i][2]
            can.coords(piece[i][0],x,y,x+u,y+u)
        can.after(dt,move)
    else:
        for i in range(4) :
            x,y=piece[i][1],piece[i][2]
            for e in piece :                                                                        #   ces deux lignes uniquement pr
                can.delete(e[0])                                                                    #   changer de couleur  :D
            GRID[y//u][x//u]=can.create_rectangle(x,y,x+u,y+u,fill='Burlywood')                          #piece[i][0]
        for e in range(nl) :
            Del_Line(e*u)
        can.after(dt,n_forme)

## Formes   :
def f1() :
    global piece
    i=0
    for x in [3*u,4*u,5*u,6*u] :
        piece[i]=[can.create_rectangle(x,-u,x+u,0,fill='red'),x,-u]
        i+=1
def f2() :
    global piece
    i=0
    for (x,y) in [(3*u,-u),(4*u,-u),(5*u,-u),(4*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='yellow'),x,y]
        i+=1
def f3() :
    global piece
    i=0
    for x,y in [(3*u,-u),(4*u,-u),(3*u,-2*u),(4*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='Lime Green'),x,y]
        i+=1
def f4() :
    global piece
    i=0
    for x,y in [(4*u,-u),(5*u,-u),(3*u,-2*u),(4*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='violet'),x,y]
        i+=1
def f5() :
    global piece
    i=0
    for x,y in [(3*u,-u),(4*u,-u),(4*u,-2*u),(5*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='Cornflower Blue'),x,y]
        i+=1
def f6() :
    global piece
    i=0
    for (x,y) in [(3*u,-u),(4*u,-u),(5*u,-u),(3*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='Medium Spring Green'),x,y]
        i+=1
def f7() :
    global piece
    i=0
    for (x,y) in [(3*u,-u),(4*u,-u),(5*u,-u),(5*u,-2*u)] :
        piece[i]=[can.create_rectangle(x,y,x+u,y+u,fill='Light Yellow'),x,y]
        i+=1
def n_forme() :   #creer une nvelle forme
    global piece,np,dt,next,dt0,L
    P=False
    for i in range(3,5) :
        if not empty(i*u,0) :
            can.create_image(nc*u//2,nl*u//2,image=perdre)
            P=True
    if P==False :
        np+=1
        dt=dt0
        eval('f'+str(next)+'()')
        next=randrange(1,8)
        cn.delete(ALL)
        cn.create_image(80,50,image=eval('i'+str(next)))
        can.after(dt,move)

## Clavier    :
def gauche(event) :
    global piece
    bool=True
    for i in range(4) :
        if not empty(piece[i][1]-u,piece[i][2]) :
            bool=False
            break
    if bool==True :
        for i in range(4) :
            piece[i][1]-=u
            x,y=piece[i][1],piece[i][2]
            can.coords(piece[i][0],x,y,x+u,y+u)

def droite(event) :
    global piece
    bool=True
    for i in range(4) :
        if not empty(piece[i][1]+u,piece[i][2]) :
            bool=False
            break
    if bool==True :
        for i in range(4) :
            piece[i][1]+=u
            x,y=piece[i][1],piece[i][2]
            can.coords(piece[i][0],x,y,x+u,y+u)

def rapidos(event) :
    global dt
    dt=1

## Personnaliser :
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
vc.set("12")

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
vu.set("3")

def valider() :
    global vl,vc,vv,vu,u,nl,nc,dt0
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
    else :
        nl=int(vl.get())
    if int(vc.get())*u>1000 :
        vc.set(str(1000//u))
        nc=1000//u
    else :
        nc=int(vc.get())
    if int(vv.get())>8 :
        vv.set('8')
    else :
        print('yes')
    NEW_GAME()

## autres Fonctions   :
def Del_Line(y) :
    global GRID,L,Score,score,dt0
    j=y//u
    D=True
    for i in range(nc) :
        if GRID[j][i]==None :
            D=False
    if D==True :
        score+=nl*nc-(nl*nc)%50
        Score.configure(text='Score  : '+str(score))
        L+=1
        # Accélérer après à chaque 15 lignes complétées
        if L==15 :
            print(dt0)
            L=0
            if dt0 > 160 :
            	dt0=dt0-20
        for e in GRID[j] :
            can.delete(e)
        GRID.remove(GRID[j])
        GRID=[[None]*nc]+GRID
        for p in range(1,j+1) :
            for i in range(nc) :
                if GRID[p][i]!=None :
                    can.coords(GRID[p][i],i*u,(p)*u,(i+1)*u,(p+1)*u)

def rotate(event) :
    global piece
    pieceO=piece
    bool=True
    xM,yM,ym=piece[0][1],piece[0][2],piece[0][2]
    for e in piece :
        if e[2]>yM :
            yM=e[2]
        if e[2]<ym :
            ym=e[2]
        if e[1]>xM:
            xM=e[1]
    for i in range(4) :
        if not empty(xM+piece[i][2]-yM,ym-piece[i][1]+xM) :
            bool=False
            break
    if bool==True :
        for i in range(4) :
            x,y=piece[i][1],piece[i][2]
            piece[i][1]=xM+y-yM
            piece[i][2]=ym-x+xM
            can.coords(piece[i][0],piece[i][1],piece[i][2],piece[i][1]+u,piece[i][2]+u)

def NEW_GAME() :
    global can,cn,nc,nl,u,can,GRID,score,dt0
    dt0=500-50*int(vv.get())
    can.destroy()
    cn.destroy()
    can=Canvas(fen,height=u*nl,width=u*nc,bg='black',relief=GROOVE)
    can.grid(column=0,row=0,rowspan=10)
    cn=Canvas(fen,height=100,width=160,bg='black')
    cn.grid(column=1,row=1,padx=50,columnspan=3)
    GRID=[[None]*nc for i in range(nl)]
    score=0
    Score.configure(text='Score  : 0')
    for i in range(nc) :
        can.create_line(i*u,0,i*u,nl*u,fill='green')
    for i in range(nl) :
        can.create_line(0,i*u,nc*u,i*u,fill='green')
    fen.bind("<Left>",gauche)  
    fen.bind("<Right>",droite)
    fen.bind("<Down>",rapidos)
    fen.bind("<Up>",rotate)
    n_forme()
NEW_GAME()



V=Button(fen,text='   Valider   ',font=('Agency FB',15),command=valider)
V.grid(column=1,row=9,columnspan=3)
B=Button(fen,text='Nouvelle Partie',font=('Agency FB',12),bg='Honeydew3',command=NEW_GAME)
B.grid(column=0,row=10,sticky=E,padx=50)
Q=Button(fen,text='Quitter',font=('Agency FB',12),bg='Honeydew3',command=fen.destroy)
Q.grid(column=0,row=10,sticky=W,padx=50)
fen.mainloop()
