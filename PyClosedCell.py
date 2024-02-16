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

# from newContFunctions import *
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
# from Python.openCellZeroDimCt import params
#%% Initial conditions - BurstOpenCell
file = "AUTOClosedCell"
model = load(file) 
# run(
#     model, 
#     IPS=-2, 
#     ICP=['TIME'], 
#     NMX=40000,
# )
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2, 
    ICP=['p', 11], 
    NMX=100,
    DS=1e-2,
    DSMAX=1e-0,
    SP=['LP0'],
    UZSTOP={'p': 1}, 
    UZR={'p': 0.1}
)
diag = relabel(eq + cycle)
save(diag, 'eq')
cl()
#%% Low Ct conditions - BurstOpenCell
file = "AUTOClosedCell"
model = load(file) 
CtVal = 95
# run(
#     model, 
#     IPS=-2, 
#     ICP=['TIME'], 
#     NMX=40000,
# )
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': CtVal}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'p': 1}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['p', 11, 46], 
    NMX=500,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'p': 1}, 
    UZR={'p': 0.1}
)
# cycle = cycle + run(
#     cycle, 
#     SP=['LP2', 'TR0', 'PD0'],
# )
diag = relabel(eq + cycle)
save(diag, 'eq')
cl()

#%% TwoPar Ct-p - ClosedCell
file = "AUTOClosedCell"
model = load(file) 

eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 130}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'p': 2}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['p', 11], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP2', 'TR0', 'PD3'],
    UZSTOP={'p': 1}, 
    UZR={'p': 0.1}
)
twoPar = run(model, NMX=1)
for sol in eq(['LP1','HB1']):
    fwd = run(
        sol, 
        ICP = ['Ct', 'p'], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-0, 
        NMX=6000,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'p': [0, 2], 'Ct': [200, 10]},
    )
    bwd = run(
        sol, 
        ICP = ['Ct', 'p'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-0, 
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'p': [0, 2], 'Ct': [200, 10]},
    )
    twoPar = twoPar + merge(fwd+bwd)
for sol in cycle(['LP1']):
    t = run(
        sol, 
        ICP = ['Ct', 'p'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=6000,
        NTST=2200,
        SP=['LP1', 'UZ', 'BP0'],
        UZSTOP={'p': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-3,)
    bwd = run(t, DS=-1e-3, SP = ['LP0'])
    # bwd = run(
    #     sol, 
    #     ICP = ['Ct', 'Vplc'], 
    #     ISW=2, 
    #     DS = -1e-2, 
    #     NMX=6000,
    #     DSMAX = 1e-0, 
    #     SP=['LP0', 'UZ', 'BP0'],
    #     UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    # )
    twoPar = twoPar + merge(fwd+bwd)

twoPar = relabel(twoPar)
save(twoPar, 'eqT')
cl()
