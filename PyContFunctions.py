#%%
import sys
import os
import numpy as np
import pandas as pd
from scipy.io import savemat
auto_directory = "/home/huitzil/auto/07p/python" 
sys.path.append(auto_directory)
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
sys.path.append(parentPath)
from subprocess import call 
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
# from Python.openCellZeroDimCt import params
#%%
def parChange(newPar, modelName, startPar):
    model = load(modelName, constants = modelName) 
    eqN = run(
        model, 
        ICP=['delta'], 
        NMX=3, 
        DS=3e-2,
    )
    #Run parameter changes, one at a time 
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
    # eqN = run(
    #     eqN,
    #     ICP=["p"],
    #     UZSTOP={'p': [0.995]},
    #     DS=3e-2,
    #     DSMAX=1e-2,
    #     # UZR={'p': [1]},
    #     # PAR={'Ts': 100}
    # )
    # if eqN('HB') != []:
    #     eqN = eqN + run(
    #         eqN('HB1'), 
    #         IPS=2,
    #         # ISP=3,
    #         ICP=["p", 11, 46],
    #         DSMAX=e-1,
    #         NMX=1000,
    #         NPR=100,
    #         NTST=300,
    #         UZSTOP={'p': [1.95], 11:[1e+4]},
    #         DS=5e-2,
    #         SP=['LP0', 'UZ'],
    #         UZR={'p': [0.532]},
    #     )
    # save(eqN, 'eqN')
    # call(["gnome-terminal", ])
    # os.system(r'@pp eqN')
    cl()
    return eqN

def parTwo(parTwo, modelName, parTwoLim, eqDiag):
    model = load(modelName, constants = modelName) 
    twoPar = run(model, NMX=1)
    #Run parameter changes, one at a time 
    for sol in eqDiag(['LP', 'HB']):
        fwd = run(
            sol, 
            ICP = [parTwo, 'p'], 
            ISW=2, 
            DS = 1e-2,
            NMX=6000,
            SP=['LP0', 'UZ', 'BP0'],
            UZSTOP={'p': [0, 2], parTwo: parTwoLim},
        )
        bwd = run(
            sol, 
            ICP = [parTwo, 'p'], 
            ISW=2, 
            DS = -1e-2, 
            NMX=6000,
            SP=['LP0', 'UZ', 'BP0'],
            UZSTOP={'p': [0, 2], parTwo: parTwoLim},
        )
        twoPar = twoPar + merge(fwd+bwd)
    twoPar = relabel(twoPar)
    print(twoPar)
    save(twoPar, 'eqT')
    cl()

# def parChangeNoSave(parTwo, modelName, parTwoLim, eqDiag):
#     model = load(modelName, constants = modelName) 
#     twoPar = run(model, NMX=1)
#     #Run parameter changes, one at a time 
#     for sol in eqDiag(['LP', 'HB']):
#         fwd = run(
#             sol, 
#             ICP = [parTwo, 'p'], 
#             ISW=2, 
#             DS = 1e-2,
#             NMX=6000,
#             SP=['LP0', 'UZ'],
#             UZSTOP={'p': [0, 2], parTwo: parTwoLim},
#         )
#         bwd = run(
#             sol, 
#             ICP = [parTwo, 'p'], 
#             ISW=2, 
#             DS = -1e-2, 
#             NMX=6000,
#             SP=['LP0', 'UZ'],
#             UZSTOP={'p': [0, 2], parTwo: parTwoLim},
#         )
#         twoPar = twoPar + merge(fwd+bwd)
#     twoPar = relabel(twoPar)
#     # print(twoPar)
#     # save(twoPar, 'eqT')
#     cl()
#     return twoPar

