#%% Libraries
"""
This file contains all the scripts necessary to create fig #2
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pathlib as pth
import pandas as pd
auto_directory = "/home/huitzil/auto/07p/python" #Update with your own AUTO directory
sys.path.append(auto_directory)
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
# sys.path.append(parentPath)
# latexPath = Path(os.getcwd()).parent/'Latex'
# from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS
matplotlib.rcParams.update(myRcParams())
#%% Data Collection 
"""
Data Vplc Diag - Narrow Spike
"""
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 140
eqN = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': CtVal}
)
eqN = run(
    eqN, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycleN = run(
    eqN('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11, 'MIN c'], 
    NMX=5000,
    NTST=1200,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP2', 'TR0', 'PD2', 'BP0'],
    # UZSTOP={'Vplc': 0.1575}, 
    UZR={'Vplc': 0.1}
)
"""
Data Vplc Diag - Wide Spike
"""
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 75
eqB = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': CtVal}
)
eqB = run(
    eqB, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycleB = run(
    eqB('HB2'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11, 'MIN c'], 
    NMX=1200,
    DS=1e-2,
    NTST=1000,
    DSMAX=1e-1,
    SP=['LP6', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
# cycleB1 = cycleB + run(
#     cycleB('PD1'), 
#     ISW=-1,
#     SP=['LP6', 'TR0', 'PD3'],
#     )
"""
Data Vplc Diag - Wide Spike w/Plateau
"""
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 95
eqBR = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': CtVal}
)
eqBR = run(
    eqBR, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycleBR = run(
    eqBR('HB2'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11, 'MIN c'], 
    NMX=1200,
    DS=1e-2,
    NTST=1000,
    DSMAX=1e-1,
    SP=['LP3', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
cl()
#%%
"""
Data Simulation - Narrow Spike
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, talpha, tf = [0, 10, 40]
par['Vplc']=0.1
par['Ct']=140
dataN = getIVP(model, par, ics, tini=tini, tf=200)
ics = getnewICS(dataN)
dataN = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Wide Spike w/ Plateau - 95
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, talpha, tf = [0, 10, 120]
par['Vplc']=0.195
par['Ct']=95
dataBr = getIVP(model, par, ics, tini=tini, tf=200)
ics = getnewICS(dataBr)
dataBr = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Narrow Spike - 95
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, talpha, tf = [0, 10, 40]
par['Vplc']=0.09
par['Ct']=95
dataN95 = getIVP(model, par, ics, tini=tini, tf=200)
ics = getnewICS(dataN95)
dataN95 = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Wide Spike - 75
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, talpha, tf = [0, 10, 40]
par['Vplc']=0.1
par['Ct']=75
dataB = getIVP(model, par, ics, tini=tini, tf=200)
ics = getnewICS(dataB)
dataB = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Narrow Spike - 75
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, talpha, tf = [0, 10, 40]
par['Vplc']=0.06
par['Ct']=75
dataN75 = getIVP(model, par, ics, tini=tini, tf=200)
ics = getnewICS(dataN75)
dataN75 = getIVP(model, par, ics, tini=tini, tf=tf)
#%% Figure creation
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=6, figure=fig)
fig_width,fig_height = set_figsize(1, (2,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
"""
Ax settings Vplc Diag - Ct 140
"""
ax = fig.add_subplot(spec[0:2,0])
# Data extraction
eqCurve = eqN.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleN.data[0]
cyCurve = cyCurve[0::2]
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
# Limit cycle curve
ax.plot(cyCurve['Vplc'], cyCurve['MAX c'], 'C3')
ax.plot(cyCurve['Vplc'], cyCurve['MIN c'], 'C3')
# HB points 
for i in [3,4]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB'+str(i-2),
            [point['Vplc'],
            max(point['c'])*0.85],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )

# Ax limits 
xlim = [0,0.2]
ylim = [0.05, 0.25]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks([0, 0.1, 0.2])
# ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('A \t' + r'($C_t = 140$)', loc='left')


"""
Ax settings Vplc Diag - Ct 95
"""
ax = fig.add_subplot(spec[2:4,0])
# Data extraction
eqCurve = eqBR.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleBR.data[0]
cyCurve = cyCurve[0::1]
cycleStab = cyCurve.stability()
cycleStab.insert(0,0)
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
#Limit cycle curve 
for i in range(1,len(cycleStab)):
    if cycleStab[i]< 0:
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
            'C3', 
            ls='solid', 
            # label='Limit cycle'
            
        )
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
            'C3', 
            ls='solid', 
            # label='Limit cycle'
            
        )
    else:
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
            'C3',
            ls='dotted',
        )
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
            'C3',
            ls='dotted',
        )
# HB points 
for i in [3,4]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB'+str(i-2),
            [point['Vplc']+0.01,max(point['c']*0.8)],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
