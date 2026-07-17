from data_loader import load_excel_adrien,extract_important_data
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
from validation import validate_against_excel

from constants import (
    DYNAMIC_VISCOSITY,
    EPAISSEUR_ECHANTILLON,
    SECTION_PASSANTE,
    CYLINDER_SHAPE_FACTOR,
    V_AMONT,
    APPARENT_PRESSURE_FACTOR,
    
    SECTION_PASSANTE,
    DYNAMIC_VISCOSITY,
    EPAISSEUR_ECHANTILLON,

)

def plotting(x,name_x,y,name_y):
    plt.plot(
    x,y
    )

    plt.xlabel(name_x)
    plt.ylabel(name_y)
    plt.grid()

    plt.show()

def local_linear_regression(time,pressure,half_window):
    a_array=[]
    b_array=[]
    N=len(time)
    for i in range(N):
        
        start = max(i - half_window, 0)
        end = min(i + half_window + 1, N)
        t = time[start:end]
        P = pressure[start:end]
        a,b=np.polyfit(t,P,1)
        a_array.append(a)
        b_array.append(b)
    
    a_array=np.array(a_array)
    b_array=np.array(b_array)
    p_smooth_array=a_array*time+b_array

    return a_array,b_array,p_smooth_array

def main():
    raw_data=load_excel_adrien()
    analysis_data=extract_important_data(raw_data)   
    dP_dt = np.gradient(
        analysis_data.pressure_amont,
        analysis_data.time,
    )

    #plotting(analysis_data.time,"Time",dP_dt,"Derivative")
    
    a_amont,b_amont,p_amont_smooth=local_linear_regression(analysis_data.time,analysis_data.pressure_amont,126)
    a_avale,b_avale,p_avale_smooth=local_linear_regression(analysis_data.time,analysis_data.pressure_avale,126)

    p_apparent_smooth=APPARENT_PRESSURE_FACTOR*p_amont_smooth+(1-APPARENT_PRESSURE_FACTOR)*p_avale_smooth
    
    permeability_apparent = (
        np.abs(a_amont)
        * V_AMONT
        * DYNAMIC_VISCOSITY
        * EPAISSEUR_ECHANTILLON
        / SECTION_PASSANTE
        / CYLINDER_SHAPE_FACTOR
        / (0.5 * (p_amont_smooth**2 - p_avale_smooth**2))
    )
    
    conductance_apparent = (
        SECTION_PASSANTE
        * permeability_apparent
        * p_apparent_smooth
        / DYNAMIC_VISCOSITY
        / EPAISSEUR_ECHANTILLON
    )    

    
    VALIDATION = True

    if VALIDATION:
        validate_against_excel(
            a_amont,
            b_amont,
            p_amont_smooth,
            p_apparent_smooth,
            permeability_apparent,
            conductance_apparent,
        )


if __name__=="__main__":
    main()   