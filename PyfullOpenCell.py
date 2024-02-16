#%%
"""
This script consists of a single function designed to take out the 
limit cycles for different values of Ct a a given value of Vplc 
Used in conjunction with VplcCycle to generate a hybrid diagram of the open cell
"""
import sys
import os
import numpy as np
from scipy.io import savemat
auto_directory = "/home/huitzil/auto/07p/python" 
sys.path.append(auto_directory)
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
sys.path.append(parentPath)

from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
# from Python.openCellZeroDimCt import params
#%% Initial conditions - fullOpenCell
file = "AUTOfullOpenCell"
model = load(file, constants = file) 
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=1,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 1}
)
save(eq, 'eq')
cl()
#%% 
# region Parameter changes 
modelName = 'AUTOfullOpenCell'
newPar = {
    'Vpm': 3, 
    'Vsoce': 3, 
    'Kpm': 0.2, 
    # 'Ke': 780, 
    'Ts': 15, 
    's1': 0.2,
    'delta': 2,
    'Kt': 0.09
}
startPar = {
    'Vpm': 3, 
    'Vsoce': 3, 
    'Kpm': 0.2, 
    # 'Ke': 780, 
    'Ts': 15, 
    's1': 0.2,
    'delta': 2,
    'Kt': 0.09
}
model = parChange(newPar, modelName, startPar)
# endregion 

