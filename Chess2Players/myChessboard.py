##############        CHESS       ################  :       02/07/2016



##/ Variables du jeu :
joueur,adversaire='White','Black'
xp,yp=1,6    # coordonnees du clic
piece=None  # piece selectionnee
m0=0
White,Black,Eventual,Coords,Cev,KING_EV,TRACE,E=[],[],[],[],[],[],[],[]

# White/Black : les pions
# Eventual : mvts eventuels de piece
# Coords : liste de listes L :len(L)=4, L=[x,y,'White'/'Black',0,i] definit un pion


##/ Initialisation fenetre et importer images :

from tkinter import *
fen=Tk()
fen.title("myChessboard")
fen.geometry("1136x700")
fen.resizable(0,0)
player=Canvas(fen,height=700,width=400)
player.pack(side=LEFT)
txtEmatt=PhotoImage(file="data/echecematt.gif")
txtChoisir=PhotoImage(file="data/choisir.gif")
txtEchec=PhotoImage(file="data/echec.gif")
imCadre=PhotoImage(file="data/cadre.gif")
imTable=PhotoImage(file="data/table.gif")
Cadre=Canvas(fen,height=700,width=730)
can=Canvas(fen,bg='ivory',height=600,width=600)
can.create_image(0,0,image=imTable)
Cadre.pack(side=LEFT)
Cadre.create_image(0,0,image=imCadre,anchor=NW)
Cadre.create_window(65,50,window=can,anchor=NW)

for j in range(8) :
    x=(75*(1+(-1)**j))//2
    y=(j+1)*75
    for i in range(0,4) :
        can.create_rectangle(x,y,x+75,y-75,width=2,fill='black')
        x=x+150


bli0=PhotoImage(file="data/pions/roin.gif")
bli1=PhotoImage(file="data/pions/pionn.gif")
bli2=PhotoImage(file="data/pions/foun.gif")
bli3=PhotoImage(file="data/pions/cavaliern.gif")
bli4=PhotoImage(file="data/pions/tourn.gif")
bli5=PhotoImage(file="data/pions/reinen.gif")

whi0=PhotoImage(file="data/pions/roib.gif")
whi1=PhotoImage(file="data/pions/pionb.gif")
whi2=PhotoImage(file="data/pions/foub.gif")
whi3=PhotoImage(file="data/pions/cavalierb.gif")
whi4=PhotoImage(file="data/pions/tourb.gif")
whi5=PhotoImage(file="data/pions/reineb.gif")

## MINIATURES  : 

mbli1=PhotoImage(file="data/miniatures/pionn.gif")
mbli2=PhotoImage(file="data/miniatures/foun.gif")
mbli3=PhotoImage(file="data/miniatures/cavaliern.gif")
mbli4=PhotoImage(file="data/miniatures/tourn.gif")
mbli5=PhotoImage(file="data/miniatures/reinen.gif")

mwhi1=PhotoImage(file="data/miniatures/pionb.gif")
mwhi2=PhotoImage(file="data/miniatures/foub.gif")
mwhi3=PhotoImage(file="data/miniatures/cavalierb.gif")
mwhi4=PhotoImage(file="data/miniatures/tourb.gif")
mwhi5=PhotoImage(file="data/miniatures/reineb.gif")


dead1=Canvas(fen,height=150,width=250,bg='Light Goldenrod')
dead2=Canvas(fen,height=150,width=250,bg='Light Goldenrod')
fond=PhotoImage(file="data/player.gif")
player.create_image(0,0,image=fond,anchor=NW)
player.create_window(75,450,window=dead1,anchor=NW)
player.create_window(75,200,window=dead2,anchor=NW)

for j in range(3) :
    x=(50*(1+(-1)**j))//2
    y=(j+1)*50
    for i in range(3) :
        if x<=200 :
            dead1.create_rectangle(x,y,x+50,y-50,width=1,fill='black')
            dead2.create_rectangle(x,y,x+50,y-50,width=1,fill='black')
        x=x+100
C1,C2=[],[]
I1,I2=[],[]
##/ fonctions generales  :
def empty(x,y) :  # verifie si la case (c,y) est vide ou non
    c=True
    if not (0<=x<8 and 0<=y<8) :
        c=False
    else :
        for e in Coords :
            if (e[0],e[1])==(x,y) :
                c=False
                break
    return c

