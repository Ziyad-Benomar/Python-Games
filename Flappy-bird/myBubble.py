from tkinter import *
from random import *
fen=Tk()
fen.geometry("1275x640")
fen.resizable(0,0)
fen.title('myBubble')
can=Canvas(fen)
#BALL  :  [img,d,x0,y0,t,s]
COL=['Thistle','Lime green','violet','Dark Goldenrod','yellow','red']
c=COL[randrange(len(COL))]
Ball=[]
SB=[(10,300,4,0.04),(20,375,4.25,0.035),(30,450,4.5,0.03),(50,525,4.75,0.028),(80,600,5,0.025),(120,675,5.25,0.022),(180,750,5.5,0.02),(250,825,5.75,0.018)]
GAME_OVER=False
im1=PhotoImage(file="data/im1.gif")
im2=PhotoImage(file="data/im2.gif")
sl=PhotoImage(file="data/sl.gif")
vie=PhotoImage(file="data/vie.gif")
perso=PhotoImage(file="data/perso.gif")
perdre=PhotoImage(file="data/perdre.gif")
fond=PhotoImage(file="data/fond.gif")
img=PhotoImage(file="data/img.gif")
pause=PhotoImage(file="data/pause.gif")

cn=Canvas(fen,height=150,width=200)
cn.grid(column=1,row=0)
cn.create_image(-20,0,image=img,anchor=NW)


Player=[can.create_image(300,610,image=perso),0,500]
can.create_image(0,0,image=im2,anchor=NW)
VIE=[]
laser=PhotoImage(file="data/laser.gif")
Laser=[]

Score=Label(fen,text='Score   :  0',font=('Agency FB',20),fg='red',bg='black')
Score.grid(column=1,row=1)

def identify(B) :
    c=0
    for e in SB :
        if e[0]==B[1] :
            return e,c
            break
        else :
            c+=1
def ACT_Coll0() :
    global Player
    u=Player.pop()
    v=Player.pop()
    can.delete(u)
    can.delete(v)
def ACT_Coll() :
    global Player,A
    if A==True :
        u=Player.pop()
        v=Player.pop()
        can.delete(u)
        can.delete(v)
    A=False
def Coll(B,y,yObjet,Objet) :
    x0=B[2]+B[1]//2
    y0=y+B[3]+B[1]//2
    if ((Objet[2]-x0)**2+(yObjet-y0)**2)**0.5<=B[1]//2+15:
        return True
    else :
        return False

def del_bonus() :
    global Bonus
    if Bonus!=[] :
        can.delete(Bonus[0][0])
        Bonus.remove(Bonus[0])
def nv_bonus() :
    global Bonus
    i=randrange(2)
    x=20*randrange(2,49)
    if i==1 :
        IM=can.create_image(x,560,image=vie,anchor=NW)
    else :
        IM=can.create_oval(x,560,x+40,600,width=4,outline='Gold')
    Bonus+=[[IM,x,i]]
    can.after(8000,del_bonus)


