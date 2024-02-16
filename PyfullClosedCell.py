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
#%% Initial conditions - fullOpenCell
file = "AUTOfullClosedCell"
model = load(file) 
# run(
#     model, 
#     IPS=-2, 
#     ICP=[14], 
#     NMX=40000,
# )
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2, 
    ICP=['Vplc', 11], 
    NMX=100,
    DS=1e-2,
    DSMAX=1e-0,
    SP=['LP0'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
diag = relabel(eq + cycle)
save(diag, 'eq')
cl()
#%% Low Ct conditions - fullOpenCell
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 75
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
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=500,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
cycle = cycle + run(
    cycle, 
    SP=['LP2', 'TR0', 'PD0'],
)
# pd1 = run(
#     cycle('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd2 = run(
#     pd1('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd3 = run(
#     pd2('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd4 = run(
#     pd3('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd5 = run(
#     pd4('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     NMX=2000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
diag = relabel(eq + cycle 
            #    + pd1 + pd2 + pd3 + pd4 + pd5
            )
save(diag, 'eq')
cl()
#%% Ct - Broad/Narrow Spike - fullOpenCell
file = "AUTOfullClosedCell"
model = load(file) 
VplcVal = 0.1
# run(
#     model, 
#     IPS=-2, 
#     ICP=['TIME'], 
#     NMX=40000,
# )
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': VplcVal}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': [200, -10]},
    UZR={'Ct': [73, 140]}

)
cycle = run(
    eq('HB'), 
    IPS=2, 
    ICP=['Ct', 11, 46], 
    NMX=10000,
    NTST=2000,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'PD3'],
    UZSTOP={'Ct': 10}, 
    UZR={'Ct': [75, 90, 88, 85, 80, 140]}
)
eq  = run(eq, DS=-1e-2)
diag = relabel(eq + cycle)
save(diag, 'eq')
cl()
pd1 = run(
    cycle('PD1'), 
    ISW=-1,
    NTST=2000,
    DSMAX=1e-2,
    SP=['LP5', 'TR0', 'PD2'],
)
# pd2 = run(
#     pd1('PD1'), 
#     ISW=-1,
#     # NTST=4000,
#     SP=['LP0', 'TR0', 'PD2'],
# )
diag = relabel(eq
                + cycle
                + pd1
                # + pd2
            )
save(diag, 'eq')
cl()
#%% Vplc - Narrow Spike - fullOpenCell
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 140
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
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=5000,
    NTST=1200,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP2', 'TR0', 'PD2', 'BP0'],
    # UZSTOP={'Vplc': 0.1575}, 
    UZR={'Vplc': 0.1}
)
cycle = cycle + run(
    cycle, 
    # DS=-1e-4,
    NTST=2200,
    SP=['LP2', 'TR0', 'PD0','BP0'],
)
diag = relabel(eq + cycle 
            )
save(diag, 'eq')
cl()
#%% Vplc - Broad Spike - fullOpenCell
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 75
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
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=500,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
cycle = cycle + run(
    cycle, 
    SP=['LP2', 'TR0', 'PD0'],
)
pd1 = run(
    cycle('PD1'), 
    ISW=-1,
    NTST=1000,
    NMX=7000,
    SP=['LP0', 'TR0', 'PD3', 'BP0'],
)
# pd2 = run(
#     pd1('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd3 = run(
#     pd2('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd4 = run(
#     pd3('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd5 = run(
#     pd4('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     NMX=2000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
diag = relabel(eq + cycle 
               + pd1 
            # + pd2 + pd3 + pd4 + pd5
            )
save(diag, 'eq')
cl()
#%% Vplc - Bursting - fullOpenCell
file = "AUTOfullClosedCell"
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
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=500,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
cycle = cycle + run(
    cycle, 
    SP=['LP2', 'TR0', 'PD0'],
)
pd1 = run(
    cycle('PD1'), 
    ISW=-1,
    NTST=1000,
    NMX=7000,
    SP=['LP0', 'TR0', 'PD3', 'BP0'],
)
pd2 = run(
    pd1('PD1'), 
    ISW=-1,
    NTST=1000,
    SP=['LP0', 'TR0', 'PD3'],
)
# pd3 = run(
#     pd2('PD1'), 
#     ISW=-1,
#     NTST=1000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd4 = run(
#     pd3('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     SP=['LP0', 'TR0', 'PD1'],
# )
# pd5 = run(
#     pd4('PD1'), 
#     ISW=-1,
#     NTST=1600,
#     NMX=2000,
#     SP=['LP0', 'TR0', 'PD1'],
# )
diag = relabel(eq + cycle 
               + pd1 
            + pd2 
            # + pd3 + pd4 + pd5
            )
