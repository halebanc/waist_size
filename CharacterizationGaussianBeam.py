# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:08:21 2022

@author: clementine
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.special
import os

def number_from_title(name):
    number=""
    for i in name[9:]:
        if i not in ['1','2','3','4','5','6','7','8','8','9','0','-']:
            break
        else:
            number+=i
    return float(number.replace('-','.'))

### Razor blade technique
def reg_func_measured_power(x,w,x0):
    return 0.5*(1-scipy.special.erf(np.sqrt(2)*(x-x0)/w))

wave_lenght=1.55*(10**-6)
def reg_func_measured_spot_size(z, w0, d0):
    return w0*np.sqrt(1+( (wave_lenght*(z-d0) / (np.pi*w0**2) )**2))

def cacul_popt(file_name):
    file=np.genfromtxt(file_name,delimiter=',',skip_header=1,names=["position",'voltage','gain','offset'])
    GainDetectors=[1.51e3,4.75e3,1.5e4,4.75e4,1.51e5,4.75e5,1.5e6,4.75e6]
    G=file['gain']/10
    G=G.astype(int)
    Gain=np.array([GainDetectors[i] for i in G])
    Power=(file['voltage']-file['offset'])/(0.85*Gain)
    Power=Power/np.max(Power)
    Position=file['position']*1e-3
    popt,pcov=scipy.optimize.curve_fit(reg_func_measured_power,Position,Power,[400e-6,0.005])
    return popt



#array with all the file name

#tab_name=["position_0cm.csv", "position_1-3cm.csv", "position_2-5cm.csv", "position_3-9cm.csv","position_10-7cm.csv", "position_15-5_new_cm.csv"]
tab_name=[i for i in os.listdir() if (i[-4:]==".csv" and i[:9]=='position_')]

#array with all the positions
tab_z=[]
for i in tab_name:
    tab_z.append(number_from_title(i))

#sort the two arrays by position 
tab_name=[x for _,x in sorted(zip(tab_z, tab_name))]
tab_z=[i*(10**-2) for i in sorted(tab_z)]
print(tab_name)
print(tab_z)
tab_popt=[]
for i in tab_name:
    tab_popt.append(cacul_popt(i)[0])



print(tab_popt)

tab_z_theo=np.arange(0, max(tab_z), 0.001)
popt_z,pcov_z=scipy.optimize.curve_fit(reg_func_measured_spot_size,tab_z,tab_popt,maxfev=10000000)
plt.plot([i*10**2 for i in tab_z], [i*(10**6) for i in tab_popt], '+',color="steelblue")
#plt.errorbar([i*10**2 for i in tab_z], [i*(10**6) for i in tab_popt], xerr=0.5, ecolor="red", label='both limits (default)')
plt.plot([i*10**2 for i in tab_z_theo], [i*(10**6) for i in reg_func_measured_spot_size(tab_z_theo, popt_z[0], popt_z[1])], color="red",label='Fit with w0='+f'{popt_z[0]*10**6:.2f}'+'µm\nand d0='f'{popt_z[1]*10**3:.2f}'+'mm')
plt.legend(loc='upper left')
plt.xlabel("position en cm")
plt.ylabel("spot size en µm")
plt.savefig("CharacterizationGaussianBeam.png")
plt.show()