def king(patrie) :
    for e in Coords :
        if (e[2],e[3])==(patrie,0) :
            return e[0],e[1]
            break

def identify(x,y) :
    I=[None]*4
    for e in Coords :
        if (e[0],e[1])==(x,y) :
            I=e
            break
    return I

def test(x,y) :
    global Coords, Eventual ,Cev
    e=identify(xp,yp)
    v=identify(x,y)
    s=0
    if v[0]!=None :
        Coords.remove(v)
        s=1
    Coords+=[[x,y,e[2],e[3]]]
    Coords.remove(e)
    xk,yk=king(joueur)
    if echec(xk,yk,joueur) :
        Eventual+=[can.create_rectangle(x*75+3,y*75+3,(x+1)*75-2,(y+1)*75-2,outline='Indian Red',width=6)]
    else :    
        Eventual+=[can.create_rectangle(x*75+2,y*75+2,(x+1)*75-2,(y+1)*75-2,outline='blue',width=4)]
        Cev+=[(x,y)]
    if s==1 :
        Coords+=[v]
    Coords.remove([x,y,e[2],e[3]])
    Coords+=[e]
        
    
    
def blue_erase() :
    global Eventual,Cev
    T=Eventual
    for e in T :
        can.delete(e)
    Eventual,Cev=[],[]

