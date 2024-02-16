#%% 
# region Libraries
import numpy as np
from scipy.integrate import solve_ivp
# endregion
#%% 
def fullOpenCell(t, y, par):
    """
    Create the model equations using Scipy for integration (solve_ivp)
    Parameters
    ----------
    t: double, time 
    y: vector with the state variables

    Returns 
    ----------
    field: vector with the field equations
    """
    """
    Declare variables
    """
    c, ce, h, p, s = y
    """
    Declare parameters 
    """
    #Volume
    gamma=par['gamma']
    delta = par['delta']
    Ts = par['Ts']
    delta = par['delta']
    Tp = par['Tp']
    """ 
    Declare fluxes 
    """
    Jipr = getIPR(y, par)
    Jh = getJh(y, par)
    Th = getTh(y, par)
    Jserca= getSERCA(y, par)
    Jsoce = getSOCE(y, par)
    Jpm = getPMCA(y, par)
    L = getL(y, par)
    """
    Declare field 
    """
    dc=(Jipr - Jserca) + delta*(s - Jpm)
    dce=gamma*(Jserca - Jipr)
    dh=Jh/Th
    dp=(L)/Tp
    ds=(Jsoce - s)/Ts
    field = [dc, dce, dh, dp, ds]
    """
    Return
    """
    return field 
def simpleOpenCell(t, y, par):
    """
    Create the model equations using Scipy for integration (solve_ivp)
    Parameters
    ----------
    t: double, time 
    y: vector with the state variables

    Returns 
    ----------
    field: vector with the field equations
    """
    """
    Declare variables
    """
    c, ce, h, s = y
    """
    Declare parameters 
    """
    #Volume
    gamma=par['gamma']
    delta = par['delta']
    Ts = par['Ts']
    delta = par['delta']
    Tp = par['Tp']
    """ 
    Declare fluxes 
    """
    Jipr = getIPR(y, par)
    Jh = getJh(y, par)
    Th = getTh(y, par)
    Jserca= getSERCA(y, par)
    Jsoce = getSOCE(y, par)
    Jpm = getPMCA(y, par)
    """
    Declare field 
    """
    dc=(Jipr - Jserca) + delta*(s - Jpm)
    dce=gamma*(Jserca - Jipr)
    dh=Jh/Th
    ds=(Jsoce - s)/Ts
    field = [dc, dce, dh, ds]
    """
    Return
    """
    return field 

def fullClosedCell(t, y, par):
    """
    Create the model equations using Scipy for integration (solve_ivp)
    Parameters
    ----------
    t: double, time 
    y: vector with the state variables

    Returns 
    ----------
    field: vector with the field equations
    """
    """
    Declare variables
    """
    c, h, p= y
    """
    Declare parameters 
    """
    #Volume
    gamma=par['gamma']
    delta = par['delta']
    Ts = par['Ts']
    delta = par['delta']
    Tp = par['Tp']
    """ 
    Declare fluxes 
    """
    Jipr = getIPR(y, par)
    Jh = getJh(y, par)
    Th = getTh(y, par)
    Jserca= getSERCA(y, par)
    L = getL(y, par)
    """
    Declare field 
    """
    dc=(Jipr - Jserca)
    dh=Jh/Th
    dp=(L)/Tp
    field = [dc, dh, dp]
    """
    Return
    """
    return field 
def simpleClosedCell(t, y, par):
    """
    Create the model equations using Scipy for integration (solve_ivp)
    This model only includes the equations for cytoplasm and ER Ca2+. 
    Parameters
    ----------
    t: double, time 
    y: vector with the state variables

    Returns 
    ----------
    field: vector with the field equations
    """
    """
    Declare variables
    """
    c, h = y
    """
    Declare parameters 
    """
    #Volume
    gamma=par['gamma']
    delta = par['delta']
    Ts = par['Ts']
    delta = par['delta']
    Tp = par['Tp']
    """ 
    Declare fluxes 
    """
    Jipr = getIPR(y, par)
    Jh = getJh(y, par)
    Th = getTh(y, par)
    Jserca= getSERCA(y, par)
    """
    Declare field 
    """
    dc=(Jipr - Jserca)
    dh=Jh/Th
    field = [dc, dh]
    """
    Return
    """
    return field 