#%% Initial conditions - Reparametrized
file = "AUTOfullOpenCell"
model = load(file, constants = file) 
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.49}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': [0.1, 0.08]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqOB')
cl()
#%% TwoPar
# region  
twoPar = run(eq, NMX=1)
parTwo = 'Ke'
parTwoLim = [0.01, 10]
for sol in eq(['HB']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    twoPar = twoPar + merge(fwd+bwd)
# sol = eq('LP3')
# solRun = run(
#         sol, 
#         ICP = ['Ct', 'p'], 
#         ISW=2, 
#         IPS=2,
#         DS = 1e-2,
#         NMX=3000,
#         SP=['LP2', 'UZ'],
#         UZSTOP={'p': [0, 2], 'Ct':[1, 150]},
#     )
# fwd = run(solRun, DS=1e-2)
# bwd = run(solRun, DS=-1e-2)
# twoPar = twoPar + merge(fwd+bwd)
twoPar = relabel(twoPar)
print(twoPar)
save(twoPar, 'eqT')
# endregion
#%% 
# region Branch changes 
m=1.05
l=0.95
newPar = {
    'Vpm': 3, 
    # 'Vsoce': 1.5, 
    'Kpm': 0.45, 
    'Ke': 450, 
    'Ts': 15, 
    # 's1': 0.16,
    # 'Ks': 0.2*l, 
    # 'Kt': 0.11, 
    'Kc': 0.18,
    # 'Vs': 0.2, 
    # 'Kf': 0.2,
    'Kh': 0.09, 
    'Tmax': 10, 
    # 'Ct': 76*l
    'delta': 3,
    # 'gamma': 20
}
startPar = {
    'Vpm': 1.5, 
    'Vsoce': 0.8, 
    'Kpm': 0.4, 
    'Ke': 400, 
    'Ts': 25, 
    's1': 0.2,
    'Ks': 0.19, 
    'Kt': 0.1, 
    'Kc': 0.16,
    'Vs': 2, 
    'Kf': 1.6,
    'Kh': 0.168, 
    'Tmax': 10, 
    'Ct': 76*l,
    'delta': 4,
    'gamma': 5.5
}
eqN = run(
    model, 
    ICP=['p'], 
    NMX=3, 
    DS=3e-2,
)
for key, value in newPar.items():
    if value < startPar[key]: # Decreasing parameter case
        eqN = run(
            eqN, 
            ICP = [key], 
            DS=-1e-4,
            NMX=5000,
            UZSTOP = {key: value}
        )
    elif value > startPar[key]: # Increasing parameter case
        eqN = run(
            eqN, 
            ICP = [key], 
            DS=1e-4,
            NMX=5000,
            UZSTOP = {key: value}
        )
# Re-run diagram 
eqN = run(
    eqN,
    ICP=["p"],
    UZSTOP={'p': [0.995]},
    DS=3e-2,
    DSMAX=1e-2,
    # UZR={'p': [1]},
    # PAR={'Ts': 100}
)
# run(
#     eqN('HB1'), 
#     IPS=2,
#     ICP=["p", 11, 46],
#     DSMAX=1e-1,
#     NMX=20000,
#     NTST=300,
#     UZSTOP={'p': [1.95], 11:[1e+4]},
#     DS=5e-2,
#     SP=['LP1', 'UZ2'],
#     UZR={'p': [1]},
# )
if eqN('HB') != []:
    eqN = eqN + run(
        eqN('HB1'), 
        IPS=2,
        # ISP=3,
        ICP=["p", 11, 46],
        DSMAX=e-1,
        NMX=1000,
        NPR=100,
        NTST=300,
        UZSTOP={'p': [1.95], 11:[1e+4]},
        DS=5e-2,
        SP=['LP0', 'UZ'],
        UZR={'p': [0.532]},
    )
save(eqN, 'eqN')
cl()
# endregion 
#%% TwoPar
# region TwoPar 
twoPar = run(model, NMX=1)
parTwo = 'Ke'
parTwoLim = [10, 20]
sols = eqN(
    [
        'LP1', 
        # 'HB1', 
        # 'LP2', 
        # 'HB2',
        # 'HB3',
     ]
    )
for sol in sols:
    fwd = run(
        sol, 
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = 2e-3,
        NMX=3000,
        SP=['LP0', 'BP0', 'UZ'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = -2e-3, 
        NMX=3000,
        SP=['LP0', 'BP0', 'UZ'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    twoPar = twoPar + merge(fwd+bwd)
# sol = eq('LP3')
# solRun = run(
#         sol, 
#         ICP = ['Ct', 'p'], 
#         ISW=2, 
#         IPS=2,
#         DS = 1e-2,
#         NMX=3000,
#         SP=['LP2', 'UZ'],
#         UZSTOP={'p': [0, 2], 'Ct':[1, 150]},
#     )
# fwd = run(solRun, DS=1e-2)
# bwd = run(solRun, DS=-1e-2)
# twoPar = twoPar + merge(fwd+bwd)
twoPar = relabel(twoPar)
print(twoPar)
save(twoPar, 'eqT')
# endregion
#%%
from itertools import product
n = 3
Kpm = np.linspace(0.1, 0.3, n)
Ke = np.linspace(600, 800, n)
Vsoce = np.linspace(3, 5, n)
Vpm = np.linspace(3, 5, n)
Ts = np.linspace(100, 300, n)
parSpace = [x for x in product(*[Kpm, Ke, Vsoce, Vpm, Ts])]
startPar = {
    'Vpm': 2.2, 
    'Vsoce': 2, 
    'Kpm': 0.1, 
    'Ke': 450, 
    'Ts': 150, 
    's1': 0.0015,
    'Ks': 0.19, 
    'Kt': 0.1, 
    'Kc': 0.16,
    'Vs': 0.10, 
    'Kf': 0.08,
    'Kh': 168, 
    'Tmax': 200, 
    'delta': 1,
    'gamma': 5.5
}
validPar = []
for p in parSpace:
    newPar = {
    'Kpm': p[0], 
    'Ke': p[1], 
    'Vsoce': p[2], 
    'Vpm': p[3], 
    'Ts': p[4], 
}  
    eqN = run(
        model, 
        ICP=['p'], 
        NMX=3, 
        DS=3e-2,
    )
    for key, value in newPar.items():
        if value < startPar[key]: # Decreasing parameter case
            eqN = run(
                eqN, 
                ICP = [key], 
                DS=-1e-4,
                NMX=5000,
                UZSTOP = {key: value}
            )
        elif value > startPar[key]: # Increasing parameter case
            eqN = run(
                eqN, 
                ICP = [key], 
                DS=1e-4,
                NMX=5000,
                UZSTOP = {key: value}
            )
    # Re-run diagram 
    eqN = run(
        eqN,
        ICP=["p"],
        UZSTOP={'p': [3]},
        DS=3e-2,
        # UZR={'p': [1]},
        # PAR={'Ts': 100}
    )
    if eqN('HB') != []:
        validPar.append(p)
        np.savetxt('validPar.txt', validPar, delimiter=',')
    cl()
