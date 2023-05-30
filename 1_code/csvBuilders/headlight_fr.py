from secondary_functiuns import *

def led_frontale(id=0,first_step=1,duration=10,fps=24,folder="example",extension = "part1",modulo=24):
    steps=fps*duration
    delta_t = round(1/fps,3)
    header = ['Step','Id','Command','X-R-L', 'Y-G', 'Z-B','Yaw-Intensity', 'Duration']
    #------------------------------mes constantes spécifiques-------------------------------------
    #compléter
    led=0
    #---------------------------------------------------------------------------------------------
    #ne pas modifier
    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='headlight',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')
        for i in range(steps+1):
            #------------------------------mes variables dependant de step------------------------
            #compléter
            if i%modulo==0:
                led=1-led  # 1 allumé, 0 éteint
                changed=1 #laisser à zéro si aucun changement (à vérifier si c'est inutile d'envoyer plein de fois la même position)
            duration = 0  #durée de l'allumage (inutile si l=0), mettre à 0 pour allumer sans limite de temps
            #-------------------------------------------------------------------------------------
            #ne pas modifier
            if changed:
                changed=0
                étape=[first_step+i,id,"Headlight",led,0,0,0,duration]
                for i in range(len(étape)-1):
                    file.write(str(étape[i])+',')
                file.write(str(étape[i+1])+'\n')#empêche la dernière virgule
        print("derniere step : {}".format(first_step+steps))
        return first_step+steps


def led_frontale_simple(id=0,step=0,etat=1,folder="example",extension = "part1"):
    header = ['Step','Id','Command','X-R-L', 'Y-G', 'Z-B','Yaw-Intensity', 'Duration']

    if not os.path.exists('../2_csv/'+folder):
        os.makedirs('../2_csv/'+folder)
    file=file_name(folder=folder,mode='headlight',drone=id,extension=extension)
    with open('../2_csv/'+folder+'/'+file, 'w') as file:
        for i in range(len(header)-1):
            file.write(str(header[i])+',')
        file.write(str(header[i+1])+'\n')
        
        étape=[step,id,"Headlight",etat,0,0,0,0]
        for i in range(len(étape)-1):
            file.write(str(étape[i])+',')
        file.write(str(étape[i+1])+'\n')