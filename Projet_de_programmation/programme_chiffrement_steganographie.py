from PIL import Image, ImageDraw
import os # pour avoir l'extension de l'image

def steganographie(nb_bit_img1,nb_bit_img2,chemin_img_recev,chemin_img_env):
    #On charge l'image

    #pour tester 
    # chemin_img_recev = "./loutre.jpg" #A nous de choisir attention aux extension
    # chemin_img_env = "./kangooroo.jpeg" 

    chemin_img_recev = chemin_img_recev #A nous de choisir attention aux extension
    chemin_img_env = chemin_img_env

    image_recep = Image.open(chemin_img_recev)
    image_env = Image.open(chemin_img_env)

    #On conversion en RGBA pour faciliter le traitement
    image_recep = image_recep.convert('RGBA') #on le passe sous la forme RGBAlpha 
    image_env = image_env.convert('RGBA')

    #On reccupere les info sur les largeurs et Hauteurs de chaque image
    larg_image_recep, hauteur_image_recep = image_recep.size
    larg_image_env, hauteur_image_env = image_env.size

    # On redimensionne image_env pour qu'elle ait la meme dimension que l'image qui recoit
    image_env = image_env.resize((larg_image_recep, hauteur_image_recep))

    #restitution des nb_bit
    nb_bit_img1=nb_bit_img1
    nb_bit_img2=nb_bit_img2
    

    #Fusion des bits du pixel de limage 1 avec les bit de limage2
    #On conservera par exemple les 5 bits de poids fort de limage 1 et les 3 bit de poids faible de limage2
    def compo_bit_pix(nb_bit_img1, nb_bit_img2 , pix_img1, pix_img2):

        # Transformation en binaire des pixel
        pix_img1_bin = bin(pix_img1)[2:]
        pix_img2_bin = bin(pix_img2)[2:]

        # Ajout de zero pour avoir une taille de 8 bits
        pix_img1_bin = pix_img1_bin.zfill(8)
        pix_img2_bin = pix_img2_bin.zfill(8)

        #si nb_bit_img2 est différent de 0
        if nb_bit_img2 != 0:
            # Nombre binaire resultat du nb_bit_img1 de l'image 1 choisi et des nb_bit_img2 de l'image 2 choisi
            pix_img_bin_res = pix_img1_bin[:nb_bit_img1] + pix_img2_bin[:nb_bit_img2]

        else:
            pix_img_bin_res = pix_img1_bin

        #passage de bin à entier
        pix_img_entier_res = int(pix_img_bin_res, 2)

        return pix_img_entier_res    


    def modif_img_stegano (larg_image_recep, hauteur_image_recep ) :
        for x in range(larg_image_recep):
            for y in range(hauteur_image_recep):
                #----- Separation en 3 couleurs + 1 alpha de chaque alpha de l'image1  ------------
                pixel_recep = image_recep.getpixel((x, y))
            
                #on verifie le mode avec la chaine de caractere resultat de  .mode
                mode_pixel_recep = image_recep.mode

                if mode_pixel_recep == 'RGBA':
                    rou_pix_rec, ver_pix_rec, ble_pix_rec, alpha_pix_rec = pixel_recep
                else:
                    rou_pix_rec, ver_pix_rec, ble_pix_rec ,alpha_pix_rec = 255
                    

                #----- Separation en 3 couleurs + 1 alpha de chaque alpha de l'image2  ------------
                pixel_env = image_env.getpixel((x, y))
            
                #on verifie le mode avec la chaine de caractere resultat de  .mode
                mode_pixel_env = image_env.mode

                if mode_pixel_env == 'RGBA':
                    rou_pix_env, ver_pix_env, ble_pix_env, alpha_pix_env = pixel_env
                else:
                    rou_pix_env, ver_pix_env, ble_pix_env ,alpha_pix_env = 255 , 255 , 255 , 255


                #--------- Fusion des nuance des pixel  ----------------
                rou_pix_fusion =compo_bit_pix(nb_bit_img1, nb_bit_img2 ,rou_pix_rec, rou_pix_env)
                ver_pix_fusion =compo_bit_pix(nb_bit_img1, nb_bit_img2 ,ver_pix_rec, ver_pix_env)
                ble_pix_fusion =compo_bit_pix(nb_bit_img1, nb_bit_img2 ,ble_pix_rec, ble_pix_env)
                alpha_pix_fusion = compo_bit_pix(nb_bit_img1, nb_bit_img2 ,alpha_pix_rec, alpha_pix_env) #ici jai choisi que limage caché aurait plus dimportance et donc on conserve son alpha

                ensemble_couleur = (rou_pix_fusion , ver_pix_fusion , ble_pix_fusion , alpha_pix_fusion) 

                # on place la couleur
                image_recep.putpixel((x, y), (ensemble_couleur) )
        return image_recep

    # Appel de la fonction modif_img_stegano pour chiffer limage
    image_recep=modif_img_stegano(larg_image_recep, hauteur_image_recep)

    # Ensemble de division pour reccuperer chaque chiffre  
    # des milliers , centaines etc...
    def decomposer_nombre_uniDizCenMil(nombre):
        milliers = nombre // 1000
        centaines = (nombre // 100) % 10
        dizaines = (nombre // 10) % 10
        unites = nombre % 10
        print((milliers, centaines, dizaines, unites))
        return (milliers, centaines, dizaines, unites)

    info_larg_env = decomposer_nombre_uniDizCenMil(larg_image_env)
    info_haut_env = decomposer_nombre_uniDizCenMil(hauteur_image_env)

    #On stock donc la largeur et hauteur original de l'image d'envoie
    #Pour cela on stock par couche de couleur les milliers , centaine , dizaine , unites
    image_recep.putpixel((0, 0), info_larg_env)
    image_recep.putpixel((0, 1), info_haut_env)

    #On stock egalement le niveau de "cachoterie" cela permettra de reccuperer l'image plus tard
    #Egalement l'extension afin de recreer l'image au plus près
    extension_fichier_env = os.path.splitext(chemin_img_env)[1]
    if extension_fichier_env == ".png" :
        nb_ext_env = 0
    elif extension_fichier_env == ".jpg" :
        nb_ext_env = 100
    elif extension_fichier_env == ".jpeg" :
        nb_ext_env = 200
    
    #on met 100 pour dire que la steganographie pour eviter de décod
    steganographie_faite=100

    image_recep.putpixel((larg_image_recep -1, hauteur_image_recep-1), (nb_bit_img2, nb_ext_env , steganographie_faite, 200) )


    #image_recep.show()

    # Pour sauvegarder l'image
    image_recep.save('resultat.png', 'png')