#%%
def parFullOpenCell():
    """
    This is the main parameter set used in the fullOpenCell and fullClosedCell models
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    par = {
        # PMCA 
        'Vpm': 3.0, 
        'Kpm': 0.2, 
        # SOCE 
        's1': 0.2, 
        'Vsoce': 3, 
        'Ts': 15, 
        'Ke': 800, 
        # IP3 
        'Vdeg': 6, 
        'Kdeg': 0.5,
        'Vplc': 0, 
        'Tp': 2, 
        # 'p': 0, 
        # Volume
        'gamma': 5.5,
        'delta': 2,
        # Total Ca, conserved for closed cell problems 
        'Ct': 147,
        # IPR 
        'Kf': 1.6,
        'kbeta': 0.4,
        'Kp': 10,
        'Kc': 0.16,
        # H
        'Kh': 0.168,
        'Tmax': 7.5,
        'Kt': 0.095,
        # SERCA 
        'Vs': 2.0,
        'Kbar': 1e-8,
        'Ks': 0.19,
        
    }
    return par

def parSimpleOpenCell():
    """
    This is the main parameter set used in the simpleOpenCell and simpleClosedCell models
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    par = {
        # PMCA 
        'Vpm': 3.0, 
        'Kpm': 0.2, 
        # SOCE 
        's1': 0.2, 
        'Vsoce': 3, 
        'Ts': 25, 
        'Ke': 800, 
        # IP3 
        'Vdeg': 6, 
        'Kdeg': 0.5,
        'Vplc': 0, 
        'Tp': 2, 
        # 'p': 0, 
        # Volume
        'gamma': 5.5,
        'delta': 2,
        # Total Ca, conserved for closed cell problems 
        'Ct': 147,
        # IPR 
        'Kf': 1.6,
        'kbeta': 0.4,
        'Kp': 10,
        'Kc': 0.16,
        # H
        'Kh': 0.12,
        'Tmax': 30,
        'Kt': 0.09,
        # SERCA 
        'Vs': 2.0,
        'Kbar': 1e-8,
        'Ks': 0.19,
        
    }
    return par

def icsFullOpenCell():
    """
    These are the coordinates of the resting EQ point for the corresponding model 
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    dic = {
        #Initial conditions 
        'c': 8.09050E-02,
        'ce': 8.09050E+02, 
        'h': 9.48960E-01,
        'p': 0,
        's': 4.21884E-01,
    }
    return dic

def icsSimpleOpenCell():
    """
    These are the coordinates of the resting EQ point for the corresponding model
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    dic = {
        #Initial conditions 
        'c': 8.0905040989E-002,
        'ce':8.0905041234E+002, 
        'h': 8.2875969080E-001,
        's': 4.2188446695E-001,
    }
    return dic

def icsFullClosedCell():
    """
    These are the coordinates of the resting EQ point for the corresponding model
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    dic = {
        #Initial conditions 
        'c': 8.09050E-02,
        'h': 9.48960E-01,
        'p': 0,
    }
    return dic

def icsSimpleClosedCell():
    """
    These are the coordinates of the resting EQ point for the corresponding model
    Parameters
    ----------
    Returns 
    ----------
    par: dict, set of named parameters
    """
    dic = {
        #Initial conditions 
        'c': 8.09050E-02,
        'h': 9.48960E-01,
    }
    return dic
# par = params()
# Kf=par['Kf']
# p=par['Kf']
# kbeta=par['kbeta']
# Kp=par['Kp']
# Kc=par['Kc']
# Kh=par['Kh']
# gamma=par['gamma']
# delta=par['delta']
# Vs=par['Vs']
# Kbar=par['Kbar']
# Ks=par['Ks']
# Tmax=par['Tmax']
# Kt=par['Kt']
# Ke=par['Ke']
# Vsoce=par['Vsoce']
# a0=par['a0']
# Kpm=par['Kpm']
# Vpm=par['Vpm']
# Ts=par['Ts']
# s1=par['s1']

#%%
# region fluxes
def getPMCA(y, par):     
    """
    The PMCA flux
    Parameters
    ----------
    y: vector with the state variables

    Returns 
    ----------
    Jpm: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    #PM 
    Vpm=par['Vpm']
    Kpm=par['Kpm']
    # PM
    Jpm = (Vpm*c**2)/(c**2 + Kpm**2)
    return Jpm
    
