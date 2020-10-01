from tkinter import *
from math import *
from random import randrange
fen=Tk()
fen.title("myBird")
u=15
B=[]
q=0
can=Canvas()
score=0
Score=Label(fen,text='Score   :  '+str(score),font=('Agency FB',30),fg='red',bg='black')
Score.grid(column=1,row=1)
dm,dM=150,190
dt=1400
v=3
h0=0
col=['blue','ivory','Lime green','red','pink','purple','black','Khaki','yellow','Dark Goldenrod','yellow','Firebrick','Thistle','yellow']
##/ Images :
Bh=[PhotoImage(file="data/Bhaut.gif"),PhotoImage(file="data/Bhaut1.gif"),PhotoImage(file="data/Bhaut2.gif"),PhotoImage(file="data/Bhaut3.gif")]
Bb=[PhotoImage(file="data/Bbas.gif"),PhotoImage(file="data/Bbas1.gif"),PhotoImage(file="data/Bbas2.gif"),PhotoImage(file="data/Bbas3.gif")]
herbe=PhotoImage(file="data/herbe.gif")
img=PhotoImage(file="data/bird.png")
perdre=PhotoImage(file="data/perdre.gif")
eyes=PhotoImage(file="data/eyes.gif")
wing=PhotoImage(file="data/wing.gif")
tree=PhotoImage(file="data/tree.gif")
rock=PhotoImage(file="data/rock.gif")
cn=Canvas(height=200,width=190)
cn.grid(column=1,row=0)
cn.create_image(5,10,image=img,anchor=NW)
##/  Fonctions  :
def delete_B() :
    global B
    e=0
    while B[e][1]<-100 :
        can.delete(B[e][0])
        can.delete(B[e][3])
        can.delete(B[e][5])
        B.remove(B[e])
    can.after(3*dt,delete_B)
def barriere() :
    global B,h0,Bh,Bb,q,dt,dh
    h=randrange(20,35)
    while abs(h-h0)<dh :
        h=randrange(20,35)
    h0=h
    d=randrange(dm,dM)
    if (score+3)%50==0 :
        dh-=1.5
        if q<len(Bh)-1 :
            q+=1
        else :
            q=0
    B+=[[can.create_image(760,h*u,image=Bb[q],anchor=NW),760,h*u,can.create_image(760,h*u-d,image=Bh[q],anchor=SW),h*u-d,can.create_image(0,600,image=herbe,anchor=NW),1]]
    can.after(dt,barriere)

def move() :
    global a,y,x,B,score,Score,v,dm,dM,dt
    if y<550 :
        a+=0.055
        y=y0+60*(a**2-4*a+3)
        can.coords(BIRD[0],150,y,200,y+50)
        can.coords(BIRD[1],175,y-30+15*a)
        can.coords(BIRD[2],140,y+15-10*sin(5*a))
        for b in B :
            can.coords(b[0],b[1]-v,b[2])
            can.coords(b[3],b[1]-v,b[4])
            can.coords(b[5],b[1]-v,600)
            b[1]-=v
            if (y-b[4]<-4 or b[2]-y<45) and -90<(b[1]-150)<42 :
                y=600
            elif -90<(b[1]-150)<42 and b[6]!=0 :
                score+=1
                Score.configure(text='Score   :  '+str(score))
                b[6]=0
                if (score+3)%10==0:
                    if dt>=1120:
                        dt-=20
                    if dm>=120 :
                        dm,dM=dm-5,dM-10
                        if dM<=dm :
                            dM=dm+10
        can.after(15,move)
        if y>550 :
            can.create_image(320,375,image=perdre)
        
def up(event) :
    global a,y0
    if y>-50 :
        a=1
        y0=y
def start(event) :
    global K
    if K==True :
        K=False
        a=1
        move()
        can.after(dt,barriere)
        delete_B()
        can.delete(Textt)

def NEW_GAME() :
    global can,B,y,y0,a,BIRD,can,K,fond,score,SCORE,Textt,dt,dm,dM,q,dh
    q=0
    dm,dM=170,200
    dt=1400
    dh=4
    can.destroy()
    can=Canvas(fen,height=43*u,width=50*u,bg='black')
    can.grid(column=0,row=0,rowspan=5)
    #for i in range(50) :
    #    can.create_line(i*u,0,i*u,40*u,fill='green')
    #for i in range(40) :
    #    can.create_line(0,i*u,50*u,i*u,fill='green')
    f="data/fond"+str(randrange(5))+".gif"
    fond=PhotoImage(file=f)
    can.create_image(0,0,image=fond,anchor=NW)
    BIRD=[can.create_oval(150,150,200,200,fill=col[randrange(len(col))],width=2),can.create_image(175,153,image=eyes,anchor=NW),can.create_image(140,170,image=wing,anchor=NW)]
    Tex=Label(fen,text='appuyez sur <Entrer>\n pour commencer',font=('Agency FB',25),fg='black')
    Textt=can.create_window(400,250,window=Tex)
    for i in range(8) :
        can.create_image(i*100,600,image=herbe,anchor=NW)
    B=[[can.create_image(30,-55,image=tree,anchor=NW),30,-55,can.create_image(30,510,image=rock,anchor=NW),510,can.create_image(0,600,image=herbe,anchor=NW),0]]
    score=0
    Score.configure(text='Score   :  0')
    a=1
    y0=150
    y=150
    K=True
    fen.bind("<Return>",start)
    fen.bind("<Up>",up)
NEW_GAME()
N=Button(fen,text='Nouvelle Partie',width=10,font=('Agency FB',15),bg='Honeydew3',command=NEW_GAME)
N.grid(column=1,row=3,padx=50)
Q=Button(fen,text='Quitter',width=10,font=('Agency FB',15),bg='Honeydew3',command=fen.destroy)
Q.grid(column=1,row=4,padx=50)
fen.mainloop()
