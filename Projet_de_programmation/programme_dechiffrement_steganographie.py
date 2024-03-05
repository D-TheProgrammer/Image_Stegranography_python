from PIL import Image, ImageDraw
import os # pour avoir l'extension de l'image


def dechiffrement_steganographie(chemin_img_chiff):
    #Limage chiffré est de base en png
    #chemin_img_chiff = "resultat.png"
    chemin_img_chiff = chemin_img_chiff

    image_chiff = Image.open(chemin_img_chiff)

    #On conversion en RGBA pour faciliter le traitement
    image_chiff = image_chiff.convert('RGBA') #on le passe sous la forme RGBAlpha 

    #On reccupere les info sur les largeurs et Hauteurs de chaque image
    larg_img_chiff, haut_img_chiff = image_chiff.size

    print("Largeur chiff", larg_img_chiff)
    print("hauteur chiff", haut_img_chiff)


    #On dechiffre uniquement les images qui ont été chiffré
    chiffrement_realiser= image_chiff.getpixel((larg_img_chiff - 1, haut_img_chiff - 1))[2]

    if chiffrement_realiser == 100 :


        def reccup_larg_haut (pixel):
            milliers, centaines, dizaines, unites = pixel
            somme = milliers * 1000 + centaines *100 + dizaines*10 +unites
            return somme

        # Largeur et Hauteur de l'image dechiffrer 
        larg_img_dechiff = reccup_larg_haut (image_chiff.getpixel((0, 0)))
        haut_img_dechiff = reccup_larg_haut (image_chiff.getpixel((0, 1)))

        print("Largeur de limage a Retrouver", larg_img_dechiff)
        print("Hauteur de limage a Retrouver", haut_img_dechiff)

        #On reccupere caché dans le dernier pixel de limage 
        #lextension et le Nombre de Bit caché par pixel dans limage chiffre

        nb_bit_cache= image_chiff.getpixel((larg_img_chiff - 1, haut_img_chiff - 1))[0]
        print("bit cacher",nb_bit_cache)
        nb_ext_dechiff= image_chiff.getpixel((larg_img_chiff -1 , haut_img_chiff - 1))[1]
        print("nombre de lextention",nb_ext_dechiff)



        # Creation de la nouvelle image temporaire avec les mauvaise dimension
        img_dechiffrer = Image.new("RGBA", (larg_img_dechiff, haut_img_dechiff))




        #Fusion des bits du pixel de limage 1 avec les bit de limage2
        #On conservera les 5 bits de poids fort de limage 1 et les 3 bit de poids faible de limage2
        def compo_bit_pix_dechif(nb_bit_cache , pix_img1_bin_chiff):
            # Transformation en binaire des pixel
            pix_img1_bin_chiff = bin(pix_img1_bin_chiff)[2:]
            
            # Ajout de zero pour avoir une taille de 8 bits
            pix_img1_bin = pix_img1_bin_chiff.zfill(8)
            
            #Il va falloir reccuperé les derniers bit de poids faible en fonction du nombre de bit caché
            bit_a_supp= 8-nb_bit_cache
            
            # Nombre binaire resultat du nb_bit_img1 de l'image 1 choisi et des nb_bit_img2 de l'image 2 choisi
            pix_img_bin_res = pix_img1_bin[-nb_bit_cache:] + '0' * (8 - nb_bit_cache)
            #print(pix_img_bin_res)

            #passage de bin à entier
            pix_img_entier_res = int(pix_img_bin_res, 2)

            return pix_img_entier_res

        # POUR TESTER LES VALEUR DECHIFFRE 
        # print("---------------")
        # pixel_chiff = image_chiff.getpixel((790, 140))
        # rou_pix_chiff, ver_pix_chiff, ble_pix_chiff, alpha_pix_chiff = pixel_chiff
        # print("rouge chiffrer",rou_pix_chiff )
        # rou_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache ,rou_pix_chiff )
        # print("rouge dechiffrer",rou_pix_dechiff )

        # print("VERT chiffrer",ver_pix_chiff )
        # ver_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache ,ver_pix_chiff )
        # print("vert dechiffrer",ver_pix_dechiff )

        # print("BLEU chiffrer",ble_pix_chiff )
        # ble_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache ,ble_pix_chiff )
        # print("bleu dechiffrer",ble_pix_dechiff )

        # print("ALPHA chiffrer",alpha_pix_chiff )
        # alpha_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache ,alpha_pix_chiff )
        # print("ALPHA dechiffrer",alpha_pix_dechiff )



        def dechiffrement_bit (larg_img_chiff, haut_img_chiff ) :
            for x in range(larg_img_chiff):
                for y in range(haut_img_chiff):
                    #----- Separation en 3 couleurs + 1 alpha de chaque alpha de l'image1  ------------
                    pixel_chiff = image_chiff.getpixel((x, y))
                
                    # #on verifie le mode avec la chaine de caractere resultat de  .mode
                    
                    mode_pixel_recep = image_chiff.mode

                    if mode_pixel_recep == 'RGBA':
                        rou_pix_chiff, ver_pix_chiff, ble_pix_chiff, alpha_pix_chiff = pixel_chiff
                    else:
                        rou_pix_chiff, ver_pix_chiff, ble_pix_chiff ,alpha_pix_chiff = 255
            
                    #--------- Fusion des nuance des pixel  ----------------
                    rou_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache ,rou_pix_chiff )
                    ver_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache, ver_pix_chiff )
                    ble_pix_dechiff =compo_bit_pix_dechif(nb_bit_cache, ble_pix_chiff )
                    #alpha_pix_dechiff = alpha_pix_chiff # car dans le chiffrement on avait deja laisser la couche alpha de limage cacher
                    alpha_pix_dechiff = compo_bit_pix_dechif(nb_bit_cache, alpha_pix_chiff )

                    ensemble_couleur = (rou_pix_dechiff , ver_pix_dechiff , ble_pix_dechiff , alpha_pix_dechiff) 
                    
                    # on place la couleur
                    #toile_img.point((x, y), fill=ensemble_couleur)
                    image_chiff.putpixel((x, y), ensemble_couleur)

            #Car On a stocker une information sur le dernier pixel
            #Donc si on est sur le dernier pixel on replace l'avant dernier
            pixel_dechiff = image_chiff.getpixel((larg_img_chiff - 2, haut_img_chiff - 2))
            image_chiff.putpixel((larg_img_chiff - 1, haut_img_chiff - 1), pixel_dechiff)
            
            return image_chiff


        # Appel de la fonction steganographie pour chiffer limage
        image_chiff = dechiffrement_bit(larg_img_chiff , haut_img_chiff ) 



        #A laide de l'information qui était stocker on resize a la bonne taille
        img_dechiffrer= image_chiff.resize((larg_img_dechiff, haut_img_dechiff))
        

        #on reatribuer la bonne extension en fonction du nombre cacher
        extension_fichier_dechiff=""
        if nb_ext_dechiff < 100:
            extension_fichier_dechiff = ".png"
        elif nb_ext_dechiff < 200:
            extension_fichier_dechiff = ".jpg"
            img_dechiffrer = img_dechiffrer.convert('RGB')
        else:
            extension_fichier_dechiff = ".jpeg"
            img_dechiffrer = img_dechiffrer.convert('RGB')


        # Enregistrez l'image sous un nom de fichier
        nom_fichier_dechiff = "res_dechiff" + extension_fichier_dechiff
        img_dechiffrer.save(nom_fichier_dechiff)

        # Afficher l'image (facultatif)
        #img_dechiffrer.show()


    #si aucun chiffrement n'a pas été réalisé on save l'image d'origine A savoir la Chiffré
    else :
        nom_fichier_dechiff = "res_dechiff.png"
        image_chiff.save(nom_fichier_dechiff)

    #on return le nom du fichier pour pourvoir afficher le fichier avec la bonne extension sur le tkinter
    return nom_fichier_dechiff