def pDiagramCC(model, LP = True, maxp = 2):
    eq = run(
    model,
    ICP=["p"],
    UZSTOP={'p': [maxp]},
    DS=1e-3,
    DSMAX=5e-3,
    NMX=40000,
    # UZR={'p': [1]},
    # PAR={'Ts': 100}
    )
    if eq(['HB']) != []:
        if LP:
            LP1 = run(
                eq('HB')[-1], 
                IPS=2,
                ICP=["p", 11, 46],
                DSMAX=1e-0,
                NMX=20000,
                NTST=300,
                UZSTOP={'p': [10], 11:[1e+4]},
                DS=5e-2,
                SP=['LP1', 'UZ20'],
                UZR={'p': [1]},
            )
        cycle = run(
            eq('HB')[-1], 
            IPS=2,
            ICP=["p", 11, 46],
            DSMAX=1e-0,
            NMX=20000,
            NTST=300,
            NPR=5000, 
            UZSTOP={'p': [10], 11:[1e+4]},
            DS=5e-2,
            SP=['LP0', 'UZ20'],
            UZR={'p': [1]},
        )
    if LP:
        diag = eq + LP1 + cycle
    else:
        diag = eq + cycle
    diag = relabel(diag)
    cl()
    return diag



def sensitivityRunCC(startPar, model, percent):
    # model = load(modelName, constants = modelName)
    # Run the initial diagram 
    eq = pDiagramCC(model, LP = True)
    #Run parameter changes, one at a time 
    pars = []
    lp1 = np.array([])
    hb1 = np.array([])
    lpcAmp = np.array([])
    lpcP = np.array([])
    model = run(model, NMX=1)
    for par in startPar:
        value = model('EP1')[par]
    # Decreasing parameter case
        bw = run(
            model, 
            ICP = [par], 
            DS=-1e-4,
            NMX=10000,
            DSMAX=1,
            UZSTOP = {par: value*(1-percent)}
        )
        bw = pDiagramCC(bw)
        pars.append(str(par + "-"))
        if bw('LP') != []:
            lp1 = np.append(lp1, bw('LP1')['p'])
            # lp1.append(bw('LP1')['p'])
        else:
            lp1 = np.append(lp1, -1)
        if bw('HB') != []:
            hb1 = np.append(hb1, bw('HB1')['p'])
            # hb1.append(bw('HB1')['p'])
        else:
            hb1 = np.append(hb1, -1)
            # hb1.append(-1)
        if bw[1]('LP') != []:
            lpcP = np.append(lpcP, bw[1]('LP1')['p'])
            lpcAmp = np.append(lpcAmp, bw[1]('LP1')['MAX c'])
        else:
            lpcP = np.append(lpcP, -1)
            lpcAmp = np.append(lpcAmp, -1)      
     # Increasing parameter case
        fw = run(
            model, 
            ICP = [par], 
            DS=1e-4,
            NMX=10000,
            DSMAX=1,
            UZSTOP = {par: value*(1+percent)}
        )
        fw = pDiagramCC(fw)
        pars.append(str(par + "+"))
        if fw('LP') != []:
            lp1 = np.append(lp1, fw('LP1')['p'])
            # lp1.append(fw('LP1')['p'])
        else:
            lp1 = np.append(lp1, 0)
        if fw('HB') != []:
            hb1 = np.append(hb1, fw('HB1')['p'])
            # hb1.append(fw('HB1')['p'])
        else:
            hb1 = np.append(hb1, 0)
            # hb1.append(-1)
        if fw[1]('LP') != []:
            lpcP = np.append(lpcP, fw[1]('LP1')['p'])
            lpcAmp = np.append(lpcAmp, fw[1]('LP1')['MAX c'])
        else:
            lpcP = np.append(lpcP, 0)
            lpcAmp = np.append(lpcAmp, 0)    
    cl()
    distBurst = lp1 - hb1 
    distBurst = (distBurst - (eq('LP1')['p'] - eq('HB1')['p']))/((eq('LP1')['p'] - eq('HB1')['p']))  
    lp1 = (lp1-eq('LP1')['p'])/eq('LP1')['p']
    hb1 = (hb1-eq('HB1')['p'])/eq('HB1')['p']
    lpcP = (lpcP - eq[1]('LP1')['p'])/eq[1]('LP1')['p']
    lpcAmp = (lpcAmp - eq[1]('LP1')['MAX c'])/eq[1]('LP1')['MAX c']
    data = {
        '% LP1': lp1*100, 
        '% HB1': hb1*100, 
        '% Burst': distBurst*100, 
        '% Amp LPC': lpcAmp*100, 
        '% p LPC': lpcP*100, 
    }
    data = pd.DataFrame(data, index = pars)
    return data



