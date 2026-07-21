from constants import KLINKENBERG_ORDER_1_REF, KLINKENBERG_ORDER_2_REF, PERMEABILITY_REF
from data_loader import load_excel_adrien,extract_important_data
import numpy as np
from processors import LocalLinearRegressionProcessor, SavgolProcessor
from validation import validate_against_excel
from models import DarcyKlinkenbergModel


from plots import (
    plot_pressure_smoothing,
    plot_derivative_comparison, 
    plot_pressure_models,
    plot_apparent_permeability,
    plot_summary,
)

def main():
    raw_data=load_excel_adrien()
    analysis_data=extract_important_data(raw_data)  
    excel_model = DarcyKlinkenbergModel(analysis_data)

    darcy_model = DarcyKlinkenbergModel(
        analysis_data,
        permeability=PERMEABILITY_REF,
        b1=KLINKENBERG_ORDER_1_REF,
        b2=KLINKENBERG_ORDER_2_REF,
    )
     
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

    results_linreg2 = (
        LocalLinearRegressionProcessor()
        .process(
            analysis_data,
            darcy_model,
        )
    )

    
    all_ok = compare_results(
        results_linreg,
        results_linreg2,
    )

    print("\nGlobal check:", all_ok)




    

    results_savgol = (
        SavgolProcessor()
        .process(
            analysis_data,
            excel_model,
        )
    )      

    
    p_excel = excel_model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=1,
    )
    p_darcy = darcy_model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=1,
    )
    



    PLOT_SUMMARY = True  # Set to True to enable summary plotting
    if PLOT_SUMMARY:
        plot_summary(
            analysis_data,
            results_linreg,
        )
        plot_summary(
            analysis_data,
            results_savgol,
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
            results_linreg.dP_dt,
        )

    
    plot_derivative_comparison(
        analysis_data.time,
        dP_dt_dummy,
        results_linreg.dP_dt,
        results_savgol.dP_dt,
    )


def compare_results(
    results_ref,
    results_test,
):
    checks = {
        "p_amont_smooth": np.allclose(
            results_ref.p_amont_smooth,
            results_test.p_amont_smooth,
        ),
        "p_avale_smooth": np.allclose(
            results_ref.p_avale_smooth,
            results_test.p_avale_smooth,
        ),
        "p_apparent_smooth": np.allclose(
            results_ref.p_apparent_smooth,
            results_test.p_apparent_smooth,
        ),
        "dP_dt": np.allclose(
            results_ref.dP_dt,
            results_test.dP_dt,
        ),
        "k_apparent_exp": np.allclose(
            results_ref.k_apparent_exp,
            results_test.k_apparent_exp,
        ),
        "k_apparent_model": np.allclose(
            results_ref.k_apparent_model,
            results_test.k_apparent_model,
        ),
        "conductance_apparent": np.allclose(
            results_ref.conductance_apparent,
            results_test.conductance_apparent,
        ),
        "p_amont_ordre0": np.allclose(
            results_ref.p_amont_ordre0,
            results_test.p_amont_ordre0,
        ),
        "p_amont_ordre1": np.allclose(
            results_ref.p_amont_ordre1,
            results_test.p_amont_ordre1,
        ),
        "p_amont_ordre2": np.allclose(
            results_ref.p_amont_ordre2,
            results_test.p_amont_ordre2,
        ),
        "knudsen": np.allclose(
            results_ref.knudsen,
            results_test.knudsen,
        ),
    }

    print("\nResults comparison")
    print("-" * 40)

    for name, equal in checks.items():
        print(f"{name:<25} {equal}")

    print("-" * 40)

    return all(checks.values())


if __name__=="__main__":
    main()   