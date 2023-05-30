import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import os
import matplotlib.animation

import pandas as pd

def csv2gif(file="",suffixe="",axes="changing",label=1):
    
    df=pd.read_csv("../3_outputCSV/"+file+"/"+file+".csv")
    nb_steps=df["Step"].unique()

    nb_drones=df['Id'].max()+1
    text=["label" for x in range(int(nb_drones))]
    graph=["graph" for x in range(int(nb_drones))]
    headlight=[None for x in range(int(nb_drones))]

    def update_graph(num):
        if num%50==0 or num==nb_steps[-1]:
            print("Creating the gif - image {} of {}".format(int(num),int(nb_steps[-1])))
        if axes=="changing":
            ax.view_init(22.5+22.5*num/nb_steps.max(), 22.5+45*num/nb_steps.max())
        title.set_text('Simu Crazyflie, time={}s'.format(num//24))
        data=df[df['Step']==num]
        data_ring=data[data['Command']=='Ring']
        data_head=data[data['Command']=='Headlight']
        data_goto=data[data['Command']=='Goto']
        data_land=data[data['Command']=='Land']
        for index, row in data_ring.iterrows():
            graph[int(row['Id'])].set_color([int(row['X-R-L'])/255,int(row["Y-G"])/255,int(row["Z-B"])/255])
            graph[int(row['Id'])].set_edgecolor(headlight[int(row['Id'])])
        for index, row in data_head.iterrows():
            headlight[int(row['Id'])]=[None,'yellow'][int(row['X-R-L'])]
            graph[int(row['Id'])].set_edgecolor(headlight[int(row['Id'])])
        for index, row in data_goto.iterrows():
            graph[int(row['Id'])]._offsets3d = ((float(row["X-R-L"]),),(float(row["Y-G"]),),(float(row["Z-B"]),))
            if label:
                xt, yt, _ = proj3d.proj_transform(float(row["X-R-L"]), float(row["Y-G"]), float(row["Z-B"]), ax.get_proj())
                text[int(row['Id'])].set_position((xt+0.002,yt+0.002))
        for index, row in data_land.iterrows():
            graph[int(row['Id'])]._offsets3d = ((float(row["X-R-L"]),),(float(row["Y-G"]),),(0,))
            if label:
                xt, yt, _ = proj3d.proj_transform(float(row["X-R-L"]), float(row["Y-G"]), 0, ax.get_proj())
                text[int(row['Id'])].set_position((xt+0.002,yt+0.002))


    fig = plt.figure(figsize=((10,10)))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(0,4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    if axes == "corner":
        ax.view_init(45, 45) # vertical x y
    elif sorted(axes) == ['x', 'y']:
        ax.view_init(90, 90) # vertical x y 
    elif sorted(axes) == ['x', 'z']:
        ax.view_init(0, 90) # side x,z
    elif sorted(axes) == ['y', 'z']:
        ax.view_init(0, 0) # side y z
    elif axes == "changing":
        ax.view_init(22.5,22.5)

    data_takeof=df[df['Command']=='Takeof']
    
    for index, row in data_takeof.iterrows():
        x=float(row["X-R-L"])
        y=float(row["Y-G"])
        z=0
        #texts
        if label:
            xt, yt, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
            text[int(row['Id'])]=ax.text2D(xt+0.002, yt+0.002, '{}'.format(row['Id']),size=10)
            text[int(row['Id'])].set_position((xt,yt))
        #points
        graph[int(row['Id'])]=ax.scatter((x,),(y,),(z,),s=100, linewidth=2)
        graph[int(row['Id'])].set_color('k')

    data_step0=df[df['Step']==0]
    data_Ring0=data_step0[data_step0['Command']=="Ring"]
    for index, row in data_Ring0.iterrows():
        graph[int(row['Id'])].set_color([int(row['X-R-L'])/255,int(row["Y-G"])/255,int(row["Z-B"])/255])
    data_Headligt0=data_step0[data_step0['Command']=="Headlight"]
    for index, row in data_Headligt0.iterrows():
        headlight[int(row['Id'])]=[None,'yellow'][int(row['X-R-L'])]
        graph[int(row['Id'])].set_edgecolor(headlight[int(row['Id'])])

    title = ax.set_title('Simu Crazyflie',size=20)        
    ani = matplotlib.animation.FuncAnimation(fig, update_graph, nb_steps,interval=40, blit=False)
    if not os.path.exists('../4_gif/'+file):
        os.makedirs('../4_gif/'+file)
    if len(axes)==2:
        axes="{}{}".format(axes[0],axes[1])
    ani.save("../4_gif/"+file+"/"+file+"_axes_"+str(axes)+suffixe+".gif",fps=24)
    print("To open the gif :\neog ../4_gif/"+file+"/*")