from data_loader import load_excel_adrien,extract_important_data
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
from experimental_data import Results
from validation import validate_against_excel
from models import ExcelAdrien

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

    k_apparent_exp = model.apparent_permeability_experimental(
        a_amont,
        p_amont_smooth,
        p_avale_smooth,
    )

    conductance_apparent = model.apparent_conductance(
        k_apparent_exp,
        p_apparent_smooth,
    )

    p_amont_ordre2 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=2
    )

    p_amont_ordre1 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=1
    )

    p_amont_ordre0 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=0
    )

    k_apparent_model = model.apparent_permeability_model(
        p_apparent_smooth,
    )

    '''

    plot_pressure_models(
        analysis_data.time,
        analysis_data.pressure_amont,
        p_amont_ordre0,
        p_amont_ordre1,
        p_amont_ordre2,
    )

    plot_apparent_permeability(
        analysis_data.time,
        p_apparent_smooth,
        k_apparent_exp,
        k_apparent_model,
    )

    '''
    
    knudsen = model.knudsen_number(
        p_apparent_smooth,
        characteristic_length=300e-6,
    )
        
    viscous_mask = knudsen < 0.01

    slip_mask = (
        (knudsen >= 0.01)
        & (knudsen < 0.1)
    )

    transition_mask = (
        (knudsen >= 0.1)
        & (knudsen < 10)
    )

    free_molecular_mask = knudsen >= 10

    
    results = Results(
        p_amont_smooth=p_amont_smooth,
        p_avale_smooth=p_avale_smooth,
        p_apparent_smooth=p_apparent_smooth,
        k_apparent_exp=k_apparent_exp,
        k_apparent_model=k_apparent_model,
        conductance_apparent=conductance_apparent,
        p_amont_ordre0=p_amont_ordre0,
        p_amont_ordre1=p_amont_ordre1,
        p_amont_ordre2=p_amont_ordre2,
        knudsen=knudsen,        
        viscous_mask=viscous_mask,
        slip_mask=slip_mask,
        transition_mask=transition_mask,
        free_molecular_mask=free_molecular_mask,

    )




    plot_summary(
        analysis_data,
        results,
    )



    
    VALIDATION = True  # Set to True to enable validation against Excel data

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
            dP_dt,
            a_amont,
        )



if __name__=="__main__":
    main()   