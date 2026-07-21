#test hardcoded for now 
from pathlib import Path
from experimental_data import AnalysisData,ExperimentalData
import numpy as np
import pandas as pd

def load_excel_adrien():
    local=Path(".")
    case=local/"Y SC 40 P2"
    for file in case.glob("TRAITEMENT*.xlsx"):
        df = pd.read_excel(file)
        
    pfeiffer_amont = df["Pfeiffer_P1 [mbar]"].to_numpy()
    pfeiffer_avale = df["Pfeiffer_P2 [mbar]"].to_numpy()
    agilent_amont = df["Agilent_P1 [mbar]"].to_numpy()
    agilent_avale = df["Agilent_P2 [mbar]"].to_numpy()
    temp_amont = df["Temp_P1 [ｰC]"].to_numpy()+273.15
    temp_avale = df["Temp_P2 [ｰC]"].to_numpy()+273.15
    temp_eprouvette = df["Temp_Eprouvette [ｰC]"].to_numpy()+273.15

    time=np.arange(len(pfeiffer_amont))  #i noticed that all the measurements are exactly separated by 1sec, check each case prolly


    pressure_check_amont = df["P_amont [Pa]"].to_numpy()
    pressure_check_avale = df["P_avale [Pa]"].to_numpy()

    return ExperimentalData(
        time=time,
        pfeiffer_amont=pfeiffer_amont,
        pfeiffer_avale=pfeiffer_avale,
        agilent_amont=agilent_amont,
        agilent_avale=agilent_avale,
        temp_amont=temp_amont,
        temp_avale=temp_avale,
        temp_eprouvette=temp_eprouvette,
        pressure_check_amont=pressure_check_amont,
        pressure_check_avale=pressure_check_avale,
    )

def load_excel_2():
    local=Path(".")
    case=local/"Y SC MOLECULAIRE"
    for file in case.glob("Reproduction*.xlsx"):
        df_data = pd.read_excel(file,sheet_name=0,header=21,usecols="B:I,M:N,P:U")
        df_analyse = pd.read_excel(file,sheet_name=1,header=22,usecols="B:P")
    


    time=df_data["t [s]"].to_numpy()
    pressure_amont=df_data["Pamont exp [Pa]"].to_numpy()
    pressure_avale=df_data["Paval exp [Pa]"].to_numpy()
    
    
    return AnalysisData(
        time=time, 
        pressure_amont=pressure_amont, 
        pressure_avale=pressure_avale, 
        temp_moyenne_global=np.zeros_like(time)  # Placeholder, replace with actual temperature data if available
    )

def extract_important_data(raw_data):
    pressure_amont,pressure_avale=capteur_selector(raw_data.pfeiffer_amont,raw_data.pfeiffer_avale,raw_data.agilent_amont,raw_data.agilent_avale)

    
    assert np.allclose(pressure_amont, raw_data.pressure_check_amont)  #use assert maybe
    assert np.allclose(pressure_avale, raw_data.pressure_check_avale)

    temp_amont_moyenne=np.mean(raw_data.temp_amont)
    temp_avale_moyenne=np.mean(raw_data.temp_avale)
    temp_eprouvette_moyenne=np.mean(raw_data.temp_eprouvette)

    temp_moyenne_global=np.mean([temp_amont_moyenne,temp_avale_moyenne,temp_eprouvette_moyenne])

    return AnalysisData(
        time=raw_data.time, pressure_amont=pressure_amont, pressure_avale=pressure_avale, temp_moyenne_global=temp_moyenne_global)


def capteur_selector(pf1,pf2,ag1,ag2):
    pressure_amont = []
    pressure_avale = []
    i=0
    for value in pf1:
        if value > 10:
            pressure_amont.append(value*100)
        else:
            pressure_amont.append(ag1[i]*100)
        i+=1
    i=0
    for value in pf2:
        if value > 10:
            pressure_avale.append(value*100)
        else:
            pressure_avale.append(ag2[i]*100)
        i+=1
    pressure_amont = np.array(pressure_amont)
    pressure_avale = np.array(pressure_avale)
    return pressure_amont, pressure_avale    
