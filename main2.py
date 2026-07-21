from constants import KLINKENBERG_ORDER_1_REF, KLINKENBERG_ORDER_2_REF, PERMEABILITY_REF
from data_loader import load_excel_2, load_excel_adrien,extract_important_data
import numpy as np
from optimization import DarcyKlinkenbergOptimizer
from processors import LocalLinearRegressionProcessor, SavgolProcessor
from validation import validate_against_excel, compare_results, check_optimization
from models import DarcyKlinkenbergModel
import matplotlib.pyplot as plt


from plots import (
    plot_pressure_smoothing,
    plot_derivative_comparison, 
    plot_pressure_models,
    plot_apparent_permeability,
    plot_summary,
)

def main():
    analysis_data=load_excel_2()  # Call the revised function
    excel_model = DarcyKlinkenbergModel(analysis_data)

     
    dP_dt_dummy = np.gradient(
        analysis_data.pressure_amont,
        analysis_data.time,
    )

    results_linreg = (
        LocalLinearRegressionProcessor()
        .process(
            analysis_data,
            excel_model,
        )
    )


    '''
    all_ok = compare_results(
        results_linreg,
        results_linreg2,
    )
    print("\nGlobal check:", all_ok)

    '''
    

    results_savgol = (
        SavgolProcessor()
        .process(
            analysis_data,
            excel_model,
        )
    )      

    
    optimizer = DarcyKlinkenbergOptimizer(
        analysis_data
    )

    K_opt = optimizer.optimize_permeability()
    b1_opt = optimizer.optimize_b1()
    b2_opt = optimizer.optimize_b2()
    check_optimization(
        optimizer)
    




    darcy_model_opt = DarcyKlinkenbergModel(
        analysis_data,
        permeability=K_opt,
        b1=b1_opt,
        b2=b2_opt,
    )

    results_linreg_opt = (
        LocalLinearRegressionProcessor()
        .process(
            analysis_data,
            darcy_model_opt,
        )
    )
    results_savgol_opt = (
        SavgolProcessor()
        .process(
            analysis_data,
            darcy_model_opt,
        )
    )

  




    



    PLOT_SUMMARY = True  # Set to True to enable summary plotting
    if PLOT_SUMMARY:
        plot_summary(
            analysis_data,
            results_linreg,
            title="Summary - Excel"
        )
        plot_summary(
            analysis_data,
            results_savgol,
            title="Summary - Savitzky-Golay"
        )
        plot_summary(
            analysis_data,
            results_linreg_opt,
            title="Summary - Optimized Model"
        )
        plot_summary(
            analysis_data,
            results_savgol_opt,
            title="Summary - Optimized Savitzky-Golay"
        )
        plt.show()
    
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
            results_linreg.dP_dt,
        )

    
        plot_derivative_comparison(
            analysis_data.time,
            dP_dt_dummy,
            results_linreg.dP_dt,
            results_savgol.dP_dt,
        )





if __name__=="__main__":
    main()   