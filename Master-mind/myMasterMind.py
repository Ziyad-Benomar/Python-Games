from tkinter import *
from math import *
from random import *
import time
fen=Tk()
fen.title("myMasterMind")
fen.attributes("-fullscreen", 1)
can=Canvas(fen,height=800,width=1500,bg='ivory')
can.pack()

i_bg=PhotoImage(file="data/bg.gif")
i_table=PhotoImage(file="data/table.gif")
i_trou=PhotoImage(file="data/trou.gif")
i_code=PhotoImage(file="data/code.gif")
i_nr=PhotoImage(file="data/nr.gif")
i_nb=PhotoImage(file="data/nb.gif")
i_tr=PhotoImage(file="data/tr.gif")
i_tv=PhotoImage(file="data/tv.gif")
i_tm=PhotoImage(file="data/tm.gif")
i_tb=PhotoImage(file="data/tb.gif")
i_trs=PhotoImage(file="data/trs.gif")
i_tbc=PhotoImage(file="data/tbc.gif")
i_tg=PhotoImage(file="data/tg.gif")
i_tj=PhotoImage(file="data/tj.gif")
i_cr=PhotoImage(file="data/cr.gif")
i_cv=PhotoImage(file="data/cv.gif")
i_cm=PhotoImage(file="data/cm.gif")
i_cb=PhotoImage(file="data/cb.gif")
i_crs=PhotoImage(file="data/crs.gif")
i_cbc=PhotoImage(file="data/cbc.gif")
i_cg=PhotoImage(file="data/cg.gif")
i_cj=PhotoImage(file="data/cj.gif")
i_perdu=PhotoImage(file="data/perdu.gif")
i_gagne=PhotoImage(file="data/gagne.gif")
i_Vld=PhotoImage(file="data/Vld.gif")
i_ANL=PhotoImage(file="data/ANL.gif")
i_Q=PhotoImage(file="data/quitter.gif")
can.create_image(0,0,image=i_bg,anchor=NW)
R,B=[],[]
for j in range (10) :
    R+=[can.create_image(225,170+50*j,image=i_nr,anchor=NW)]#45
    B+=[can.create_image(375,170+50*j,image=i_nb,anchor=NW)]
can.create_image(250,0,image=i_table,anchor=NW)

for j in range(10) :
    for i in range(4) :
        can.create_image(305+60*i,180+50*j,image=i_trou,anchor=NW)
can.create_image(1000,200,image=i_cb,anchor=NW)
can.create_image(1000,300,image=i_cg,anchor=NW)
can.create_image(1000,400,image=i_cr,anchor=NW)
can.create_image(1000,500,image=i_crs,anchor=NW)
can.create_image(1100,200,image=i_cj,anchor=NW)
can.create_image(1100,300,image=i_cm,anchor=NW)
can.create_image(1100,400,image=i_cv,anchor=NW)
can.create_image(1100,500,image=i_cbc,anchor=NW)
a=0
nr=0
nb=0
j=9
i=0
def move_r() :
    global a,nr,j
    a+=0.001
    x=-45*nr*sin(a)+225
    if a<3.14/2 :
        can.coords(R[j],x,170+50*j)
        can.after(1,move_r)

def move_b() :
    global a,nb,j
    a+=0.001
    x=45*nb*sin(a)+375
    if a<3.14/2 :
        can.coords(B[j],x,170+50*j)
        can.after(1,move_b)
    else :
        modify()
    

def move() :
    global a,j,nr,nb
    a=0
    move_r()
    move_b()
def modify() :
    global L,j,nb,nr,a,V
    L=[]
    j=j-1
    nb,nr=0,0
    a=0
    V=True

COULEUR=[['tb','tj'],['tg','tm'],['tr','tv'],['trs','tbc']]
###/ PROG PRICIPAL   :
#CHOIX DU CODE SECRET :
CODE=[]
for p in range(4) :
    CODE+=[COULEUR[randrange(4)][randrange(1)]]
    can.create_image(305+60*p,80,image=eval('i_'+CODE[p]),anchor=NW)
H=can.create_image(290,70,image=i_code,anchor=NW)
print(CODE)
L=[]
def pointeur(event) :
    global L
    i=len(L)
    xp=(event.x-1000)//100
    yp=(event.y-200)//100
    if xp in [0,1] and yp in range(4) and i<4 and j>=0:
        L+=[[can.create_image(305+60*i,180+50*j,image=eval('i_'+COULEUR[yp][xp]),anchor=NW),COULEUR[yp][xp]]]
can.bind("<Button-1>",pointeur)

V=True
def valider() :
    global nb,nr,L,V,j,a
    T=CODE[:]
    if V==TRUE and len(L)==4 :
        for k in range(4) :
            if L[k][1]==T[k] :
                L[k][1]=None
                T[k]='checked'
                nr+=1
        for k in range(4) :
            for e in range(4) :
                if L[k][1]==T[e] :
                    L[k][1]=None
                    T[e]='checked'
                    nb+=1
        
        move()
        g=nr
        V=False
        if g==4 :
            can.unbind(pointeur)
            print ('VOUS AVEZ GAGNE')
            can.create_image(800,300,image=i_gagne)
            show()
            
        elif j<1 :
            can.unbind(pointeur)
            print ('PERDU')
            can.create_image(800,300,image=i_perdu)
            show()
def annuler() :
    global L
    l=len(L)-1
    can.delete(L[l][0])
    L.remove(L[l])
t=0
def show() :
    global t
    t+=0.001
    y=-70*sin(t)+70
    if t<3.14/2 :
        can.coords(H,290,y)
        can.after(1,show)

BA=Button(fen,image=i_ANL,command=annuler,anchor=NW)
BV=Button(fen,image=i_Vld,command=valider,anchor=NW)
BQ=Button(fen,image=i_Q,command=fen.destroy,anchor=NW)
can.create_window(900,350,window=BV)
can.create_window(900,450,window=BA)
can.create_window(1090,650,window=BQ)
    
fen.mainloop()