def diviser(B) :
    global Ball,score,Score
    e,c=identify(B)
    y=e[1]*(B[4]**2-B[4])
    xn,yn=B[2],y+B[3]
    if c>0 :
        d=SB[c-1][0]
        Ball+=[[can.create_oval(xn,yn,xn+d,yn+d,fill=B[6]),d,xn+(B[1]-d)//2,yn+(B[1]*2)//3,0.2,1,B[6]],[can.create_oval(xn,yn,xn+d,yn+d,fill=B[6]),d,xn+(B[1]-d)//2,yn+(B[1]*2)//3,0.2,-1,B[6]]]
    can.delete(B[0])
    if B in Ball :
        Ball.remove(B)
    score+=1
    Score.configure(text='Score   :  '+str(score))
    if score%15==0 and score>0 and Bonus==[]:
        nv_bonus()
def insane() :
    global Ball
    j=randrange(len(SB)-1)
    c=COL[randrange(len(COL))]
    Ball+=[[can.create_oval(10,-SB[j][0],60,-300,fill=c),SB[j][0],-SB[j][0],400,0,1,c]]
    can.after((2**j)*1000,insane)

    
def move() :
    global Ball,Player,P,Laser,VIE,GAME_OVER,n,I,A,nv
    if 5<Player[2]+Player[1]<995 :
        Player[2]+=Player[1]
        can.coords(Player[0],Player[2],570)
        if len(Player)!=3 :
            can.coords(Player[3],Player[2]-30,540,Player[2]+30,610)
            can.coords(Player[4],Player[2]-30,600)
    for L in Laser :
        L[2]-=20
        can.coords(L[0],L[1],L[2])
        if L[2]<0 :
            can.delete(L[0])
            can.delete(L[3])
            Laser.remove(L)
    for B in Ball :
        e=identify(B)[0]
        B[4]+=e[3]
        B[2]+=B[5]*e[2]
        y=e[1]*(B[4]**2-B[4])
        if y+B[3]+B[1]>600 :
            B[3]=600-B[1]
            B[4]=0
        if B[2]+B[1]>1000 or (B[2]<0 and B[5]==-1) :
            B[5]=-B[5]
        x0=B[2]+B[1]//2
        y0=y+B[3]+B[1]//2
        if y+B[3]<50 :
            can.delete(B[0])
            Ball.remove(B)
        for L in Laser :
            if 0<L[1]-B[2]<B[1]-5 and L[2]<=B[3]+y+B[1]  :
                diviser(B)
                can.delete(L[0])
                can.delete(L[3])
                Laser.remove(L)
        if Coll(B,y,570,Player) and len(Player)==3:
            A=True
            if nv==1 :
                can.delete(VIE[0])
                can.create_image(500,325,image=perdre)
                GAME_OVER=True
            else :
                nv-=1
                can.delete(VIE[0])
                VIE.remove(VIE[0])
                Player+=[can.create_oval(Player[2]-30,540,Player[2]+30,610,outline='red',width=5),can.create_image(Player[2]-10,600,image=sl,anchor=NW)]
            can.after(3000,ACT_Coll)
        can.coords(B[0],B[2],B[3]+y,B[2]+B[1],B[3]+y+B[1])
    for b in Bonus :
        if Player[2]-50<b[1]<Player[2] :
            u=b[2]
            can.delete(b[0])
            Bonus.remove(b)
            if u==1 :
                nv+=1
                VIE=[can.create_image(40*nv-30,10,image=vie,anchor=NW)]+VIE
            else :
                ACT_Coll()
                Player+=[can.create_oval(Player[2]-30,540,Player[2]+30,610,outline='Gold',width=5),can.create_image(Player[2]-10,600,image=sl,anchor=NW)]
                can.after(15000,ACT_Coll0)
    if Ball==[] :
        n+=1
        if n<len(SB) :
            c=COL[randrange(len(COL))]
            Ball=[[can.create_oval(10,-SB[n][0],60,-300,fill=c),SB[n][0],-SB[n][0],400,0,1,c]]
        elif not I :
            I=True
            insane()
    if not GAME_OVER and PAUSE==False :
        can.after(30,move)

def Droite(event) :
    global Player
    Player[1]=5
def Gauche(event) :
    global Player
    Player[1]=-5
def Stop(event) :
    global Player
    Player[1]=0
def Tir(event) :
    global Laser
    if len(Laser)==0 :
        Laser+=[[can.create_image(Player[2]-5,540,image=laser,anchor=NW),Player[2]-5,540,can.create_image(Player[2]-10,600,image=sl,anchor=NW)]]
def Pause(event) :
    global PAUSE
    if PAUSE==False :
        can.delete(PAUSE)
        PAUSE=can.create_image(500,325,image=pause)
    else :
        can.delete(PAUSE)
        PAUSE=False
        move()
        
def NEW_GAME() :
    global can,Player,Ball,VIE,GAME_OVER,n,I,score,Score,Bonus,A,nv,PAUSE
    GAME_OVER=False
    PAUSE=False
    I=False
    A=False
    n=0
    score=0
    Score.configure(text='Score   :  0')
    can.destroy()
    can=Canvas(fen,height=650,width=1000,bg='navy')
    can.grid(column=0,row=0,rowspan=5)
    can.create_image(0,0,image=fond,anchor=NW)
    can.create_image(0,600,image=im1,anchor=NW)
    can.create_image(0,0,image=im2,anchor=NW)
    c=COL[randrange(len(COL))]
    Ball=[[can.create_oval(10,300,60,350,fill=c),10,-10,400,0,1,c]]
    Player=[can.create_image(300,610,image=perso),0,500]
    nv=5
    for i in range(5) :
        VIE=[can.create_image(10+40*i,10,image=vie,anchor=NW)]+VIE
    Bonus=[]
    fen.bind("<Right>",Droite)
    fen.bind("<Left>",Gauche)
    fen.bind("<Down>",Stop)
    fen.bind("<Up>",Tir)
    fen.bind("<Return>",Pause)
    move()
NEW_GAME()

N=Button(fen,text='Nouvelle Partie',width=10,font=('Agency FB',15),bg='Honeydew3',command=NEW_GAME)
N.grid(column=1,row=3,padx=50)
Q=Button(fen,text='Quitter',width=10,font=('Agency FB',15),bg='Honeydew3',command=fen.destroy)
Q.grid(column=1,row=4,padx=50)

fen.mainloop()
