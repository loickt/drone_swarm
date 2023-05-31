import pandas as pd
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def concat_files(folder):
    files=os.listdir("../2_csv/"+folder)
    df=pd.read_csv("../2_csv/"+folder+"/"+files[0])
    for i in range(1,len(files)):
        df=pd.concat([df,pd.read_csv("../2_csv/"+folder+"/"+files[i])])
    return df

def sort_csv(df):
    #definition of the sorting order, then order
    df_mapping = pd.DataFrame({'Command': ['Ring', 'Headlight','Takeoff', 'Goto','Land','Wait'],})
    sort_mapping = df_mapping.reset_index().set_index('Command')
    df['Command_priority'] = df['Command'].map(sort_mapping['index'])
    df = df.sort_values(['Step',"Command_priority"],ascending = [True, True])
    df.pop('Command_priority')
    return df

def takeoff_land(df,folder):
    nb_drones=df['Id'].max()+1
    data = {
        'Step': [],
        'Id': [],
        'Command': [],
        'X-R-L': [],
        'Y-G': [],
        'Z-B': [],
        'Yaw-Intensity':[],
        'Duration':[],
    }
    with open("../3_outputCSV/"+folder+"/"+"start_positions.txt", "w") as f: 
        for id in range(nb_drones):
            isolated_drone=df[df["Id"]==id]
            isolated_goto=isolated_drone[isolated_drone["Command"]=='Goto']
            min=isolated_goto['Step'].min()
            max=isolated_goto['Step'].max()
            # print("drone :{}, min :{}, max :{}".format(id,min,max))

            data['Step'].extend([min-1,max+1])
            data['Id'].extend([id,id])
            data['Command'].extend(['Takeof','Land'])
            data['X-R-L'].extend([float(isolated_goto[isolated_goto['Step']==min]['X-R-L'].iloc[0]),float(isolated_goto[isolated_goto['Step']==max]['X-R-L'].iloc[0])])
            data['Y-G'].extend([float(isolated_goto[isolated_goto['Step']==min]['Y-G'].iloc[0]),float(isolated_goto[isolated_goto['Step']==max]['Y-G'].iloc[0])])
            data['Z-B'].extend([float(isolated_goto[isolated_goto['Step']==min]['Z-B'].iloc[0]),0])
            data['Yaw-Intensity'].extend([0,0])
            data['Duration'].extend([2,2])
            
            x=round(float(isolated_goto[isolated_goto['Step']==min]['X-R-L'].iloc[0]),2)
            y=round(float(isolated_goto[isolated_goto['Step']==min]['Y-G'].iloc[0]),2)
            spaces = 10-len("{}".format(x))
            f.write("drone {}     x : {}{}y : {}\n".format(int(isolated_goto[isolated_goto['Step']==min]["Id"].iloc[0]),x,spaces*" ",y))
        f.write("\n")
    dfnew = pd.DataFrame(data)
    return dfnew

def hole_detection(lst):
    missing_numbers = []
    start, end = lst[0], lst[-1]
    for i in range(start, end+1):
        if i not in lst:
            missing_numbers.append(i)
    
    sublists = []
    start_index = 0
    for i in range(len(missing_numbers) - 1):
        if missing_numbers[i+1] != missing_numbers[i] + 1:
            sublists.append(missing_numbers[start_index:i+1])
            start_index = i+1
    sublists.append(missing_numbers[start_index:])
    
    return sublists


def transition(df):
    nb_drones=df['Id'].max()+1

    data = {
        'Step': [],
        'Id': [],
        'Command': [],
        'X-R-L': [],
        'Y-G': [],
        'Z-B': [],
        'Yaw-Intensity':[],
        'Duration':[],
    }

    for id in range(nb_drones):
        isolated_drone=df[df["Id"]==id]
        isolated_goto=isolated_drone[isolated_drone["Command"]=='Goto']
        step=np.sort(isolated_goto["Step"].tolist())
        holes = hole_detection(step)
        
        if len(holes[0])!=0:
            for hole in holes:

                p_e=[[],[]] #outer positions
                p_e[0].append(float(isolated_goto[isolated_goto['Step']==hole[0]-1]['X-R-L'].iloc[0]))
                p_e[0].append(float(isolated_goto[isolated_goto['Step']==hole[0]-1]['Y-G'].iloc[0]))
                p_e[0].append(float(isolated_goto[isolated_goto['Step']==hole[0]-1]['Z-B'].iloc[0]))
                p_e[0].append(float(isolated_goto[isolated_goto['Step']==hole[0]-1]['Yaw-Intensity'].iloc[0]))
                p_e[1].append(float(isolated_goto[isolated_goto['Step']==hole[-1]+1]['X-R-L'].iloc[0]))
                p_e[1].append(float(isolated_goto[isolated_goto['Step']==hole[-1]+1]['Y-G'].iloc[0]))
                p_e[1].append(float(isolated_goto[isolated_goto['Step']==hole[-1]+1]['Z-B'].iloc[0]))
                p_e[1].append(float(isolated_goto[isolated_goto['Step']==hole[-1]+1]['Yaw-Intensity'].iloc[0]))

                data['Step'].extend(hole)
                data['Id'].extend([id for step in hole])
                data['Command'].extend(['Goto' for step in hole])
                
                data['X-R-L'].extend([float(round(p_e[0][0]+itere*(p_e[1][0]-p_e[0][0])/(len(hole)+1),3)) for itere in range(1,len(hole)+1)])
                data['Y-G'].extend([float(round(p_e[0][1]+itere*(p_e[1][1]-p_e[0][1])/(len(hole)+1),3)) for itere in range(1,len(hole)+1)])
                data['Z-B'].extend([float(round(p_e[0][2]+itere*(p_e[1][2]-p_e[0][2])/(len(hole)+1),3)) for itere in range(1,len(hole)+1)])
                data['Yaw-Intensity'].extend([float(round(p_e[0][3]+itere*(p_e[1][3]-p_e[0][3])/(len(hole)+1),3)) for itere in range(1,len(hole)+1)])
                data['Duration'].extend([round(1/24,3) for itere in range(1, len(hole)+1)])
        dfnew = pd.DataFrame(data)   
    return dfnew

