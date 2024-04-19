# Functions for Yield Gap Analysis

import pandas as pd                          # Read data
import numpy as np                           # Array Operations
from scipy.optimize import curve_fit         # Fit function
import warnings                              # mute error code
warnings.filterwarnings('ignore')            # mute error code
from scipy.stats import linregress

def CB_Percentile_Model(df, PRECIP, YIELD, percent_tile):
    df['PRECIP'] = PRECIP
    df['YIELD'] = YIELD
    data=PRECIP.dropna()
    
    PRECIP_bins=np.histogram_bin_edges(data , bins='doane')
    N = np.count_nonzero(PRECIP_bins)
    frontier_yield_obs = np.array([]) # empty array to append yields 
    frontier_PRECIP_obs = np.array([]) # empty array to append PRECIP 


# Loop over observations to identify maximum ET and Yield for each ET bin
    for n in range(0, len(PRECIP_bins)-1):
        idx = (PRECIP >= PRECIP_bins[n]) & (PRECIP < PRECIP_bins[n+1]) 
        
        if np.all(idx == False):
            continue
        else:
            PRECIP_bin = df.loc[idx, 'PRECIP'] # loc precipitation to index for each bin 
            yield_bin = df.loc[idx, 'YIELD'] # loc yield to corresponding yield for each precipitation 
        
            frontier_PRECIP_obs = np.append(frontier_PRECIP_obs, np.percentile(PRECIP_bin, percent_tile)) #append resulting precip data   
            frontier_yield_obs = np.append(frontier_yield_obs, np.percentile(yield_bin, percent_tile))   
    
    PRECIP_max = np.max(PRECIP)
    # Define Cobb-Douglas model 
  
    cobb_douglas = lambda x, a, b, c: a + b * np.log(x) + c * np.log(x)**2 # define lambda function for cobb_douglas  
   
    par0 = [0, 0, 0] # Define initial guess for the parameters of the Cobb-Douglas model
    pars, cov = curve_fit(cobb_douglas,frontier_PRECIP_obs,frontier_yield_obs, 
                          par0, method = 'dogbox')
  
    # Calculate residuals, standard deviation and r2
    stdevs, residuals = np.sqrt(np.diag(cov)), frontier_yield_obs - cobb_douglas(frontier_PRECIP_obs, *pars) 
    ss_res,  ss_tot  = np.sum(residuals**2), np.sum((frontier_yield_obs-np.mean(frontier_yield_obs))**2) 
    r_squared = np.round(1-(ss_res/ss_tot), 2)
    
    # Use parameters to create the y efficiency frontier line
    frontier_PRECIP_line = np.arange(0, PRECIP_max,1) # a range of x values from 0 to max observed 
    frontier_yield_line = cobb_douglas(frontier_PRECIP_line, *pars)

    return (frontier_PRECIP_line, frontier_yield_line, frontier_PRECIP_obs, frontier_yield_obs, PRECIP_bins, pars, 
            len(frontier_PRECIP_line), stdevs, cov, residuals, r_squared, ss_res, ss_tot, N)   

def Yw_Obs(df, PRECIP, YIELD,  method):
    df['PRECIP'] = PRECIP
    df['YIELD'] = YIELD
    
    data=PRECIP.dropna()
    
    PRECIP_bins=np.histogram_bin_edges(data, bins= method)#'auto') #'doane')
    N = np.count_nonzero(PRECIP_bins)
    frontier_yield_obs = np.array([]) # empty array to append yields 
    frontier_PRECIP_obs = np.array([]) # empty array to append PRECIP 

# Loop over observations to identify maximum ET and Yield for each ET bin
    for n in range(0, len(PRECIP_bins)-1):
        idx = (PRECIP >= PRECIP_bins[n]) & (PRECIP < PRECIP_bins[n+1]) 
        
        if np.all(idx == False):
            continue
        else:
            PRECIP_bin = df.loc[idx, 'PRECIP'] # loc precipitation to index for each bin 
            yield_bin = df.loc[idx, 'YIELD'] # loc yield to corresponding yield for each precipitation 
        
            max_yield_bin = np.amax(yield_bin.values)
            idx_max_yield_bin = np.argmax(yield_bin.values)
            corresponding_PRECIP_bin = PRECIP_bin.iloc[idx_max_yield_bin] 
            
            frontier_PRECIP_obs = np.append(frontier_PRECIP_obs, corresponding_PRECIP_bin) #append resulting ET data 
            frontier_yield_obs = np.append(frontier_yield_obs, max_yield_bin) #append resulting yield data   

    return (frontier_PRECIP_obs, frontier_yield_obs)   

def TE_MWL(y_values, x_values, median_precip):
    slope, intercept, r_value, p_value, std_err = linregress(x_values,y_values)
    x1=np.arange(0,800)
    y1=slope*x1+intercept
    
    water_loss=x1[np.where(y1 == y1[y1>0][0])[0][0]]
    
    print('MWL', water_loss, "\nTE", slope)
