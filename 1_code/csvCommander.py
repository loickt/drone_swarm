#!/usr/bin/env python

"""csvCommander.py: This code controls the drone swarm based on the chosen csv file"""

__author__      = "Loïck Toupin"

# This code is based on the library developed by crazyflie
# Find more details here : https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/swarm/synchronizedSequence.py


import threading
import time
from collections import namedtuple
from queue import Queue

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

import csv
import pandas as pd
import os

parent = os.getcwd().split("/")[-1]
if parent != "1_code":
	print("Put your terminal in the folder 1_code")
	exit()

#------------------------------------VARIABLES----------------------------------------------

file="circles_2_drones_led"
uris = [
    #'radio://0/80/2M/E7E7E7E7E1',
    #  'radio://0/80/2M/E7E7E7E7E2',
    #  'radio://0/80/2M/E7E7E7E7E3',
    #  'radio://0/80/2M/E7E7E7E7E4',
     'radio://0/80/2M/E7E7E7E7E5',
     'radio://0/80/2M/E7E7E7E7E6',
    # 'radio://0/80/2M/E7E7E7E7E7',
]

#------------------------------------------------------------------------------------------

Takeoff = namedtuple('Takeoff', ['height', 'time'])
Land = namedtuple('Land', ['time'])
Goto = namedtuple('Goto', ['x', 'y', 'z','yaw', 'time'])
# RGB [0-255], Intensity [0.0-1.0]
Ring = namedtuple('Ring', ['r', 'g', 'b', 'intensity', 'time'])
Header = namedtuple('Header', ['val','time'])
# Reserved for the control loop, do not use in sequence
Quit = namedtuple('Quit', [])
STEP_TIME=0.042

sequence=[]
df=pd.read_csv("../3_outputCSV/"+file+"/"+file+".csv")
nb_steps=df["Step"].unique()
nb_drones=df['Id'].max()+1

for num in nb_steps:
    data=df[df['Step']==num]
    data_takeof=data[data['Command']=='Takeof']
    data_ring=data[data['Command']=='Ring']
    data_head=data[data['Command']=='Headlight']
    data_goto=data[data['Command']=='Goto']
    data_land=data[data['Command']=='Land']
    for index, row in data_takeof.iterrows():
        sequence.append((num,row['Id'],Takeoff(row['Z-B'],row["Duration"])))
    for index, row in data_land.iterrows():
        sequence.append((num,row['Id'],Land(row["Duration"])))
    for index, row in data_ring.iterrows():
        sequence.append((num,row['Id'],Ring(int(row['X-R-L']),int(row["Y-G"]),int(row["Z-B"]),int(row["Yaw-Intensity"]),row["Duration"])))
    for index, row in data_head.iterrows():
        sequence.append((num,row['Id'],Header(int(row['X-R-L']),row['Duration'])))
    for index, row in data_goto.iterrows():
        sequence.append((num,row['Id'],Goto(row['X-R-L'],row["Y-G"],row["Z-B"],row["Yaw-Intensity"],row["Duration"])))

#---------------------------------------


def activate_high_level_commander(scf):
    scf.cf.param.set_value('commander.enHighLevel', '1')


def activate_mellinger_controller(scf, use_mellinger):
    controller = 1
    if use_mellinger:
        controller = 2
    scf.cf.param.set_value('stabilizer.controller', str(controller))


def set_ring_color(cf, r, g, b, intensity, time):
    cf.param.set_value('ring.fadeTime', str(time))

    r *= intensity
    g *= intensity
    b *= intensity

    color = (int(r) << 16) | (int(g) << 8) | int (b)
    print(color)
    cf.param.set_value('ring.fadeColor', str(color))

def set_front_led(cf,val):
    cf.param.set_value("ring.headlightEnable", str(val))


def crazyflie_control(scf):
    cf = scf.cf
    control = controlQueues[uris.index(cf.link_uri)]

    activate_mellinger_controller(scf, False)

    commander = scf.cf.high_level_commander

    # Set fade to color effect and reset to Led-ring OFF
    set_ring_color(cf, 0, 0, 0, 0, 0)
    cf.param.set_value('ring.effect', '14')

    while True:
        command = control.get()
        if type(command) is Quit:
            return
        elif type(command) is Takeoff:
            commander.takeoff(command.height, command.time)
        elif type(command) is Land:
            commander.land(0.0, command.time)
        elif type(command) is Goto:
            commander.go_to(command.x, command.y, command.z, command.yaw, command.time)
        elif type(command) is Ring:
            set_ring_color(cf, command.r, command.g, command.b,
                           command.intensity, command.time)
            pass
        elif type(command) is Header:
            set_front_led(cf, command.val)
            pass
        else:
            print('Warning! unknown command {} for uri {}'.format(command,
                                                                  cf.uri))


def control_thread():
    pointer = 0
    step = 0
    stop = False

    
    while not stop:
        maxduration=0
        print('Step {}:'.format(step))
        while sequence[pointer][0] <= step:
            cf_id = sequence[pointer][1]
            command = sequence[pointer][2]
            if command.time>maxduration:
                maxduration=command.time
            print(' - Running: {} on {}'.format(command, cf_id))
            controlQueues[cf_id].put(command)
            pointer += 1

            if pointer >= len(sequence):
                print('Reaching the end of the sequence, stopping!')
                stop = True
                break

        step += 1
        time.sleep(maxduration)

    for ctrl in controlQueues:
        ctrl.put(Quit())


if __name__ == '__main__':
    controlQueues = [Queue() for _ in range(len(uris))]

    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    if nb_drones==len(uris):
        with Swarm(uris, factory=factory) as swarm:
            swarm.parallel_safe(activate_high_level_commander)
            swarm.reset_estimators()

            print('Starting sequence!')

            threading.Thread(target=control_thread).start()

            swarm.parallel_safe(crazyflie_control)

            time.sleep(1)
    else :
        print("{} drone{} in the flight, but {} URIs given".format(nb_drones,"s"*(nb_drones%2-1),len(uris),"s"*(len(uris)%2-1),"s"*(len(uris)%2-1)))
