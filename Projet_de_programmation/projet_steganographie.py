#______________________________________________________________________
#_______PROJET INTRODUCTION A LA SECURITE , STEGANOGRAPHIE ____________
#_____________________ PROJET FAIT EN PYTHON   ________________________
#______________________________________________________________________

#Tout le projet est accompagné par de commentaires 
#afin de rendre le code plus compréhensible

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os # pour avoir l'extension de l'image
import programme_chiffrement_steganographie
import programme_dechiffrement_steganographie


#On cache le menu home et on fait apparaitre les bouton du menu_steganographie
def menu_steganographie():
    label_home.place_forget()
    bout_suivant_home.place_forget()

    #On supprime tous les boutons de la page Dechiffrement
    label_dechiff_stegano.place_forget()
    bout_page_chiffrer.place_forget()
    btn_dechiff_steganographie.place_forget()
    btn_charger_img3.place_forget()
    img_label_stegano4.place_forget()

    #On affiche les boutons correspondant a la page
    label_page_stegano.place(x=0, y=0)
    bout_quitter.place(x=685, y=1)
    bout_page_déchiffrer.place(x=560, y=4)
    

    btn_charger_img1.place(x=20, y=446)
    btn_charger_img2.place(x=142,  y=446)
    btn_reinit_img.place(x=263, y=446)
    btn_prepa_stegano.place(x=570, y=446)
    

def menu_dechiff_steganographie():
    #on n'affiche plus tous les boutons de la page de Chiffrement
    label_page_stegano.place_forget()
    btn_charger_img1.place_forget()
    btn_charger_img2.place_forget()
    btn_prepa_stegano.place_forget()
    bout_page_déchiffrer.place_forget()
    
    txt_bit_cache.place_forget()
    entry_bit_cache.place_forget()
    btn_steganographie.place_forget()
    reinit_toutes_img(0)

    #On affiche les boutons correspondant a la page
    label_dechiff_stegano.place(x=0, y=0)
    bout_page_chiffrer.place(x=570, y=4)
    btn_dechiff_steganographie.place(x=100,  y=446)
    btn_charger_img3.place(x=590, y=446)



def fermer(): #pour fermer avec message ou la croix 
    fenetre.quit()


#cReattion de la fenetre et de sa taille 
fenetre = tk.Tk()
fenetre.title("Projet Stéganographie")
fenetre.configure(bg="#ffffff")
fenetre.geometry("800x500") 
fenetre.resizable(False, False)


#On place Le menu d'accueil du programme
image_background_home = Image.open("fond_home_steganographie.png")
image_tk_home = ImageTk.PhotoImage(image_background_home)
label_home = tk.Label(fenetre, image=image_tk_home)
label_home.place(x=0, y=0)


bout_suivant_home = tk.Button(fenetre, text="Suivant",  font=("Arial", 16), height=1, width=13, borderwidth=0, highlightthickness=0, relief="groove", bg= "#E2E2E2", fg="black", activeforeground="green", command=menu_steganographie)
bout_suivant_home.place(x=320, y=380)

#---------------------PAGE STEGANOGRAPHIE------------------------
#le nouveau Fond 
image_bg_page_stegano = Image.open("fond_steganographie.png")
image_tk_page_stegano = ImageTk.PhotoImage(image_bg_page_stegano)
label_page_stegano = tk.Label(fenetre, image=image_tk_page_stegano)

#Bouton permettant de changer de page
bout_page_déchiffrer = tk.Button(fenetre, text="Déchiffrer", font=("Arial", 15), height=2, borderwidth=0, highlightthickness=0, bg="#3B7CBF",fg="#E2E2E2", relief='groove',activebackground="#3B7CBF" , activeforeground="green",command=menu_dechiff_steganographie)


#Labels permettant d'afficher les images choisis 
img_label_stegano1 = tk.Label(fenetre) #image1 a qui recoit limage
img_label_stegano2 = tk.Label(fenetre) #image2 a qui sera cacher 
img_label_stegano3 = tk.Label(fenetre) #pour choisir une image chiffré
img_label_stegano4 = tk.Label(fenetre) #resultat de limage dechiffré

#Liste pour stocker les chemins des deux images
global chemins_images 
chemins_images = ["", "", "" , ""]

