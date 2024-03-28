#%%
"""
This file contains all the scripts necessary to create fig #1
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
from PyModels import parFullOpenCell, getIVP, getnewICS, fullOpenCell, icsFullOpenCell
matplotlib.rcParams.update(myRcParams())
#%% TwoPar Ct-Vplc - fullOpenCell
"""
Data Two Par - low Ke
"""
# Hopf bifurcations 
file = "AUTOfullOpenCell"
model = load(file) 
parTwo = 'delta'
parTwoLim = [0.0001, 3]
eq = run(
    model, 
    IPS=1, 
    ICP=['Ke'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ke': 400}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.08}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['delta'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-3,
    UZSTOP={parTwo: parTwoLim}
)
twoParE = run(model, NMX=1)
for sol in eq(['HB1', 'HB2']):
    fwd = run(
        sol, 
        ICP = ['Vplc',parTwo], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=6000,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc':[0.01, 1],parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ICP = ['Vplc',parTwo], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-1, 
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc':[0.01, 1], parTwo: parTwoLim},
    )
    twoParE = twoParE + merge(fwd+bwd)
"""
Data - Low delta - low Ke
"""
# file = "AUTOfullOpenCell"
# model = load(file) 
# eq = run(
#     model, 
#     IPS=1, 
#     ICP=['Ke'], 
#     NMX=5000,
#     DS=-1e-2,
#     DSMAX=1e-1,
#     UZSTOP={'Ke': 400}
# )
# eqNe = run(
#     eq, 
#     IPS=1, 
#     ICP=['Vplc'], 
#     NMX=5000,
#     DS=1e-2,
#     DSMAX=1e-2,
#     UZSTOP={'Vplc': 0.3},
#     PAR={'delta': 0.01}
# )
# cycleNe = run(
#     eqNe('HB'), 
#     IPS=2,
#     # ISP=2, 
#     ICP=['Vplc', 11, 'MIN c'], 
#     NMX=5000,
#     NTST=1200,
#     DS=1e-2,
#     DSMAX=1e-2,
#     SP=['LP6', 'TR0', 'PD3', 'BP0'],
#     # UZSTOP={'Vplc': 0.1575}, 
#     UZR={'Vplc': 0.1}
# )
# #%
# """
# Data - Mid delta - low Ke
# """
# file = "AUTOfullOpenCell"
# model = load(file) 

# eqMe = run(
#     eq, 
#     IPS=1, 
#     ICP=['Vplc'], 
#     NMX=5000,
#     DS=1e-2,
#     DSMAX=1e-2,
#     UZSTOP={'Vplc': 0.5},
#     PAR={'delta': 0.62}
# )
# cycleMe = run(
#     eqMe('HB3'), 
#     IPS=2,
#     # ISP=2, 
#     ICP=['Vplc', 11, 'MIN c'], 
#     NMX=5000,
#     NTST=1200,
#     DS=1e-2,
#     DSMAX=1e-1,
#     SP=['LP2', 'TR0', 'PD5', 'BP0', 'UZ3'],
#     # UZSTOP={'Vplc': 0.0874}, 
#     UZR={'Vplc': 0.0874}
# )
# cycleMe2 = run(
#     eqMe('HB2'), 
#     IPS=2,
#     # ISP=2, 
#     ICP=['Vplc', 11, 'MIN c'], 
#     NMX=20000,
#     NTST=1200,
#     DS=1e-2,
#     DSMAX=1e-1,
#     SP=['LP19', 'TR0', 'PD8', 'BP0'],
#     # UZSTOP={'Vplc': 0.1575}, 
#     UZR={'Vplc': 0.1}
# )
# save(eqMe + cycleMe + cycleMe2, 'eq')
# cl()
# #%
# """
# Data - High delta - low Ke
# """
# file = "AUTOfullOpenCell"
# model = load(file) 
# eqHe = run(
#     eq, 
#     IPS=1, 
#     ICP=['Vplc'], 
#     NMX=5000,
#     DS=1e-2,
#     DSMAX=1e-1,
#     UZSTOP={'Vplc': 0.3},
#     PAR={'delta': 2.2}
# )
# cycleHe = run(
#     eqHe('HB'), 
#     IPS=2,
#     # ISP=2, 
#     ICP=['Vplc', 11, 'MIN c'], 
#     NMX=8000,
#     NTST=800,
#     DS=1e-2,
#     DSMAX=1e-0,
#     SP=['LP8', 'TR0', 'PD2', 'BP0', 'UZ2'],
#     # UZSTOP={'Vplc': 0.1575}, 
#     UZR={'Vplc': 0.04}
# )
cl()

