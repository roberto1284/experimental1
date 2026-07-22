from pathlib import Path
import pandas as pd
import numpy as np
from constants import (
    KLINKENBERG_ORDER_1_REF,
    KLINKENBERG_ORDER_2_REF,
    PERMEABILITY_REF,
)


def load_excel_check():
    local=Path(".")
    case=local/"Y SC 40 P2"
    for file in case.glob("Reproduction*.xlsx"):
        df_data = pd.read_excel(file,sheet_name=0,header=21,usecols="B:I,M:N,P:U")
        df_analyse = pd.read_excel(file,sheet_name=1,header=22,usecols="B:P")
    
    p_amont_ordre2_check=df_data["Pamont 1D visqueux + raréfié ordre 1 + raréfié ordre 2 [Pa]"].to_numpy()
    p_amont_ordre1_check=df_data["Pamont 1D visqueux + raréfié ordre 1 [Pa]"].to_numpy()
    p_amont_ordre0_check=df_data["Pamont 1D visqueux [Pa]"].to_numpy()

    
    a_amont_check=df_analyse["Interpolation linéaire a - Pamont [Pa/s]"].to_numpy()
    b_amont_check=df_analyse["Interpolation linéaire b - Pamont [Pa/s]"].to_numpy()
    p_amont_smooth_check=df_analyse["Pamont lissé [Pa]"].to_numpy()
    permeability_apparent_check=df_analyse["K_apparent [m²]"].to_numpy()
    conductance_apparent_check=df_analyse["Conductance apparente [m3/s]"].to_numpy()
    p_apparent_smooth_check=df_analyse["P_moyen apparente lissée [Pa]"].to_numpy()

    
    return {
        "p_amont_ordre0": p_amont_ordre0_check,
        "p_amont_ordre1": p_amont_ordre1_check,
        "p_amont_ordre2": p_amont_ordre2_check,
        "a_amont": a_amont_check,
        "b_amont": b_amont_check,
        "p_amont_smooth": p_amont_smooth_check,
        "p_apparent_smooth": p_apparent_smooth_check,
        "permeability_apparent": permeability_apparent_check,
        "conductance_apparent": conductance_apparent_check,
    }


def load_excel_check2():
    local=Path(".")
    case=local/"Y SC MOLECULAIRE"
    for file in case.glob("Reproduction*.xlsx"):
        df_data = pd.read_excel(file,sheet_name=0,header=21,usecols="B:I,M:N,P:U")
        df_analyse = pd.read_excel(file,sheet_name=1,header=22,usecols="B:P")
    
    p_amont_ordre2_check=df_data["Pamont 1D visqueux + raréfié ordre 1 + raréfié ordre 2 [Pa]"].to_numpy()
    p_amont_ordre1_check=df_data["Pamont 1D visqueux + raréfié ordre 1 [Pa]"].to_numpy()
    p_amont_ordre0_check=df_data["Pamont 1D visqueux [Pa]"].to_numpy()
    
    for i in range(5):
        print(
            f"{i:2d} | "
            f"O0={p_amont_ordre0_check[i]:12.6f} | "
            f"O1={p_amont_ordre1_check[i]:12.6f} | "
            f"O2={p_amont_ordre2_check[i]:12.6f}"
        )



    


    
    a_amont_check=df_analyse["Interpolation linéaire a - Pamont [Pa/s]"].to_numpy()
    b_amont_check=df_analyse["Interpolation linéaire b - Pamont [Pa/s]"].to_numpy()
    p_amont_smooth_check=df_analyse["Pamont lissé [Pa]"].to_numpy()
    permeability_apparent_check=df_analyse["K_apparent [m²]"].to_numpy()
    conductance_apparent_check=df_analyse["Conductance apparente [m3/s]"].to_numpy()
    p_apparent_smooth_check=df_analyse["P_moyen apparente lissée [Pa]"].to_numpy()

    
    return {
        "p_amont_ordre0": p_amont_ordre0_check,
        "p_amont_ordre1": p_amont_ordre1_check,
        "p_amont_ordre2": p_amont_ordre2_check,
        "a_amont": a_amont_check,
        "b_amont": b_amont_check,
        "p_amont_smooth": p_amont_smooth_check,
        "p_apparent_smooth": p_apparent_smooth_check,
        "permeability_apparent": permeability_apparent_check,
        "conductance_apparent": conductance_apparent_check,
    }