# LP points 
j=2
for i in [6,10]: #I only care about two particular labels
    point = cyCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'SNPO'+str(j),
            [point['Vplc']+0.01,max(point['c'])*0.95],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
        j=j-1
# PD points 
j=2
for i in [7,8]: #I only care about two particular labels
    point = cyCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'PD'+str(j),
            [point['Vplc']+0.01,max(point['c'])],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
        j=j-1
# Ax limits 
xlim = [0,0.3]
ylim = [0, 0.4]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks([0, 0.1, 0.2, 0.3])
# ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=0)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('C \t'+ r'($C_t = 95$)', loc='left')

"""
Ax settings Vplc Diag - Ct 75
"""
ax = fig.add_subplot(spec[4:6,0])
# Data extraction
eqCurve = eqB.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleB.data[0]
cyCurve = cyCurve[0::1]
cycleStab = cyCurve.stability()
cycleStab.insert(0,0)
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
# Limit cycle curve
for i in range(1,len(cycleStab)):
    if cycleStab[i]< 0:
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
            'C3', 
            ls='solid', 
            # label='Limit cycle'
        )
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
            'C3', 
            ls='solid', 
            # label='Limit cycle'
        )
    else:
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
            'C3',
            ls='dotted',
        )
        ax.plot(
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
            cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
            'C3',
            ls='dotted',
        )
# HB points 
for i in [3,4]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB'+str(i-2),
            [point['Vplc']+0.01,max(point['c']*0.8)],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
# LP points 
j=2
for i in [6,10]: #I only care about two particular labels
    point = cyCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'SNPO'+str(j),
            [point['Vplc']+0.01,max(point['c']*0.9)],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
        j=j-1
# PD points 
j=2
for i in [7,9]: #I only care about two particular labels
    point = cyCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'PD'+str(j),
            [point['Vplc']+0.01,max(point['c'])],
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize = 4
        )
        j=j-1
# Ax limits 
xlim = [0,0.3]
ylim = [0, 0.4]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks([0, 0.1, 0.2, 0.3])
ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=0)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('E \t'+ r'($C_t = 75$)', loc='left')


"""
Ax settings Simulation - Narrow Spike - Ct 140
"""
ax = fig.add_subplot(spec[0:2,1])
ax.plot(dataN[0], dataN[1], color = 'red', label = r'$c$')
ax2 = ax.twinx()
ax2.plot(dataN[0], dataN[3], color = 'red', ls = 'dashed', label = r'$p$')
# Ax limits 
xlim = [0,20]
ylim = [0, 0.3]
y2lim = [0, 0.3]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
# ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$p$', labelpad=-10)
ax.set_title('B', loc='left')
ax.legend(loc='lower left')
ax2.legend(loc='lower right')
"""
Ax settings Simulation - Narrow Spike - Ct 95
"""
ax = fig.add_subplot(spec[2,1])
ax.plot(dataN95[0], dataN95[1], color = 'red')
ax2 = ax.twinx()
ax2.plot(dataN95[0], dataN95[3], color = 'red', ls = 'dashed')
# Ax limits 
xlim = [0,40]
ylim = [0, 0.3]
y2lim = [0, 0.5]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
# ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$p$', labelpad=-10)
ax.set_title('D', loc='left')

"""
Ax settings Simulation - Wide Spike w/Plateau - Ct 95
"""
ax = fig.add_subplot(spec[3,1])
ax.plot(dataBr[0], dataBr[1], color = 'salmon')
ax2 = ax.twinx()
ax2.plot(dataBr[0], dataBr[3], color = 'salmon', ls = 'dashed')
# Ax limits 
xlim = [0,120]
ylim = [0, 0.4]
y2lim = [0, 0.6]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
# ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$p$', labelpad=-10)
# ax.set_title('F)', loc='left')

"""
Ax settings Simulation - Narrow Spike - Ct 75
"""
ax = fig.add_subplot(spec[4,1])
ax.plot(dataN75[0], dataN75[1], color = 'red')
ax2 = ax.twinx()
ax2.plot(dataN75[0], dataN75[3], color = 'red', ls = 'dashed')
# Ax limits 
xlim = [0,40]
ylim = [0, 0.3]
y2lim = [0, 0.6]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
# ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$p$', labelpad=-10)
ax.set_title('F', loc='left')

"""
Ax settings Simulation - Wide Spike - Ct 75
"""
ax = fig.add_subplot(spec[5,1])
ax.plot(dataB[0], dataB[1], color = 'orangered')
ax2 = ax.twinx()
ax2.plot(dataB[0], dataB[3], color = 'orangered', ls = 'dashed')
# Ax limits 
xlim = [0,40]
ylim = [0, 0.4]
y2lim = [0, 0.6]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
ax.set_xlabel(r'Time (seconds)', labelpad=-3)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$p$', labelpad=-10)
# ax.set_title('G)', loc='left')

# fig.savefig(latexPath/'Fig8.pdf')
fig.savefig('Figures/Fig8.pdf')
# %%