# Fonction pour charger, stocker un chemin d'image  et afficher l'image qui en découle
def charger_afficher_image(indice, choisi_ou_pas):
    #on reccupere le chemin de l'image
    #Soit le chemin est imposé soit on choisi
    if choisi_ou_pas == "chiffrer":
        fichier_image= "./resultat.png"

    elif choisi_ou_pas == "dechiff" :
        if chemins_images[2] != "" : #Si le chemin de limage chiffré est differente de "rien"
            fichier_image= programme_dechiffrement_steganographie.dechiffrement_steganographie(chemins_images[2])

    else:
        fichier_image = filedialog.askopenfilename()

    if (fichier_image and (0 <= indice < 2)):
        chemins_images[indice] = fichier_image  #Ajout du chemin en fonction de l'image
        nouvelle_taille_img=(241, 134) #pour le resize
    else:
        chemins_images[indice] = fichier_image  #Ajout du chemin en fonction de l'image
        nouvelle_taille_img=(294, 166) #pour le resize

    if 0 <= indice < 4:
        fichier_image = chemins_images[indice]
        
        if fichier_image:
            image = Image.open(fichier_image)
            image = image.resize(nouvelle_taille_img)
            image_tk = ImageTk.PhotoImage(image)

            if indice == 0: #en fonction de l'image qui sera chiffré ou cacher on affiche le label
                img_label_stegano1.place(x=70, y=78)  
                img_label_stegano1.config(image=image_tk)
                img_label_stegano1.image = image_tk
            elif indice == 1 :
                img_label_stegano2.place(x=70, y=290)
                img_label_stegano2.config(image=image_tk)
                img_label_stegano2.image = image_tk
            elif indice == 2  :
                img_label_stegano3.place(x=477, y=163)
                img_label_stegano3.config(image=image_tk)
                img_label_stegano3.image = image_tk
            else :
                img_label_stegano4.place(x=24, y=163)
                img_label_stegano4.config(image=image_tk)
                img_label_stegano4.image = image_tk
     



#Bouton qui charge et affiche la première image
btn_charger_img1 = tk.Button(fenetre, text="Choisir Image Qui\nReçoit Une Autre", height=3, borderwidth=0, highlightthickness=0, bg="#232947",fg="#E2E2E2", relief='groove',activebackground="#232947" , activeforeground="#ECD113",command=lambda: charger_afficher_image(0,"oui"))

# Bouton qui charge et affiche la seconde image
btn_charger_img2 = tk.Button(fenetre, text="Choisir Image\nA Cacher", height=3, width=13,borderwidth=0, highlightthickness=0, bg="#232947",fg="#E2E2E2", relief='groove',activebackground="#232947" , activeforeground="#ECD113",command=lambda: charger_afficher_image(1,"oui"))


#Variable permettant de choisir le niveau de dissimulation allant de 0 a 8
# 0 : Il reste que l'image 1 
# 8 : Il ne reste que l'image 2 donc elle est pas caché 
#On va donc initialiser avec un niveau 3 (niveau correspondant au nb_bit_img2)

global nb_bit_img1, nb_bit_img2
nb_bit_img1 = 5
nb_bit_img2 = 3

txt_bit_cache = tk.Label(fenetre,text="Degré de Dissimulation (3 est recommandé):",bg="#B7330E",width=35, height=1)
entry_bit_cache = tk.Entry(fenetre,width=3,bg="#B7330E", border=0, font=("Arial", 12))

#fonction pour placer le label prevenant l'utilisateur quil doit choisir le niveau de dissimulation et placant les bon bouton
def preparer_steganographie():
    txt_bit_cache.place(x=475, y=345)
    entry_bit_cache.place(x=723, y=345)

    btn_prepa_stegano.place_forget()
    btn_steganographie.place(x=570, y=438)

btn_prepa_stegano = tk.Button(fenetre, text="Preparation de la Steganographie",height=3, borderwidth=0, highlightthickness=0, bg="#294664",fg="#E2E2E2", relief='groove',activebackground="#294664" , activeforeground="#ECD113",command=preparer_steganographie)



#fonction permmetant le choix du niv de dissimulation
def choix_nb_bit_a_cacher():
    global nb_bit_img1, nb_bit_img2  

    nb_bit_img2 = entry_bit_cache.get()
    
    #Transformation en nombre du texte
    nb_bit_img2 = int(nb_bit_img2)
    
    #On Vérifie que la valeur est entre 0 et 8
    nb_bit_img2 = max(0, min(8, nb_bit_img2))
    nb_bit_img1 = 8 - nb_bit_img2


