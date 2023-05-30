from secondary_functiuns import *


def modele_rgb(id=0, first_step=0, duration=10, fps=24, folder="example", extension="part1"):
    # 1 ajouter mes parametres specifiques a la fonction dans la signature

    steps = fps*duration
    delta_t = round(duration/steps, 3)
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G','Z-B', 'Yaw-Intensity', 'Duration']

    # ----------------2 mes constantes specifiques-------------------
    r=0
    g=0
    b=0
    intensity=1
    duration=0  #durée du fade, 0 pour hard
    # -------------------------------------------------------------
    # ne pas modifier
    if not os.path.exists('../csv/'+folder):
        os.makedirs('../csv/'+folder)
    file = file_name(foldefolderr=folder, mode='rgb', drone=id,extension=extension)
    with open('../csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')  # empeche la derniere virgule
        for i in range(steps+1):
            # --------3 les variables dependant de step------------------
            # completer sans tenir compte des offsets
            r = 1
            g = 1
            b = 1
            changed = 1  # laisser a zero si aucun changement :
            # l'etape (identique) ne sera ainsi pas creee
            # -------------------------------------------------------------
            # ne pas modifier
            if changed:
                changed = 0
                etape = [first_step+i, id, "Ring", round(r),round(g), round(b),round(intensity,3), duration]
                for i in range(len(etape)-1):
                    file.write(str(etape[i])+',')
                file.write(str(etape[i+1])+'\n')  # empeche la derniere virgule
        print("derniere step : {}".format(first_step+steps))
        return first_step+steps

def rgb_simple(id=0,step=0,folder="example",couleur="r",intensité=1, extension = "part1"):
    header = ['Step','Id','Command','X-R-L', 'Y-G', 'Z-B','Yaw-Intensity', 'Duration']
    
    r=0
    g=0
    b=0

    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='rgb',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')
        match couleur:
            case "r":
                r=255
            case "g":
                g=255
            case "b":
                b=255
            case "w":
                r=255
                g=255
                b=255
        étape=[step,id,"Ring",round(r),round(g), round(b),round(intensité,3), 0]  # c'est sans doute pas problématique si ça empiète sur le fade précédent, mais éviter duration>
        for i in range(len(étape)-1):
            file.write(str(étape[i])+',')
        file.write(str(étape[i+1])+'\n')#empêche la dernière virgule
        

def led_rgb(id=0,first_step=0,duration=10,décalage=0,modulo=24,fps=24,folder="example",extension="part1",couleurs=["r","g","b","w"]):
    steps=fps*duration
    delta_t = round(1/fps,3)
    header = ['Step','Id','Command','X-R-L', 'Y-G', 'Z-B','Yaw-Intensity', 'Duration']
    r=0
    g=0
    b=0
    #------------------------------mes variables spécifiques-------------------------------------
    #compléter

    indic=décalage
    intensity=1
    duration=0  #durée du fade, 0 pour hard
    #---------------------------------------------------------------------------------------------
    #ne pas modifier
    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='rgb',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')
        for i in range(steps+1):
            #------------------------------mes variables dependant de step------------------------
            #compléter
            if i%modulo==0:
                indic+=1
                if 'r' in couleurs[indic%len(couleurs)]:
                    r=255
                    g=0
                    b=0
                elif'g' in couleurs[indic%len(couleurs)]:
                    r=0
                    g=255
                    b=0
                elif 'b' in couleurs[indic%len(couleurs)]:
                    r=0
                    g=0
                    b=255
                elif'w' in couleurs[indic%len(couleurs)]:
                    r=255
                    g=255
                    b=255
                changed=1 #laisser à zéro si aucun changement
            #-------------------------------------------------------------------------------------
            #ne pas modifier
            if changed:
                changed=0
                étape=[first_step+i,id,"Ring",round(r),round(g), round(b),round(intensity,3), duration]  # c'est sans doute pas problématique si ça empiète sur le fade précédent, mais éviter duration>
                for i in range(len(étape)-1):
                    file.write(str(étape[i])+',')
                file.write(str(étape[i+1])+'\n')#empêche la dernière virgule
        print("derniere step : {}".format(first_step+steps))
        return first_step+steps

def rgb_several_drones_sync(nb_drones=3,décalage=0,first_id=0,modulo=24,duration=10,first_step=0,folder="example",extension=""):
    for i in range(nb_drones):
        last_step =led_rgb(id=first_id+i,décalage=décalage,first_step=first_step,duration=duration,modulo=modulo,folder=folder,extension=extension)
    return last_step