from data_loader import load_excel_2
import numpy as np
from optimization import DarcyKlinkenbergOptimizer
from processors import LocalPolynomialRegressionProcessor, SavgolProcessor
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

    results_regression_order1 = (
        LocalPolynomialRegressionProcessor(polyorder=1)
        .process(
            analysis_data,
            darcy_klinkenberg,
        )
    )
    results_regression_order2 = (
        LocalPolynomialRegressionProcessor(polyorder=2)
        .process(
            analysis_data,
            darcy_klinkenberg,
        )
    )
    results_regression_order3 = (
        LocalPolynomialRegressionProcessor(polyorder=3)
        .process(
            analysis_data,
            darcy_klinkenberg,
        )
    )

    check_savgol = False  # Set to True to skip Savgol processing
    if check_savgol:
        results_savgol = (
            SavgolProcessor()
            .process(
                analysis_data,
                darcy_klinkenberg,
            )
        )    
        dt = np.diff(analysis_data.time)

        print("dt min :", np.min(dt))
        print("dt mean:", np.mean(dt))
        print("dt max :", np.max(dt))

    


    plot_derivative_comparison(
        analysis_data.time,
        dP_dt_dummy,
        results_regression_order1,
        results_regression_order2,
        results_regression_order3,
    )

    plot_summary(
            analysis_data,
            results_regression_order1,
            title="Summary - order 1"
        )
    plot_summary(
            analysis_data,
            results_regression_order2,
            title="Summary - order 2"
        )
    plot_summary(
            analysis_data,
            results_regression_order3,
            title="Summary - order 3"
        )
    plt.show()



    

  




    








if __name__=="__main__":
    main()   