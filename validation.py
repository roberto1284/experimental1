from pathlib import Path
import pandas as pd
import numpy as np

def load_excel_check():
    local=Path(".")
    case=local/"Y SC 40 P2"
    for file in case.glob("Reproduction*.xlsx"):
        df_data = pd.read_excel(file,sheet_name=0,header=21,usecols="B:I,M:N,P:U")
        df_analyse = pd.read_excel(file,sheet_name=1,header=22,usecols="B:P")
    
    p_amont_ordre2_check=df_data["Pamont 1D visqueux + raréfié ordre 1 + raréfié ordre 2 [Pa]"].to_numpy()


    
    a_amont_check=df_analyse["Interpolation linéaire a - Pamont [Pa/s]"].to_numpy()
    b_amont_check=df_analyse["Interpolation linéaire b - Pamont [Pa/s]"].to_numpy()
    p_amont_smooth_check=df_analyse["Pamont lissé [Pa]"].to_numpy()
    permeability_apparent_check=df_analyse["K_apparent [m²]"].to_numpy()
    conductance_apparent_check=df_analyse["Conductance apparente [m3/s]"].to_numpy()
    p_apparent_smooth_check=df_analyse["P_moyen apparente lissée [Pa]"].to_numpy()

    
    return {
        "p_amont_ordre2": p_amont_ordre2_check,
        "a_amont": a_amont_check,
        "b_amont": b_amont_check,
        "p_amont_smooth": p_amont_smooth_check,
        "p_apparent_smooth": p_apparent_smooth_check,
        "permeability_apparent": permeability_apparent_check,
        "conductance_apparent": conductance_apparent_check,
    }



def validate_against_excel(
    p_amont_ordre2,
    a_amont,
    b_amont,
    p_amont_smooth,
    p_apparent_smooth,
    permeability_apparent,
    conductance_apparent,
):

    excel = load_excel_check()

    print("Check a:",
          np.allclose(a_amont, excel["a_amont"]))

    print("Check b:",
          np.allclose(b_amont, excel["b_amont"]))

    print("Check P:",
          np.allclose(
              p_amont_smooth,
              excel["p_amont_smooth"]
          ))

    print("Check P apparent:",
          np.allclose(
              p_apparent_smooth,
              excel["p_apparent_smooth"]
          ))

    print("Check permeability:",
          np.allclose(
              permeability_apparent,
              excel["permeability_apparent"]
          ))

    print("Check conductance:",
          np.allclose(
              conductance_apparent,
              excel["conductance_apparent"]
          ))
    
    print("Check P_amont ordre 2:",
          np.allclose(
              p_amont_ordre2,
              excel["p_amont_ordre2"]
          ))
