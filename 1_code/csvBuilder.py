#!/usr/bin/env python

"""csvBuilder.py: This code creates a csv file modeling a drone warm flight"""

__author__      = "Loïck Toupin"

import os
import sys

parent = os.getcwd().split("/")[-1]
if parent != "1_code":
	print("Put your terminal in the folder 1_code")
	exit()
        

sys.path.insert(0, 'csvBuilders')
from csvBuilders.secondary_functiuns import *
from csvBuilders.goto import *
from csvBuilders.rgb import *
from csvBuilders.headlight import *
sys.path.insert(0, 'csv_processing')
from csv_processing.csv2gif import *
from csv_processing.csvAssembler import *

folder="circles_8_drones_rgb"

frequency=24
empty_csv = 1
empty_gif = 1

if empty_csv:
    rm_files(folder,type="csv")
if empty_gif:
    rm_files(folder,type="gif")
    
    

circles_several_drones(nb_drones=4,duration=10,first_step=1,axes=["y","x"],angle_init=0,radius=1.5, direction=1,folder=folder,offset=[0,0,1.5,0],extension="part1")
circles_several_drones(nb_drones=4,first_id=4,duration=10,first_step=1,axes=["z","y"],angle_init=0,radius=1.5,direction=1, folder=folder,offset=[0,1.5,1.5,0],extension="part2")


rgb_several_drones_sync(nb_drones=4,duration=10,first_step=0,folder=folder,extension="part1")
rgb_several_drones_sync(nb_drones=4,first_id=4,offset=1,duration=10,first_step=0,folder=folder,extension="part2")


prepare_csv(folder=folder)
csv2gif(file=folder,label=0,axes="changing")
# csv2gif(file=folder,label=1,axes=['x', 'y'])
# csv2gif(file=folder,label=1,axes=['x', 'z'])
# csv2gif(file=folder,label=1,axes=['y', 'z'])
# csv2gif(file=folder,label=1,axes="corner")
