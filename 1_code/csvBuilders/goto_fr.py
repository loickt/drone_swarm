from secondary_functiuns import *

import math
import os

def modele_Goto(id=0, first_step=1, duration=10, offset=[0, 0, 1, 0], fps=24, folder="example",extension='part1'):
    # 1 ajouter mes parametres specifiques a la fonction dans la signature

    steps = fps*duration
    delta_t = round(duration/steps, 3)
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G','Z-B', 'Yaw-Intensity', 'Duration']

    # ----------------2 mes constantes specifiques-------------------

    # -------------------------------------------------------------
    # ne pas modifierprint("derniere step : {}".format(first_step+steps))
    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='circle',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')  # empeche la derniere virgule
        for i in range(steps+1):
            # --------3 les variables dependant de step------------------
            # completer sans tenir compte des offsets
            x = 1
            y = 1
            z = 1
            yaw = 1
            changed = 1  # laisser a zero si aucun changement :
            # l'etape (identique) ne sera ainsi pas creee
            # -------------------------------------------------------------
            # ne pas modifier
            if changed:
                changed = 0
                etape = [first_step+i, id, "Goto", round(offset[0] + x, 3), round(
                    offset[1]+y, 3), round(offset[2]+z, 3), round(offset[3]+yaw, 3), delta_t]
                for i in range(len(etape)-1):
                    file.write(str(etape[i])+',')
                file.write(str(etape[i+1])+'\n')  # empeche la derniere virgule




def circle(id=0,first_step=1,duration=10,offset=[0, 0, 1,0],fps=24,folder="example",radius=1, angle_init=0, direction=1, axes=['x','y'],extension=""):
    steps=fps*duration
    delta_t= round(1/fps,3)
    header = ['Step','Id','Command','X-R-L', 'Y-G', 'Z-B','Yaw-Intensity', 'Duration']

    #------------------------------mes constantes spécifiques-------------------------------------
    #compléter
    delta_angle = math.pi*2 / steps
    #---------------------------------------------------------------------------------------------
    #ne pas modifier
    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='circle',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n') #empêche la dernière virgule
        for i in range(steps+1):
            #------------------------------mes variables dependant de step------------------------
            #compléter sans tenir compte des offsets
            sin = round(radius * math.sin(angle_init + (-direction)*delta_angle*i),3)
            cos = round(radius * math.cos(angle_init + (-direction)*delta_angle*i),3)
            if sorted(axes) == ['x', 'y']:
                x=sin
                y=cos
                z=0
                yaw=0
            elif sorted(axes) == ['y', 'z']:
                x=0
                y=cos
                z=sin
                yaw=0
            elif sorted(axes) == ['x', 'z']:
                x=cos
                y=0
                z=sin
                yaw=0
            else:
                print("erreur axes")
                break
            changed=1 #laisser à zéro si aucun changement
            #-------------------------------------------------------------------------------------
            #ne pas modifier
            if changed:
                changed=0
                étape=[first_step+i,id,"Goto",round(offset[0] + x,3),round(offset[1]+y,3), round(offset[2]+z,3),round(offset[3]+yaw,3), delta_t]
                for i in range(len(étape)-1):
                    file.write(str(étape[i])+',')
                file.write(str(étape[i+1])+'\n')#empêche la dernière virgule   
        print("derniere step : {}".format(first_step+steps))
        return first_step+steps

def circles_several_drones(nb_drones=3,first_id=0,duration=10,first_step=1,axes=["y","x"],angle_init=0,radius=0.5,direction=1,folder="example",offset=[0,0,0.5,0],extension=""):
    for i in range(nb_drones):
        last_step =circle(id=first_id+i,first_step=first_step,duration=duration,axes=axes,angle_init=angle_init+i*(math.pi*2/nb_drones),direction=direction,radius=radius,offset=offset,folder=folder,extension=extension)
    return last_step