def distance_calculation(df,mode="w",folder="example"): 
    nb_drones = df['Id'].max()+1
    isolated_goto = df[df["Command"] == 'Goto']
    max_step = isolated_goto['Step'].max()

    with open("../3_outputCSV/"+folder+'/'+"dist.csv", mode) as file:
        if mode=="w":
            header = []
            header.extend(["Step", "Min"])
            for i in range(5):  #row
                for j in range(i):  # column
                    header.append(str(j)+"-"+str(i))
            for i in range(len(header)-1):
                file.write(str(header[i])+',')
            file.write(str(header[i+1])+'\n')  # prevents the last comma

        steps = np.sort(isolated_goto["Step"].tolist())
        # important because subgroups may not be in order
        for step in np.unique(steps):
            row = [step,0]
            isolated_step = isolated_goto[isolated_goto["Step"] == step]
            for i in range(nb_drones):  # row
                for j in range(i):  # column
                    dist = math.sqrt(
                        (float(isolated_step[isolated_step['Id'] == i]['X-R-L'].iloc[0]) -
                         float(isolated_step[isolated_step['Id'] == j]['X-R-L'].iloc[0]))**2 +
                        (float(isolated_step[isolated_step['Id'] == i]['Y-G'].iloc[0]) -
                         float(isolated_step[isolated_step['Id'] == j]['Y-G'].iloc[0]))**2 +
                        (float(isolated_step[isolated_step['Id'] == i]['Z-B'].iloc[0]) -
                         float(isolated_step[isolated_step['Id'] == j]['Z-B'].iloc[0]))**2)
                    # follows the header's order
                    row.append(round(dist, 3))
            row[1]=np.min(row[2:])
            for i in range(len(row)-1):
                file.write(str(row[i])+',')
            file.write(str(row[i+1])+'\n')  # prevents the last comma
    
    df=pd.read_csv("../3_outputCSV/"+folder+"/dist.csv")
    return df['Min'].min()-0.13 # diagonal size of the drone

# def plot_dist_min(folder): in progress
#     df=pd.read_csv("../3_outputCSV/"+folder+"/dist.csv")
#     fig, ax = plt.subplots()
#     ax.set_title('Minimum distances between drones')
#     ax.set_ylim(0, 1.5)
#     ax.set_ylabel('minimal distance between all drones(m)')
#     ax.set_xlabel('Step')
#     x=df['Step'].tolist()
#     ax.plot(df['Step'].tolist(),df['Min'].tolist())
#     ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
#     ax.grid(True)

# def plot_dist_all(folder):  #in progress
#     df=pd.read_csv("../3_outputCSV/"+folder+"/dist.csv")
#     nb_drones=df['Id'].max()+1
#     s=0
#     for i in range(1,nb_drones+1):
#         s+=i
#     print(s)

#     fig, ax = plt.subplots()
#     ax.set_title('Minimum distances between drones')
#     ax.set_ylim(0, 1.5)
#     ax.set_ylabel('minimal distance between all drones(m)')
#     ax.set_xlabel('Step')
#     x=df['Step'].tolist()
#     ax.plot(df['Step'].tolist(),df['Min'].tolist())
#     ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
#     ax.grid(True)

def prepare_csv(folder):
    if not os.path.exists("../3_outputCSV/"+folder):
        os.makedirs("../3_outputCSV/"+folder)
    df_concat=concat_files(folder)
    nb_drones=df_concat['Id'].max()+1
    print("nbdrone="+str(nb_drones))
    if nb_drones>1:
        print("Distances on first generated CSVs >= "+str(int(float(distance_calculation(df=df_concat,mode='w',folder=folder))*100))+"cm")
    df_adds=takeoff_land(df_concat,folder=folder)
    df_interpolated_adds = transition(df_concat)
    if nb_drones>1 and df_interpolated_adds.shape[0]>0:        
        print("Distances on transition interpolated CSVs >= "+str(int(float(distance_calculation(df=df_interpolated_adds,mode='w',folder=folder))*100))+"cm")
    df_concat_1=pd.concat([df_adds,df_concat])
    df_concat_2=df_concat_1
    df_concat_2=pd.concat([df_concat_1,df_interpolated_adds])
    df_final=sort_csv(df_concat_2)
    
    df_final.to_csv("../3_outputCSV/"+folder+"/"+folder+".csv",index=False)