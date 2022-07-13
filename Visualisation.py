#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:08:21 2022

@author: clementine
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.special
import sys

#check if we have the correct number of arguments 

if(len(sys.argv)!=2):
    print("Invalid number of arguments")
    exit()

### Razor blade technique

#check the file name
try:
    file=np.genfromtxt(sys.argv[1],delimiter=',',skip_header=1,names=["position",'voltage','gain','offset'])
except FileNotFoundError:
    print("Invalid file name")
    exit()

GainDetectors=[1.51e3,4.75e3,1.5e4,4.75e4,1.51e5,4.75e5,1.5e6,4.75e6]
G=file['gain']/10
G=G.astype(int)
Gain=np.array([GainDetectors[i] for i in G])
#print(file['voltage'])
Power=(file['voltage']-file['offset'])/(0.85*Gain)
Power=Power/np.max(Power)
Position=file['position']*1e-3

def reg_func_measured_power(x,w,x0):
    return 0.5*(1-scipy.special.erf(np.sqrt(2)*(x-x0)/w))

#print(Power)
popt,pcov=scipy.optimize.curve_fit(reg_func_measured_power,Position,Power,[400e-6,0.005])

#for having the good title
name=sys.argv[1]
number=""
for i in name[9:]:
    if i not in ['1','2','3','4','5','6','7','8','8','9','0','-']:
        break
    else:
        number+=i
number=number.replace('-','.')

#array for ploting the fiting function 
Position_theo=np.arange(0, max(Position),0.0001)

plt.plot(Position*1e3,Power,'+',label='Experimental data',color='steelblue')
plt.plot(Position_theo*1e3,reg_func_measured_power(Position_theo,popt[0],popt[1]),label='Fit with w='+f'{popt[0]*10**6:.2f}'+'µm\nand x0='f'{popt[1]*10**3:.2f}'+'mm',color='lightsteelblue')
plt.title('Beam after the ouput of a fiber optic collimator')
plt.legend(loc='lower left')
plt.xlabel('Position of the blade (mm)')
plt.ylabel('Normalised measured power')
plt.savefig('Position_collimator.png')
plt.show()