def sensitivityRunOC(startPar, modelName, percent):
    model = load(modelName, constants = modelName)
    # Run the initial diagram 
    eq = pDiagramCC(model, LP = False)
    #Run parameter changes, one at a time 
    pars = []
    hb1 = np.array([])
    hb2 = np.array([])
    hb3 = np.array([])
    hb4 = np.array([])
    hbAmp = np.array([])
    model = run(model, NMX=1)
    for par in startPar:
        value = model('EP1')[par]
    # Decreasing parameter case
        bw = run(
            model, 
            ICP = [par], 
            DS=-1e-4,
            NMX=10000,
            DSMAX=1,
            UZSTOP = {par: value*(1-percent)}
        )
        bw = pDiagramCC(bw)
        pars.append(str(par + "-"))
        if bw('HB1') != []:
            hb1 = np.append(hb1, bw('LP1')['p'])
            # lp1.append(bw('LP1')['p'])
        else:
            hb1 = np.append(hb1, -1)
        if bw('HB2') != []:
            hb2 = np.append(hb2, bw('HB1')['p'])
            # hb1.append(bw('HB1')['p'])
        else:
            hb2 = np.append(hb2, -1)
        if bw('HB3') != []:
            hb3 = np.append(hb3, bw('LP1')['p'])
            # lp1.append(bw('LP1')['p'])
        else:
            hb3 = np.append(hb3, -1)
        if bw('HB4') != []:
            hb4 = np.append(hb4, bw('HB1')['p'])
            # hb1.append(bw('HB1')['p'])
        else:
            hb4 = np.append(hb4, -1)
            # hb1.append(-1)
        # if bw[1]('LP') != []:
        #     lpcP = np.append(lpcP, bw[1]('LP1')['p'])
        #     lpcAmp = np.append(lpcAmp, bw[1]('LP1')['MAX c'])
        # else:
        #     lpcP = np.append(lpcP, -1)
        #     lpcAmp = np.append(lpcAmp, -1)      
     # Increasing parameter case
        fw = run(
            model, 
            ICP = [par], 
            DS=1e-4,
            NMX=10000,
            DSMAX=1,
            UZSTOP = {par: value*(1+percent)}
        )
        fw = pDiagramCC(fw)
        pars.append(str(par + "+"))
        if fw('HB1') != []:
            hb1 = np.append(hb1, fw('LP1')['p'])
            # lp1.append(fw('LP1')['p'])
        else:
            hb1 = np.append(hb1, -1)
        if fw('HB2') != []:
            hb2 = np.append(hb2, fw('HB1')['p'])
            # hb1.append(fw('HB1')['p'])
        else:
            hb2 = np.append(hb2, -1)
        if fw('HB3') != []:
            hb3 = np.append(hb3, fw('LP1')['p'])
            # lp1.append(fw('LP1')['p'])
        else:
            hb3 = np.append(hb3, -1)
        if fw('HB4') != []:
            hb4 = np.append(hb4, fw('HB1')['p'])
            # hb1.append(fw('HB1')['p'])
        else:
            hb4 = np.append(hb4, -1)   
    cl()
    # distBurst = lp1 - hb1 
    # distBurst = (distBurst - (eq('LP1')['p'] - eq('HB1')['p']))/((eq('LP1')['p'] - eq('HB1')['p']))  
    for hb in eq('HB'):
        
        hb1 = (hb1-eq('HB1')['p'])/eq('HB1')['p']
    hb1 = (hb1-eq('HB1')['p'])/eq('HB1')['p']
    # lpcP = (lpcP - eq[1]('LP1')['p'])/eq[1]('LP1')['p']
    # lpcAmp = (lpcAmp - eq[1]('LP1')['MAX c'])/eq[1]('LP1')['MAX c']
    data = {
        '% LP1': lp1*100, 
        '% HB1': hb1*100, 
        '% Burst': distBurst*100, 
        '% Amp LPC': lpcAmp*100, 
        '% p LPC': lpcP*100, 
    }
    data = pd.DataFrame(data, index = pars)
    return data

def timeSeries(model, pval, tf):
    eq = run(
        model, 
        ICP=['TIME'], 
        NMX=30000, 
        DS=3e-2,
        UZSTOP = {'TIME': tf}, 
        PAR = {'p': pval},
    )
    save(eq, 'eqTS')
    cl()