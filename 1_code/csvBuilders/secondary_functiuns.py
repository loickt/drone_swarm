import os

def rm_files(folder,type="csv"):
    if os.path.exists('../2_csv/'+folder) and type=="csv":
        for file in os.listdir('../2_csv/'+folder):
            os.remove('../2_csv/'+folder+"/"+file)
    if os.path.exists('../4_gif/'+folder) and  type=="gif":
            for file in os.listdir('../4_gif/'+folder):
                os.remove('../4_gif/'+folder+"/"+file)

def file_name(folder="example",mode='rgb',drone=4,extension=""):
    return folder+"_"+mode+"_"+extension+'_drone'+str(drone)+'.csv'