#Pour ne plus afficher les images a lecran et reinitialiser la liste d'images
def reinit_toutes_img(extra): 
    print(chemins_images)
    chemins_images[0]="" #On reinitialise les chemins
    chemins_images[1]="" 

    #Remet les labels a zero , extra permet de supprimer certaines images en fonction des cas 
    img_label_stegano1.place_forget()
    img_label_stegano2.place_forget()
    if extra == 1 :  
        chemins_images[2]=""  
        img_label_stegano3.place_forget()
    #label_resultat_steg.place_forget()

    
#Bouton qui lance la reinitialisation
btn_reinit_img = tk.Button(fenetre, text="Réinitialisation\nDes Images", width=13, height=3, borderwidth=0, highlightthickness=0, bg="#232947",fg="#E2E2E2", relief='groove',activebackground="#232947" , activeforeground="#ECD113", command=lambda:reinit_toutes_img(1))


#Fonction demarrant la steganographie
def declencher_steagnographie():
    if (chemins_images[0] != "" and chemins_images[1] != "") : #si il y a bien 2 images pour la steganographie on effectue le reste
        #On remplace le bouton de preparation avec le bouton pour lancer la steganographie
        txt_bit_cache.place_forget()
        entry_bit_cache.place_forget()

        btn_prepa_stegano.place(x=570, y=446)
        btn_steganographie.place_forget()

        #On reccupere le nombre de bit
        choix_nb_bit_a_cacher()

        #On utilise la fonction qui englobe l'ensemble du programme de stagnographie
        programme_chiffrement_steganographie.steganographie(nb_bit_img1, nb_bit_img2 , chemins_images[0],chemins_images[1])

        #Et on reinitialise les images
        reinit_toutes_img(0)
        # Planifiez l'appel à la fonction après 10 secondes (10000 millisecondes)
        #resultat_stegano("resultat.png")  
        
        charger_afficher_image(2,"chiffrer")


btn_steganographie = tk.Button(fenetre, text="Lancer\nla steganographie",font=("Arial", 14),height=2, borderwidth=0, highlightthickness=0, bg="#294664",fg="red", relief='groove',activebackground="#294664" , activeforeground="#ECD113" ,command=declencher_steagnographie)

#Bouton pour quitter la page en fin de page
bout_quitter = tk.Button(fenetre, text="QUITTER", font=("Arial", 17), height=2, borderwidth=0, highlightthickness=0, bg="#C1272D",fg="#E2E2E2", relief='groove',activebackground="#C1272D" , activeforeground="blue",command=fermer)



#--------------------- PAGE DECHIFFREMENT ------------------------
#Bouton permettant de changer de page
bout_page_chiffrer = tk.Button(fenetre, text="Chiffrer", font=("Arial", 15), height=2, borderwidth=0, highlightthickness=0, bg="#3B7CBF",fg="#E2E2E2", relief='groove',activebackground="#3B7CBF" , activeforeground="green",command=menu_steganographie)


img_bg_dechiff_stegano = Image.open("fond_dechiff_steganographie.png")
image_tk_dechiff_stegano = ImageTk.PhotoImage(img_bg_dechiff_stegano)
label_dechiff_stegano = tk.Label(fenetre, image=image_tk_dechiff_stegano)
label_dechiff_stegano.lower()#pour placer ce fond au dernier plan



#Fonction demarrant le dechiffrement de la steganographie
def declencher_dechiff_stegano():
    if (chemins_images[2] != "" ) : #si il Manque l'image chiffré
        #On utilise la fonction qui englobe l'ensemble du programme de stagnographie
        programme_dechiffrement_steganographie.dechiffrement_steganographie(chemins_images[2])

        #Et on reinitialise les images
        reinit_toutes_img(0)

        charger_afficher_image(3,"dechiff")

btn_dechiff_steganographie = tk.Button(fenetre, text="Lancer\nDéchiffrment",font=("Arial", 14),height=2, borderwidth=0, highlightthickness=0, bg="#232947",fg="red", relief='groove',activebackground="#232947" , activeforeground="#ECD113" ,command=declencher_dechiff_stegano)


# Bouton qui charge et affiche la seconde image
btn_charger_img3 = tk.Button(fenetre, text="Choisir Image\nA Dechiffrer", height=3, width=13,borderwidth=0, highlightthickness=0, bg="#294664",fg="#E2E2E2", relief='groove',activebackground="#294664" , activeforeground="#ECD113",command=lambda: charger_afficher_image(2,"oui"))

#On ferrme en appuyant sur la croix
fenetre.protocol("WM_DELETE_WINDOW", fermer)

fenetre.mainloop()