def validate_against_excel(
    results
):

    excel = load_excel_check()

    print("Check a:",
          np.allclose(results.dP_dt, excel["a_amont"]))



    print("Check P:",
          np.allclose(
              results.p_amont_smooth,
              excel["p_amont_smooth"]
          ))

    print("Check P apparent:",
          np.allclose(
              results.p_apparent_smooth,
              excel["p_apparent_smooth"]
          ))

    print("Check permeability:",
          np.allclose(
              results.k_apparent_exp,
              excel["permeability_apparent"]
          ))

    print("Check conductance:",
          np.allclose(
              results.conductance_apparent,
              excel["conductance_apparent"]
          ))
    
    print("Check P_amont ordre 0:",
          np.allclose(
              results.p_amont_ordre0,
              excel["p_amont_ordre0"]
          ))
    
    print("Check P_amont ordre 1:",
          np.allclose(
              results.p_amont_ordre1,
              excel["p_amont_ordre1"]
          ))


    
    print("Check P_amont ordre 2:",
          np.allclose(
              results.p_amont_ordre2,
              excel["p_amont_ordre2"]
          ))


def validate_against_excel2(
    results
):

    excel = load_excel_check2()

    print("Check a:",
          np.allclose(results.dP_dt, excel["a_amont"]))



    print("Check P:",
          np.allclose(
              results.p_amont_smooth,
              excel["p_amont_smooth"]
          ))

    print("Check P apparent:",
          np.allclose(
              results.p_apparent_smooth,
              excel["p_apparent_smooth"]
          ))

    print("Check permeability:",
          np.allclose(
              results.k_apparent_exp,
              excel["permeability_apparent"]
          ))

    print("Check conductance:",
          np.allclose(
              results.conductance_apparent,
              excel["conductance_apparent"]
          ))
    
    print("Check P_amont ordre 0:",
          np.allclose(
              results.p_amont_ordre0,
              excel["p_amont_ordre0"]
          ))
    
    print("Check P_amont ordre 1:",
          np.allclose(
              results.p_amont_ordre1,
              excel["p_amont_ordre1"]
          ))


    
    print("Check P_amont ordre 2:",
          np.allclose(
              results.p_amont_ordre2,
              excel["p_amont_ordre2"]
          ))


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


def check_optimization(optimizer):
    K_opt = optimizer.optimize_permeability()

    print("K optimized:", K_opt)
    
    cost_initial = optimizer.objective_permeability(
        PERMEABILITY_REF
    )

    cost_final = optimizer.objective_permeability(
        K_opt
    )

    
    print("cost_initial:", cost_initial)
    print("cost_final:", cost_final)
    b1_opt = optimizer.optimize_b1()

    print("b1 optimized:", b1_opt)

    cost_initial = optimizer.objective_b1(
        KLINKENBERG_ORDER_1_REF
    )

    cost_final = optimizer.objective_b1(
        b1_opt
    )

    print("b1 cost_initial:", cost_initial)
    print("b1 cost_final:", cost_final)

    b2_opt = optimizer.optimize_b2()

    print("b2 optimized:", b2_opt)

    cost_initial = optimizer.objective_b2(
        KLINKENBERG_ORDER_2_REF
    )

    cost_final = optimizer.objective_b2(
        b2_opt
    )

    print("b2 cost_initial:", cost_initial)
    print("b2 cost_final:", cost_final)