def getIPR(y, par): 
    """
    The IPR flux
    Parameters
    ----------
    y: vector with the state variables

    Returns 
    ----------
    Jipr: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    # IPR 
    Kf=par['Kf']
    kbeta=par['kbeta']
    Kp=par['Kp']
    Kc=par['Kc']
    Kh=par['Kh']
    gamma=par['gamma']    
    ma = c**4 / (Kc**4 + c**4)
    B = p**2 / (Kp**2 + p**2)
    A = 1 - p**2 / (Kp**2 + p**2)
    ha = Kh**4 / (Kh**4 + c**4)
    alpha = A*(1-ma*ha)
    beta = B*ma*h
    P0 = beta/(beta + kbeta*(beta + alpha))   
    Jipr=Kf*P0*(ce-c)
    return Jipr

def getP0(y, par): 
    """
    The open probability of the IPR
    Parameters
    ----------
    y: vector with the state variables

    Returns 
    ----------
    Jipr: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    # IPR 
    Kf=par['Kf']
    kbeta=par['kbeta']
    Kp=par['Kp']
    Kc=par['Kc']
    Kh=par['Kh']
    gamma=par['gamma']    
    ma = c**4 / (Kc**4 + c**4)
    B = p**2 / (Kp**2 + p**2)
    A = 1 - p**2 / (Kp**2 + p**2)
    ha = Kh**4 / (Kh**4 + c**4)
    alpha = A*(1-ma*ha)
    beta = B*ma*h
    P0 = beta/(beta + kbeta*(beta + alpha))   
    return P0

def getSERCA(y, par): 
    """
    The SERCA flux
    Parameters
    ----------
    y: vector with the state variables
    par: dictionary, the parameter set

    Returns 
    ----------
    Jserca: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    # SERCA 
    Vs=par['Vs']
    Kbar=par['Kbar']
    Ks=par['Ks']
    gamma=par['gamma']    
    Jserca=(Vs*(c**2 - Kbar*ce**2))/(c**2 + Ks**2)
    return Jserca

def getJh(y, par): 
    """
    The flux for the auxiliary variable h 
    Parameters
    ----------
    y: vector with the state variables
    par: dictionary, the parameter set
    Returns 
    ----------
    Jh: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    Kh=par['Kh']
    Jh=(Kh**4 / (Kh**4 + c**4)) - h
    return Jh

def getTh(y, par): 
    """
    The timescale for the auxiliary variable h 
    Parameters
    ----------
    y: vector with the state variables
    par: dictionary, the parameter set
    Returns 
    ----------
    Th: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    Kt=par['Kt']
    Tmax=par['Tmax']
    Th=Tmax*(Kt**4 / (Kt**4 + c**4))
    return Th
def getSOCE(y, par): 
    """
    The flux through SERCA
    Parameters
    ----------
    y: vector with the state variables
    par: dictionary, the parameter set
    Returns 
    ----------
    Th: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    Ke=par['Ke']
    s1=par['s1']
    Vsoce=par['Vsoce']
    Jsoce =Vsoce/(1+np.exp(s1*(ce-Ke)))
    return Jsoce

def getL(y, par): 
    """
    The fluxes relating to IP3 production as a function of PLC
    and decay as a result of metabolism
    Parameters
    ----------
    y: vector with the state variables
    par: dictionary, the parameter set
    Returns 
    ----------
    L: double
    """
    #Variables 
    if len(y) == 5:
        c, ce, h, p, s = y
    if len(y) == 4:
        c, ce, h, s = y
        p = par['p']
    if len(y) == 3:
        c, h, p = y
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    if len(y) == 2:
        c, h = y
        p = par['p']
        gamma=par['gamma']
        Ct=par['Ct']
        ce = gamma*(Ct-c)
    Vdeg=par['Vdeg']
    Kdeg=par['Kdeg']
    Vplc=par['Vplc']
    IPdeg=Vdeg*c**2/(c**2+Kdeg**2)
    L=Vplc - IPdeg*p
    return L
