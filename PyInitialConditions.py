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
file = "AUTOBurstOpenCell"
model = load(file, constants = file) 
run(
    model, 
    IPS=-2, 
    ICP=['TIME'], 
    NMX=5000,
    NPR=1000,
)
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 1}
)
save(eq, 'eq')
cl()
#%% Initial conditions - OpenCell
file = "AUTOOpenCell"
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
    DS=3e-2,
    DSMAX=1e-0,
    UZSTOP={'p': 1}
)

save(eq, 'eq')
cl()
#%% Initial conditions - BurstClosedCell
file = "AUTOBurstClosedCell"
model = load(file) 
run(
    model, 
    IPS=-2, 
    ICP=['TIME'], 
    NMX=40000,
)
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 1}
)
cl()
