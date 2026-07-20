from data_loader import load_excel_adrien,extract_important_data
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
from experimental_data import Results
from processors import LocalLinearRegressionProcessor, SavgolProcessor
from validation import validate_against_excel
from models import ExcelModel


from plots import (
    plot_pressure_smoothing,
    plot_derivative_comparison, 
    plot_pressure_models,
    plot_apparent_permeability,
    plot_summary,
)

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
    R_GAS,
    REFERENCE_TEMPERATURE,

)

def main():
    raw_data=load_excel_adrien()
    analysis_data=extract_important_data(raw_data)  
    model = ExcelModel(analysis_data)
     
    dP_dt_dummy = np.gradient(
        analysis_data.pressure_amont,
        analysis_data.time,
    )

    analysis_data = extract_important_data(raw_data)

    model = ExcelModel(analysis_data)

    results_linreg = (
        LocalLinearRegressionProcessor()
        .process(
            analysis_data,
            model,
        )
    )

    results_savgol = (
        SavgolProcessor()
        .process(
            analysis_data,
            model,
        )
    )   



   


    PLOT_SUMMARY = True  # Set to True to enable summary plotting
    if PLOT_SUMMARY:
        plot_summary(
            analysis_data,
            results_linreg,
        )
    
    VALIDATION = False  # Set to True to enable validation against Excel data

    if VALIDATION:
        validate_against_excel(
            p_amont_ordre2,
            a_amont,
            b_amont,
            p_amont_smooth,
            p_apparent_smooth,
            k_apparent_exp,
            conductance_apparent,
        )    
    
        plot_pressure_smoothing(
            analysis_data.time,
            analysis_data.pressure_amont,
            p_amont_smooth,
        )

        plot_derivative_comparison(
            analysis_data.time,
            dP_dt_dummy,
            a_amont,
        )

    

    
    
   
    
    plot_derivative_comparison(
        analysis_data.time,
        dP_dt_dummy,
        results_linreg.dP_dt,
        results_savgol.dP_dt,
    )







if __name__=="__main__":
    main()   