#%%
def getIVP(model, par, ics, tini=0, tf=100): 
    """
    Simple integration using the solve_ivp routine from Scipy 

    Parameters
    ----------
    model: func, model to integrate
    par: dict, set of named parameters 
    ics: dict, set of named initial conditions
    tini: double, start of integration time
    tf: double, end of integration time 

    Returns 
    ----------
    data: array, first entry is t value, rest of values are the model variables
    """
    data = solve_ivp(model, [tini, tini+tf],list(ics.values()), method = 'Radau', max_step = 1, rtol = 1e-7, atol = 1e-9, args = (par,))
    data = np.vstack((data.t, data.y))
    return data

def getAlphaResponse(model, par, ics, p0=0, tini=0, tp=50, tf=100): 
    """
    Integrate the model
    All runs are integrated initially from tini to tini+tp, and then from tini+tp to tini+tp+tf

    Parameters
    ----------
    model: func, model to integrate
    par: dict, set of named parameters 
    ics: dict, set of named initial conditions
    tini: double, start of integration time
    tf: double, end of integration time 

    Returns 
    ----------
    data: array, first entry is t value, rest of values are the model variables
    """
    ics = getICS(par, par['c'])
    inidata = getIVP(par, ics, tini, tp)
    newICS = getnewICS(inidata)
    par['p'] =  p0 
    auxData = getIVP(par, newICS, tp, tf)
    data = np.concatenate((inidata, auxData), axis=1)
    return data

def getnewICS(data): 
    """
    Get the initial conditions of the open cell model using the 
    last data point of a former run
    Parameters
    ----------
    data: array

    Returns 
    ----------
    ics: vector in the form [c, ce, h, j, p]
    """
    ics = data[1:][:,-1]
    if len(ics) == 5:
        ics = {
        'c': ics[0],
        'ce': ics[1],
        'h': ics[2], 
        'p': ics[3],
        's': ics[4],
        }
    if len(ics) == 4:
        ics = {
        'c': ics[0],
        'ce': ics[1],
        'h': ics[2], 
        's': ics[3],
        }
    if len(ics) == 3:
        ics = {
        'c': ics[0],
        'h': ics[1], 
        'p': ics[2],
        }
    if len(ics) == 2:
        ics = {
        'c': ics[0],
        'h': ics[1], 
        }
    return ics


# endregion 


#%% 
"""
Miscellaneous functions designed to facilitate writing the AUTO f90 files 
"""
"""
getICS - get initial conditions in a printed format for the specified parameters
getParNum - return format gamma=PAR(1) - f90 file
getParValues return format gamma=1 - f90 file
getNumPar - return format PAR(1)=gamma - f90 file
getParnames - return format "gamma": 1 - constants file
"""

def printICS(ics): 
    i=1 
    for key, value in ics.items():
        print(r'U(' + str(i) + r')' + r'=' + str(value))
        i=i+1
    
def getParNum(par):
    i=1 
    for key, value in par.items():
        if type(value) != str: 
            print(str(key) + r'=PAR(' + str(i) + r')' )
            i=i+1
            if i==11:
                print(r'PERIOD=PAR(11)')
                i=i+1
            if i==14:
                print(r'TIME=PAR(14)')
                i=i+1

def getParValues(par):
    i=1 
    for key, value in par.items():
        if type(value) != str: 
            print(str(key) + r'=' + str(value) + r'' )
            i=i+1
            if i==11:
                i=i+1
            if i==14:
                i=i+1

def getNumPar(par):
    i=1 
    for key, value in par.items():
        if type(value) != str: 
            print(r'PAR(' + str(i) + r')=' + str(key) )
            i=i+1
            if i==11:
                print(r'PAR(11)=0.0')
                i=i+1
            if i==14:
                print(r'PAR(14)=0.0')
                i=i+1
def getParnames(par): 
    i=1
    for key, value in par.items():
        if type(value) != str: 
            print("" + str(i) + ": '" + key +"'," )
            i+=1
            if i==11:
                print("" + r'11' + ": '" + r'PERIOD' +"'," )
                i=i+1
            if i==14:
                print("" + r'14' + ": '" + r'TIME' +"'," )
                i=i+1

# %%
