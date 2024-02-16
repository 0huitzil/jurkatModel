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
file = "AUTOOpenCell"
model = load(file, constants = file) 
#%% 
# region Parameter changes 
modelName = 'AUTOOpenCell'
newPar = {
    'Vpm': 3, 
    'Vsoce': 3, 
    'Kpm': 0.2, 
    # 'Ke': 800, 
    'Ts': 15, 
    's1': 0.2,
    'delta': 2,
    'Tmax': 15, 
    'Kh': 0.12, 
    'Kt': 0.12,
    # 'Kc': 0.2
}
startPar = {
    'Vpm': 20, 
    'Vsoce': 40, 
    'Kpm': 0.2, 
    'Ke': 800, 
    'Ts': 20, 
    's1': 0.12,
    'delta': 1,
    'Tmax': 10, 
    'Kh': 0.168, 
    'Kt': 0.095,
    'Kc': 0.16
}
model = parChange(newPar, modelName, startPar)
# endregion 

#%% Initial conditions - Reparametrized
# region
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=5e-1,
    DSMAX=1e-0,
    UZSTOP={'p': 0.49}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['p', 11], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'p': 1}, 
    UZR={'p': [0.1, 0.08]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion

#%% Initial conditions - s1
# region
parTwo = 's1'
parTwoLim = [0.01, 1]
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 0.3}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['s1'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [0.1, 0.3,0.5,0.8]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion
#%% TwoPar - s1
# region  
twoPar = run(eq, NMX=1)
parTwo = 's1'
parTwoLim = [0.01, 1]
for sol in eq(['HB1']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
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

#%% Initial conditions - Ke
# region
parTwo = 'Ke'
parTwoLim = [1100, 1]
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 0.3}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e+1,
    UZSTOP={parTwo: parTwoLim}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=8000,
    DS=1e-2,
    DSMAX=1e+0,
    UZSTOP={parTwo: parTwoLim}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11], 
    NMX=3000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e+1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [750, 700, 650]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion
#%% TwoPar - Ke
# region  
twoPar = run(eq, NMX=1)
parTwo = 'Ke'
parTwoLim = [0.01, 10]
for sol in eq(['LP1','HB' ]):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
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
#%% Initial conditions - Ts
# region
parTwo = 'Ts'
parTwoLim = [250, 1]
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 0.3}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e+1,
    UZSTOP={parTwo: parTwoLim}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=8000,
    DS=1e-2,
    DSMAX=1e+0,
    UZSTOP={parTwo: parTwoLim}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11], 
    NMX=3000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e+1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [5,10,15,20,100]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion
#%% TwoPar - Ts
# region  
twoPar = run(eq, NMX=1)
parTwo = 'Ts'
parTwoLim = [0.01, 400]
for sol in eq(['HB1']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ', 'GH1'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ', 'GH2'],
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

#%% Initial conditions - delta
# region
parTwo = 'delta'
parTwoLim = [0.001, 3]
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 0.2}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=8000,
    DS=1e-3,
    DSMAX=5e-3,
    UZSTOP={parTwo: parTwoLim}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11], 
    NMX=3000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e+1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [5,10,15,20,100]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion
#%% TwoPar - delta
# region  
twoPar = run(eq, NMX=1)
parTwo = 'delta'
parTwoLim = [0.01, 3]
for sol in eq(['HB']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'p': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'p'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
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
#%% Initial conditions - low delta
# region
parTwo = 'delta'
parTwoLim = [0.001, 3]
eq = run(
    model, 
    IPS=1, 
    ICP=['p'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 0.59}, 
    PAR = {'delta': 0.01}
)
# eq = run(
#     eq, 
#     IPS=1, 
#     ICP=[parTwo], 
#     NMX=5000,
#     DS=-1e-2,
#     DSMAX=1e-1,
#     UZSTOP={parTwo: parTwoLim}
# )
# eq = run(
#     eq, 
#     IPS=1, 
#     ICP=[parTwo], 
#     NMX=8000,
#     DS=1e-3,
#     DSMAX=5e-3,
#     UZSTOP={parTwo: parTwoLim}
# )
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['p', 11], 
    NMX=3000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e+1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [5,10,15,20,100]}
)
diag = eq + cycle
diag = relabel(diag)
save(diag, 'eqO')
cl()
# endregion