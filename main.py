from data_loader import load_excel_adrien,extract_important_data
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
from validation import validate_against_excel
from models import ExcelAdrien

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
    model = ExcelAdrien(analysis_data)
     
    dP_dt = np.gradient(
        analysis_data.pressure_amont,
        analysis_data.time,
    )

    #plotting(analysis_data.time,"Time",dP_dt,"Derivative")
    
    a_amont,b_amont,p_amont_smooth=model.local_linear_regression(analysis_data.pressure_amont)
    a_avale,b_avale,p_avale_smooth=model.local_linear_regression(analysis_data.pressure_avale)

    
    p_apparent_smooth = model.apparent_pressure(
        p_amont_smooth,
        p_avale_smooth,
    )

    permeability_apparent = model.apparent_permeability(
        a_amont,
        p_amont_smooth,
        p_avale_smooth,
    )

    conductance_apparent = model.apparent_conductance(
        permeability_apparent,
        p_apparent_smooth,
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

    
    plt.figure(figsize=(10, 6))

    plt.plot(
        analysis_data.time,
        analysis_data.pressure_amont,
        label="Pamont raw",
    )

    plt.plot(
        analysis_data.time,
        p_amont_smooth,
        label="Pamont smooth",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Pressure [Pa]")
    plt.legend()
    plt.grid()

    plt.show()

    plt.figure(figsize=(10, 6))

    plt.plot(
        analysis_data.time,
        dP_dt,
        alpha=0.5,
        label="Raw derivative (np.gradient)",
    )

    plt.plot(
        analysis_data.time,
        a_amont,
        linewidth=2,
        label="Smoothed derivative (linear regression)",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("dP/dt [Pa/s]")

    plt.legend()
    plt.grid()

    plt.show()



if __name__=="__main__":
    main()   