def miniaturiser(d) :
    global I1,I2,C1,C2,dead1,dead2
    if d[2]=='White' :
        n=len(C1)
        y=(n//5)*50
        x=(n%5)*50
        C1+=[d+[x//50,y//50]]
        D=dead1
        m1,m2,m3,m4,m5=mwhi1,mwhi2,mwhi3,mwhi4,mwhi5
        I=I1
    else :
        n=len(C2)
        y=(n//5)*50
        x=(n%5)*50
        C2+=[d+[x//50,y//50]]
        D=dead2
        m1,m2,m3,m4,m5=mbli1,mbli2,mbli3,mbli4,mbli5
        I=I2
    
    if d[3] in [1,6,10,11,12,13,14,15] :
        I+=[D.create_image(x,y,image=m1,anchor=NW)]
    elif d[3]==5 :
        I+=[D.create_image(x,y,image=m5,anchor=NW)]
    elif d[3] in [4,9] :
        I+=[D.create_image(x,y,image=m4,anchor=NW)]
    elif d[3] in [3,8] :
        I+=[D.create_image(x,y,image=m3,anchor=NW)]
    elif d[3] in [2,7] :
        I+=[D.create_image(x,y,image=m2,anchor=NW)]

def pick(event) :
    global dead1,dead2,I1,I2,adversaire,E
    PICK=True
    if C1!=[] and C1[0][2]==adversaire :
        C=C1
        I=I1
        D=dead1
    else :
        C=C2
        I=I2
        D=dead2
    j=None
    xc,yc=event.x//50,event.y//50
    d=[None]*6
    for i in range(len(C)) :
        e=C[i]
        if (e[4],e[5])==(xc,yc) :
            d=e[:]
            e[3]=1
            j=i
            break
    v=identify(xp,yp)
    for u in Coords :
        if u==v :
            u[3]=d[3]
    L=[]
    if d[2]=='White' :
        m0,m1,m2,m3,m4,m5=mwhi1,whi1,whi2,whi3,whi4,whi5
        L=White
    else :
        m0,m1,m2,m3,m4,m5=mbli1,bli1,bli2,bli3,bli4,bli5
        L=Black
    if d[3] in [1,None] and C!=[] :
        PICK=False
    else :
        player.delete(E[0])
        D.delete(I[j])
        can.delete(piece)
        D.create_image(xc*50,yc*50,image=m0,anchor=NW)
    if d[3]==5 :
        L[d[3]]=can.create_image(xp*75,yp*75,image=m5,anchor=NW)
    elif d[3] in [4,9] :
        L[d[3]]=can.create_image(xp*75,yp*75,image=m4,anchor=NW)
    elif d[3] in [3,8] :
        L[d[3]]=can.create_image(xp*75,yp*75,image=m3,anchor=NW)
    elif d[3] not in[1,None] :
        L[d[3]]=can.create_image(xp*75,yp*75,image=m2,anchor=NW)
    trace_echec()
    if PICK :
        trace_echec()
        D.unbind("<Button-1>")
        can.bind("<Button-1>",pointeur)    

#def transformer(pion) :
    
    
        

##/ fonctions de deplacement :
# move()       :  deplace piece vers (xp,yp)
# deplacer0()  :  roi
# deplacer1()  :  pion
# deplacer2()  :  fou
# deplacer3()  :  cavalier
# deplacer4()  :  tour
# deplacer5()  :  reine
def move() :
    global m0,piece,Coords,Eventual,TRACE,E
    for e in TRACE :
        can.delete(e)
    player.delete(E[0])
    blue_erase()
    v=identify(xp,yp)
    can.coords(piece,75*xp,75*yp)
    if v[0]!=None :
        miniaturiser(v)
        Coords.remove(v)
        can.delete(eval(adversaire+'['+str(v[3])+']'))
    for e in Coords :
        if (e[2],e[3])==(joueur,m0) :
            e[0],e[1]=xp,yp
            break

def trace_echec() :
    global TRACE,E
    xk,yk=king(adversaire)
    x,y=xp,yp
    if echec(xk,yk,adversaire) :
        if m0 in [3,8] :
            TRACE+=[can.create_rectangle(xp*75+2,yp*75+2,(xp+1)*75-2,(yp+1)*75-2,outline='red',width=4)]
            TRACE+=[can.create_rectangle(xk*75+2,yk*75+2,(xk+1)*75-2,(yk+1)*75-2,outline='red',width=4)]
        else :
            s1,s2=0,0
            if xk!=x :
                s1=abs(xk-xp)//int(xk-x)
            if yk!=y :
                s2=abs(yk-yp)//int(yk-y)
            TRACE+=[can.create_rectangle(xk*75+2,yk*75+2,(xk+1)*75-2,(yk+1)*75-2,outline='red',width=4)]
            while(xk,yk)!=(x,y) :
                TRACE+=[can.create_rectangle(x*75+2,y*75+2,(x+1)*75-2,(y+1)*75-2,outline='red',width=4)]
                x,y=x+s1,y+s2
        if matt() :
            E=[player.create_image(60,355,image=txtEmatt,anchor=NW)]
        else :
            E=[player.create_image(60,355,image=txtEchec,anchor=NW)]

def eventual_king(patrie) :
    global Coords
    B=[]
    G=[]
    xk,yk=king(patrie)
    for (x,y) in [(xk-1,yk-1),(xk-1,yk),(xk-1,yk+1),(xk,yk-1),(xk,yk+1),(xk+1,yk-1),(xk+1,yk),(xk+1,yk+1)] :
        if 0<=x<8 and 0<=y<8 and identify(x,y)[2]!= patrie :
            e=identify(xk,yk)
            Coords+=[[x,y,patrie,0]]
            Coords.remove(e)
            if echec(x,y,patrie) :
                G+=[(x,y)]
            else :    
                B+=[(x,y)]
            Coords.remove([x,y,e[2],e[3]])
            Coords+=[e]
    return B,G
def deplacer0() :
    global Eventual,Cev,Coords
    B,G=eventual_king(joueur)
    for x,y in G :
        Eventual+=[can.create_rectangle(x*75+3,y*75+3,(x+1)*75-2,(y+1)*75-2,outline='Indian Red',width=6)]
    for x,y in B :
        Eventual+=[can.create_rectangle(x*75+2,y*75+2,(x+1)*75-2,(y+1)*75-2,outline='blue',width=4)]
        Cev+=[(x,y)]
    
def deplacer1() :
    global Eventual,Cev
    x,y=xp,yp
    if joueur=='White' :
        s=-1
    else :
        s=1
    if empty(x,y+s) :
        test(x,y+s)
    for c  in [-1,1] :
        if identify(x+c,y+s)[2]==adversaire :
            test(x+c,y+s)
    if y in [1,6] and empty(x,y+s) and empty(x,y+2*s) : 
        test(x,y+2*s)

def deplacer2s(xp,yp,s1,s2) :
    Cases,end=[],[]
    x,y=xp+s1,yp+s2
    while empty(x,y) :
        Cases+=[(x,y)]
        x,y=x+s1,y+s2
    if identify(x,y)[2]==adversaire :
        Cases+=[(x,y)]
        end=[identify(x,y)[3]]
    return Cases,end
def deplacer2() :
    global Eventual,Cev,xp,yp
    Cases=deplacer2s(xp,yp,1,1)[0]+deplacer2s(xp,yp,1,-1)[0]+deplacer2s(xp,yp,-1,1)[0]+deplacer2s(xp,yp,-1,-1)[0]
    for x,y in Cases :
        test(x,y)
    return deplacer2s(xp,yp,1,1)[1]+deplacer2s(xp,yp,1,-1)[1]+deplacer2s(xp,yp,-1,1)[1]+deplacer2s(xp,yp,-1,-1)[1]
def deplacer3() :
    global Eventual,Cev
    for (x,y) in [(xp+1,yp+2),(xp+1,yp-2),(xp+2,yp+1),(xp+2,yp-1),(xp-1,yp+2),(xp-1,yp-2),(xp-2,yp+1),(xp-2,yp-1)] :
        if 0<=x<8 and 0<=y<8 and identify(x,y)[2]!= joueur :
            test(x,y)

def deplacer4s(xp,yp,s) :
    Cases=[]
    end=[]
    x,y=xp+s,yp
    while empty(x,y) :
        Cases+=[(x,y)]
        x=x+s
    if identify(x,y)[2]==adversaire :
        Cases+=[(x,y)]
        end=[identify(x,y)[3]]
    x,y=xp,yp+s
    while empty(x,y) :
        Cases+=[(x,y)]
        y=y+s
    if identify(x,y)[2]==adversaire :
        Cases+=[(x,y)]
        end+=[identify(x,y)[3]]
    return Cases,end
def deplacer4() :
    global Eventual,Cev,xp,yp
    Cases1,end1=deplacer4s(xp,yp,1)
    Cases2,end2=deplacer4s(xp,yp,-1)
    Cases=Cases1+Cases2
    for x,y in Cases :
        test(x,y)
    return end1+end2

def deplacer5() :
    deplacer2()
    deplacer4()

def deplacer() :
    if m0 in range(2,6) :
        D=eval('deplacer'+str(m0)+'()')
    elif m0 in range (7,10) :
        D=eval('deplacer'+str(m0-5)+'()')
    elif m0==0 :
        deplacer0()
    else :
        deplacer1()

## Fonction echec(x0,y0,patrie) :  ((patrie in [joueur,adversaire))
#) verifie si le le roi de patrie serait en echec dans la case (x0,y0)
def echec_king_other(x0,y0,patrie) :
    global joueur,adversaire
    inverser=False
    by_king=False
    by_pion=False
    if patrie==adversaire :
        joueur,adversaire=adversaire,joueur
        inverser=True
    if patrie=='White' :
        s=-1
    else :
        s=1
    ECHEC=False
    end=deplacer4s(x0,y0,1)[1]+deplacer4s(x0,y0,-1)[1]
    if 5 in end or 4 in end or 9 in end :  #reine/tour
        ECHEC=True
    end=deplacer2s(x0,y0,1,1)[1]+deplacer2s(x0,y0,1,-1)[1]+deplacer2s(x0,y0,-1,1)[1]+deplacer2s(x0,y0,-1,-1)[1]
    if 5 in end or 2 in end or 7 in end:   #reine/fou
        ECHEC=True
    for (x,y) in [(x0+1,y0+2),(x0+1,y0-2),(x0+2,y0+1),(x0+2,y0-1),(x0-1,y0+2),(x0-1,y0-2),(x0-2,y0+1),(x0-2,y0-1)] :  #cavalier
        if identify(x,y)[2]!=patrie and identify(x,y)[3] in [3,8] :
            ECHEC=True
    for c in [-1,1] :  #pion 
        if identify(x0+c,y0+s)[2]!=patrie and (identify(x0+c,y0+s)[3] in [1,6,10,11,12,13,14,15]) :
            by_pion=True
    for (x,y) in [(x0-1,y0-1),(x0-1,y0),(x0-1,y0+1),(x0,y0-1),(x0,y0+1),(x0+1,y0-1),(x0+1,y0),(x0+1,y0+1)] :  #roi
        if identify(x,y)[3]==0 :
            by_king=True
    if inverser :
        joueur,adversaire=adversaire,joueur
    return ECHEC,by_king,by_pion
def echec(x0,y0,patrie) :
    if echec_king_other(x0,y0,patrie)==(False,False,False) :
        return False
    else :
        return True

def matt() :
    x,y=xp,yp
    MATT=False
    print(eventual_king(adversaire))
    if eventual_king(adversaire)[0]==[] :
        if joueur=='White' :
            s=-1
        else :
            s=1
        MATT=True
        print('matt')
        xk,yk=king(adversaire)
        s1,s2=0,0
        if xk!=x :
            s1=abs(xk-xp)//int(xk-x)
        if yk!=y :
            s2=abs(yk-yp)//int(yk-y)
        if echec_king_other(x,y,joueur)[2]==True :
            MATT=False
        x,y=x+s1,y+s2
        while(xk,yk)!=(x,y) and MATT==True:
            print(x,y+s)
            if (identify(x,y+s)[3] in [1,6,10,11,12,13,14,15] and identify(x,y+s)[2]==adversaire) or echec_king_other(x,y,joueur)[0] :
                print('voila')
                MATT=False
            x,y=x+s1,y+s2
    return MATT
        
def pointeur(event) :
    global Eventual,xp,yp,piece,m0,joueur,adversaire,E
    xp,yp=(event.x)//75,(event.y)//75
    if (xp,yp) in Cev :
        move()
        if m0 in [1,6,10,11,12,13,14,15] and yp in [0,7]:
            if adversaire=='White' :
                D=dead2
            else :
                D=dead1
            E=[player.create_image(20,350,anchor=NW,image=txtChoisir)]
            can.unbind("<Button-1>")   
            D.bind("<Button-1>",pick)
        else :
            trace_echec()

        joueur,adversaire=adversaire,joueur
    else :
        blue_erase()
        for e in Coords :
            if (e[0],e[1],e[2])==(xp,yp,joueur) :
                piece=eval(joueur+'['+str(e[3])+']')
                m0=e[3]
                deplacer()
can.bind("<Button-1>",pointeur)    
 
## Positionner pieces de jeu sur fenetre :
White=[can.create_image(75*4,75*7,image=whi0,anchor=NW) , can.create_image(0,75*6,image=whi1,anchor=NW), can.create_image(75*2,75*7,image=whi2,anchor=NW) , can.create_image(75,75*7,image=whi3,anchor=NW)  ,can.create_image(0,75*7,image=whi4,anchor=NW)  ,  can.create_image(75*3,75*7,image=whi5,anchor=NW)  ,  can.create_image(75,75*6,image=whi1,anchor=NW)  ,  can.create_image(75*5,75*7,image=whi2,anchor=NW)  ,  can.create_image(75*6,75*7,image=whi3,anchor=NW)  ,  can.create_image(75*7,75*7,image=whi4,anchor=NW)]

Black=[can.create_image(75*4,0,image=bli0,anchor=NW) , can.create_image(0,75,image=bli1,anchor=NW), can.create_image(75*2,0,image=bli2,anchor=NW) , can.create_image(75,0,image=bli3,anchor=NW)  ,can.create_image(0,0,image=bli4,anchor=NW)  ,  can.create_image(75*3,0,image=bli5,anchor=NW)  ,  can.create_image(75,75,image=bli1,anchor=NW)  ,  can.create_image(75*5,0,image=bli2,anchor=NW)  ,  can.create_image(75*6,0,image=bli3,anchor=NW)  ,  can.create_image(75*7,0,image=bli4,anchor=NW)]

for i in range(10,16) :
    White+=[can.create_image((i-8)*75,75*6,image=whi1,anchor=NW)]
    Black+=[can.create_image((i-8)*75,75,image=bli1,anchor=NW)]
    Coords+=[[i-8,6,'White',i],[i-8,1,'Black',i]]

Coords+=[[0,6,'White',1],[1,6,'White',6],[4,7,'White',0],[3,7,'White',5],[2,7,'White',2],[1,7,'White',3],[0,7,'White',4],[5,7,'White',7],[6,7,'White',8],[7,7,'White',9],[0,1,'Black',1],[1,1,'Black',6],[4,0,'Black',0],[3,0,'Black',5],[2,0,'Black',2],[1,0,'Black',3],[0,0,'Black',4],[5,0,'Black',7],[6,0,'Black',8],[7,0,'Black',9]]

QUIT=Button(fen,text='         QUITTER          ',command=fen.destroy,anchor=W,bg='Cornsilk')
player.create_window(140,650,anchor=NW,window=QUIT)


fen.mainloop()
