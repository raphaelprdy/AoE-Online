
import pygame 
from tkinter import *
from tkinter import ttk
#import PIL
from PIL import ImageTk
#from definitions import *
import main



def fonction_menu_principal() :
    
    fen1=Tk()
    fen1.title("Menu Principal")
    fen1.attributes('-fullscreen')
    fen1.resizable(width=False,height=False)

    swidth = fen1.winfo_screenwidth()
    sheight = fen1.winfo_screenheight()
    
    graphe=Canvas(fen1, width=swidth, height=sheight,bg="gray")

    dezoom = int(1980/swidth )
    
    dezoom2 = int(1114/sheight )
    

    img = PhotoImage(file="resources\imagemenu\BG.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth/2,sheight/2, image=img)

    img2 = PhotoImage(file="resources\imagemenu\mainmenuholder_1.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.18,sheight*.8, image=img2)

    img3 = PhotoImage(file="resources\imagemenu\mainmenuholder_2.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.1795,sheight*.704, image=img3)

    img4 = PhotoImage(file="resources\imagemenu\mainmenuholder_2.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.1795,sheight*.65, image=img4)

    img5 = PhotoImage(file="resources\imagemenu\mainmenuholder_2.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.1795,sheight*.59, image=img5)

    img6 = PhotoImage(file="resources\imagemenu\mainmenuholder_2.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.1795,sheight*.5, image=img6)

    img7 = PhotoImage(file="resources\imagemenu\mainmenuholder_3.gif").subsample(dezoom,dezoom2)
    graphe.create_image(swidth*0.18,sheight*.41, image=img7)

    graphe.pack()

    game=Button(fen1, text='Load SaINve', bg="gray", width=15, height=1, font='arial', command=lambda: fonction_jeu(fen1))
    game.place(x=swidth*0.14, y=sheight*.45)

    newgame=Button(fen1, text='New Game', bg="gray", width=15, height=1, font='arial', command=lambda: Nouvelpartie(fen1,swidth,sheight))
    newgame.place(x=swidth*0.14, y=sheight*.5)

    option=Button(fen1, text='Multiplayer', bg="gray", width=15, height=1, font='arial',command=lambda: Multiplayer(fen1,swidth,sheight) )
    option.place(x=swidth*0.14, y=sheight*.55)

    exit=Button(fen1, text='Quit', bg="gray", width=15, height=1, font='arial', command=lambda: fen1.destroy())
    exit.place(x=swidth*0.14, y=sheight*.6)

    fen1.mainloop()


def Nouvelpartie(fen,w,h):
    
    fen.destroy()
    
    fen2=Tk()
    fen2.title("Setting")
    fen2.attributes('-fullscreen')
    fen2.resizable(width=False,height=False)
  
    graphe2=Canvas(fen2, width=w, height=h,bg="white")

    img2 = PhotoImage(file="resources\imagemenu\parametre.gif").zoom(1,1)
    graphe2.create_image(w/2,h/2, image=img2)

    graphe2.pack()



    #Création menu deroulant Taille map
    
    def Mapsize():
        taille = Taille.get()
        print(MAP_SIZE)
        print(taille)
        if (taille == "Petit"):
            MAP_SIZE=10
        elif(taille == "Moyen"):
            MAP_SIZE=30
        else:
            MAP_SIZE=40


    Taille = StringVar()
    Taille.set("Petit")

    optionmap = [
        "Petit",
        "Moyen",
        "Grand"
    ]
    graphe2.create_text(w*.710,  h*.275,text="Taille de la carte :",font=('Arial',"13"),anchor="n")
    TailleMap=OptionMenu(fen2,Taille,*optionmap)
    TailleMap.place(x=w*.750, y= h*.270)

    #Création menu déroulant du nombre de population    

    def NombreHabitant():
        nombre = Nombrepop.get()
        print(nombre)

    Nombrepop = StringVar()
    Nombrepop.set("200")

    optionpop = [
        "50",
        "100",
        "200"
    ]
    graphe2.create_text(w*.710, h*.325,text="Nombre d'habitant :",font=('Arial',"13"),anchor="n")
    Nombrepopulation=OptionMenu(fen2,Nombrepop,*optionpop)
    Nombrepopulation.place(x=w*.750, y= h*.320)

    #Création menu déroulant du nombre de l'age de départ

    def AgeDepart():
        age = AgeDep.get
        print(age)

    AgeDep = StringVar()
    AgeDep.set("Age de pierre")

    option_age_depart = [
        "Age de pierre",
        "Age de l'outil"
    ]

    graphe2.create_text(w*.710,  h*.375,text="Age de depart :",font=('Arial',"13"),anchor="n")
    AgeDeDepart=OptionMenu(fen2,AgeDep,*option_age_depart)
    AgeDeDepart.place(x=w*.750, y= h*.370)




    graphe2.create_text(540,95,text="Jeu standard ",font=('Arial',"15"),anchor="n")

    game=Button(fen2,text='jouer', bg="burlywood4", width=44, height=1, font='arial',command=lambda:fonction_jeu(fen2))
    game.place(x=w*.605, y=h*.90)

    exit=Button(fen2,text='retour', bg="brown3", width=14, height=1, font='arial',command=lambda:fonction_retour(fen2))
    exit.place(x=w*.490, y=h*.80)

    confirmer=Button(fen2,text='confirmer', bg="burlywood4", width=44, height=1, font='arial',command=lambda:Mapsize())
    confirmer.place(x=w*.605, y=h*.86)
    
    fen2.mainloop()

def Multiplayer(fen,w,h):
    fen.destroy()
    fen3=Tk()
    fen3.title("Setting")
    fen3.attributes('-fullscreen')
    fen3.resizable(width=False,height=False)
  
    graphe3=Canvas(fen3, width=w, height=h,bg="white")
    img = PhotoImage(file="resources\imagemenu\campaign.png").zoom(1,1)
    graphe3.create_image(w/2,h/2, image=img)

    img3 = PhotoImage(file="resources\imagemenu\multipanel.png")
    
    graphe3.create_image(w*0.5,h*.47, image=img3)

    graphe3.pack()
    game=Button(fen3,text='Rejoindre', bg="burlywood4", width=44, height=1, font='arial',)
    game.place(x=w*.39, y=h*.47)

    fen3.mainloop()


def fonction_jeu(fen):
    fen.destroy()
    main.main()

def fonction_retour(fen) :
    fen.destroy()
    fonction_menu_principal()

fonction_menu_principal()