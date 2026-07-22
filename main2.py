from data_loader import load_excel_2
import numpy as np
from optimization import DarcyKlinkenbergOptimizer
from processors import LocalLinearRegressionProcessor, SavgolProcessor
from validation import validate_against_excel, compare_results, check_optimization, validate_against_excel2
from models import DarcyKlinkenbergModel
import matplotlib.pyplot as plt
from validation import load_excel_check2
import constants2 as constants2


from plots import (
    plot_pressure_smoothing,
    plot_derivative_comparison, 
    plot_pressure_models,
    plot_apparent_permeability,
    plot_summary,
)

def main():
    analysis_data=load_excel_2()  # Call the revised function
    darcy_klinkenberg = DarcyKlinkenbergModel(analysis_data, constants2)

    MASK=False  # Set to True to apply the mask
    if MASK:

        mask = analysis_data.time >= 40        
        analysis_data.time = analysis_data.time[mask]
        analysis_data.pressure_amont = analysis_data.pressure_amont[mask]
        analysis_data.pressure_avale = analysis_data.pressure_avale[mask]
     
    dP_dt_dummy = np.gradient(
        analysis_data.pressure_amont,
        analysis_data.time,
    )

    results_excel = (
        LocalLinearRegressionProcessor()
        .process(
            analysis_data,
            darcy_klinkenberg,
        )
    )
    
    results_savgol = (
        SavgolProcessor()
        .process(
            analysis_data,
            darcy_klinkenberg,
        )
    )

    plot_derivative_comparison(
        analysis_data.time,
        dP_dt_dummy,
        results_excel.dP_dt,
        results_savgol.dP_dt,
    )



    

  




    








if __name__=="__main__":
    main()   