save(diag, 'eq')
cl()
#%% Ct - fulling - fullOpenCell
file = "AUTOfullClosedCell"
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
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.195}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': [200, 1]}
)
eq  = run(eq, DS=-1e-2)
cycle = run(
    eq('HB'), 
    IPS=2, 
    ICP=['Ct', 11], 
    NMX=1000,
    DS=1e-2,
    DSMAX=1e-0,
    SP=['LP2', 'PD3'],
    UZSTOP={'Ct': 10}, 
    UZR={'Ct': 95}
)
cycle = cycle + run(
    cycle, 
    NMX=2000,
    SP=['LP0', 'PD3'],
)
pd1 = run(
    cycle('PD1'), 
    ISW=-1,
    NTST=1000,
    SP=['LP0', 'TR0', 'PD1'],
)
pd2 = run(
    pd1('PD1'), 
    ISW=-1,
    NTST=1000,
    SP=['LP0', 'TR0', 'PD1'],
)
pd3 = run(
    pd2('PD1'), 
    ISW=-1,
    NTST=1000,
    SP=['LP0', 'TR0', 'PD1'],
)
pd4 = run(
    pd3('PD1'), 
    ISW=-1,
    NTST=1600,
    SP=['LP0', 'TR0', 'PD1'],
)
pd5 = run(
    pd4('PD1'), 
    ISW=-1,
    NTST=1600,
    NMX=2000,
    SP=['LP0', 'TR0', 'PD1'],
)
diag = relabel(eq + cycle + pd1 + pd2 + pd3 + pd4 + pd5)
save(diag, 'eq')
cl()

#%% Basic TwoPar Ct-Vplc - fullOpenCell 
# region 
file = "AUTOfullClosedCell"
model = load(file) 
"""
Hopf bifurcations 
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 140}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)

twoPar = run(model, NMX=1)
for sol in eq(['HB1']):
    fwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-0, 
        NMX=6000,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    bwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-0, 
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    twoPar = twoPar + merge(fwd+bwd)
twoPar = relabel(twoPar)
save(twoPar, 'eqT')
cl()
print(twoPar)
# endregion
#%% TwoPar Ct-Vplc - fullOpenCell
# region 
file = "AUTOfullClosedCell"
model = load(file) 
"""
Hopf bifurcations 
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 140}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)

twoPar = run(model, NMX=1)
for sol in eq(['HB1']):
    fwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-0, 
        NMX=6000,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    bwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-0, 
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    twoPar = twoPar + merge(fwd+bwd)
"""
First Generalized Hopf
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 120}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP2', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
for sol in cycle(['LP1', 'PD2']):
    t = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-0, 
        NMX=6000,
        NTST=1200,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-2,)
    bwd = run(t, DS=-1e-2)
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
"""
Second Generalized Hopf
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 110}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=500,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
for sol in cycle(['LP2']):
    t = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=24000,
        NTST=1500,
        SP=['LP4', 'UZ', 'BP0', 'CP0', 'BT', 'ZH'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-2,SP=['LP2'])
    bwd = run(t, DS=-1e-2,SP=['LP1'])
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
"""
Third Generalized Hopf
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 50}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB1'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=10000,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP5', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
for sol in cycle(['LP1']):
    t = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=24000,
        NTST=1500,
        SP=['LP4', 'UZ', 'BP0', 'CP0', 'BT', 'ZH'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-2,SP=['LP2'])
    bwd = run(t, DS=-1e-2,SP=['LP1'])
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

"""
Fourth Generalized Hopf
"""
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={'Ct': 20}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB1'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=10000,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP5', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
for sol in cycle(['LP1']):
    t = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=24000,
        NTST=1500,
        SP=['LP4', 'UZ', 'BP0', 'CP0', 'BT', 'ZH'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-2,SP=['LP2'])
    bwd = run(t, DS=-1e-2,SP=['LP1'])
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
print(twoPar)
# endregion
#%% Low Ct conditions - fullOpenCell
# region
file = "AUTOfullClosedCell"
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
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={'Ct': 117}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3}
)
cycle = run(
    eq('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=2000,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP4', 'TR0', 'PD3'],
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1}
)
diag = relabel(eq + cycle)
save(diag, 'eq')
cl()
# endregion