#%%
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 1, nrows=1, figure=fig)
fig_width,fig_height = set_figsize(1, (0.7,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
# fig.suptitle('Experimental traces')

"""
Ax settings - Two Par - low Ke
"""
ax = fig.add_subplot(spec[:,0])
# Data extraction
soce = twoParE.data[1]
ipr = twoParE.data[2]
soce = soce[0::1]
ipr = ipr[0::1]

# soce curve 
ax.plot(soce['Vplc'], soce['delta'], 'C2', label = 'CRAC-mediated attractor')
# ipr curve
ax.plot(ipr['Vplc'], ipr['delta'], 'C3', label = 'Narrow spike attractor')

ax.fill_between(
    soce['Vplc'], soce['delta'], 3, 
    alpha = 0.7, color = 'C2'
    )
ax.fill_between(
    ipr['Vplc'], ipr['delta'], 0, 
    alpha = 0.7, color = 'C3'
    )
# Ax limits 
xlim = [0.04, 0.25]
ylim = [0, 2]
ax.set_xticks(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
ax.set_ylabel(r'$\delta$', labelpad=-10)
# ax.set_title('A', loc='left')



# """
# Ax settings Vplc Diag - low Ke - High delta
# """
# ax = fig.add_subplot(spec[0,1])
# # Data extraction
# eqCurve = eqHe.data[0]
# eqCurve = eqCurve[0::1]
# eqStab = eqCurve.stability()
# eqStab.insert(0,0)
# cyCurve = cycleHe.data[0]
# cyCurve = cyCurve[0::1]
# cycleStab = cyCurve.stability()
# cycleStab.insert(0,0)
# #  Equilibrium line 
# for i in range(1,len(eqStab)):
#     if eqStab[i]< 0:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k', 
#             ls='solid', 
#             alpha=1, 
#             # label='EQ points'
#         )
#     else:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k',
#             ls='dashed',
#             alpha=1,
#         )

# #Limit cycle curve 
# for i in range(1,len(cycleStab)):
#     if cycleStab[i]< 0:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C2', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C2', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#     else:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C2',
#             ls='dotted',
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C2',
#             ls='dotted',
#         )
# # HB points 
# for i in [3,4]: #I only care about two particular labels
#     point = eqCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'HB',
#             [point['Vplc'],
#             max(point['c'])*1.1],
#             # 'C2',
#             # marker='o', 
#             # markersize=10,
#         )
# # LP points 
# for i in [14]: #I only care about two particular labels
#     point = cyCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'SNPO',
#             [point['Vplc'],max(point['c']*1)],
#         )
# # PD points
# for i in [13]: #I only care about two particular labels
#     point = cyCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'PD',
#             [point['Vplc'],max(point['c']*1.1)],
#         )
# # Ax limits 
# xlim = [0,0.25]
# ylim = [0, 0.7]
# ax.set_xlim(xlim)
# ax.set_ylim(ylim)
# ax.set_yticks(ylim)
# ax.set_xticks(xlim)
# # ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
# ax.set_ylabel(r'$c$', labelpad=-20)
# ax.set_title('B', loc='left')


# """
# Ax settings Vplc Diag - low Ke - Mid delta
# """
# ax = fig.add_subplot(spec[1,1])
# # Data extraction
# eqCurve = eqMe.data[0]
# eqCurve = eqCurve[0::1]
# eqStab = eqCurve.stability()
# eqStab.insert(0,0)
# cyCurve = cycleMe.data[0]
# cyCurve = cyCurve[0::1]
# cycleStab = cyCurve.stability()
# cycleStab.insert(0,0)
# #  Equilibrium line 
# for i in range(1,len(eqStab)):
#     if eqStab[i]< 0:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k', 
#             ls='solid', 
#             alpha=1, 
#             # label='EQ points'
#         )
#     else:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k',
#             ls='dashed',
#             alpha=1,
#         )


# #Limit cycle curve 
# for i in range(1,len(cycleStab)):
#     if cycleStab[i]< 0:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C3', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C3', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#     else:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C3',
#             ls='dotted',
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C3',
#             ls='dotted',
#         )

# cyCurve = cycleMe2.data[0]
# cyCurve = cyCurve[0::1]
# cycleStab = cyCurve.stability()
# cycleStab.insert(0,0)
# #Limit cycle curve 
# for i in range(1,len(cycleStab)):
#     if cycleStab[i]< 0:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C2', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C2', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#     else:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C2',
#             ls='dotted',
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C2',
#             ls='dotted',
#         )
# # HB points 
# for i in [3,4,5]: #I only care about two particular labels
#     point = eqCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'HB',
#             [point['Vplc'],
#             max(point['c'])*1.1],
#             # 'C2',
#             # marker='o', 
#             # markersize=10,
#         )
# # Ax limits 
# xlim = [0,0.17]
# ylim = [0, 0.3]
# ax.set_xlim(xlim)
# ax.set_ylim(ylim)
# ax.set_yticks(ylim)
# ax.set_xticks(xlim)
# # ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
# ax.set_ylabel(r'$c$', labelpad=-20)
# ax.set_title('C', loc='left')


# """
# Ax settings Vplc Diag - low Ke - low delta
# """
# ax = fig.add_subplot(spec[2,1])
# # Data extraction
# eqCurve = eqNe.data[0]
# eqCurve = eqCurve[0::1]
# eqStab = eqCurve.stability()
# eqStab.insert(0,0)
# cyCurve = cycleNe.data[0]
# cyCurve = cyCurve[0::1]
# cycleStab = cyCurve.stability()
# cycleStab.insert(0,0)
# #  Equilibrium line 
# for i in range(1,len(eqStab)):
#     if eqStab[i]< 0:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k', 
#             ls='solid', 
#             alpha=1, 
#             # label='EQ points'
#         )
#     else:
#         ax.plot(
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
#             eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
#             'k',
#             ls='dashed',
#             alpha=1,
#         )
# #Limit cycle curve 
# for i in range(1,len(cycleStab)):
#     if cycleStab[i]< 0:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C3', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C3', 
#             ls='solid', 
#             # label='Limit cycle'
            
#         )
#     else:
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MAX c'], 
#             'C3',
#             ls='dotted',
#         )
#         ax.plot(
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['Vplc'], 
#             cyCurve[np.abs(cycleStab[i-1]):np.abs(cycleStab[i])]['MIN c'], 
#             'C3',
#             ls='dotted',
#         )
# # HB points 
# for i in [3]: #I only care about two particular labels
#     point = eqCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'HB',
#             [point['Vplc'],
#             max(point['c'])*1.2],
#             # 'C2',
#             # marker='o', 
#             # markersize=10,
#         )
# for i in [4]: #I only care about two particular labels
#     point = eqCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'HB',
#             [point['Vplc'],
#             max(point['c'])*0.7],
#             # 'C2',
#             # marker='o', 
#             # markersize=10,
#         )
# # LP points 
# for i in [6]: #I only care about two particular labels
#     point = cyCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'SNPO',
#             [point['Vplc'],max(point['c']*1.1)],
#         )
# for i in [10]: #I only care about two particular labels
#     point = cyCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'SNPO',
#             [point['Vplc'],max(point['c']*0.9)],
#         )
# # PD points 
# for i in [7,9]: #I only care about two particular labels
#     point = cyCurve.getLabel(i)
#     if point.get('TY') not in ['UZ', 'EP']:
#         ax.annotate(
#             'PD',
#             [point['Vplc'],max(point['c'])],
#         )
# # Ax limits 
# xlim = [0,0.25]
# ylim = [0, 0.4]
# ax.set_xlim(xlim)
# ax.set_ylim(ylim)
# ax.set_yticks(ylim)
# ax.set_xticks(xlim)
# ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
# ax.set_ylabel(r'$c$', labelpad=-20)
# ax.set_title('D', loc='left')


# fig.savefig(latexPath/'Fig12.pdf')
fig.savefig('Figures/Fig12.pdf')

# %%
