from pathlib import Path
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class ExperimentalData:
    time: np.ndarray
    pfeiffer1: np.ndarray
    pfeiffer2: np.ndarray
    agilent1: np.ndarray
    agilent2: np.ndarray
    temp1: np.ndarray
    temp2: np.ndarray
    temp_eprouvette: np.ndarray
    pressure_check_amont: np.ndarray
    pressure_check_avale: np.ndarray

#test hardcoded for now 

def load_excel_adrien():
    local=Path(".")
    case=local/"Y SC 40 P2"
    for file in case.glob("TRAITEMENT*.xlsx"):
        df = pd.read_excel(file)
        
    pfeiffer1 = df["Pfeiffer_P1 [mbar]"].to_numpy()
    pfeiffer2 = df["Pfeiffer_P2 [mbar]"].to_numpy()
    agilent1 = df["Agilent_P1 [mbar]"].to_numpy()
    agilent2 = df["Agilent_P2 [mbar]"].to_numpy()
    temp1 = df["Temp_P1 [ｰC]"].to_numpy()
    temp2 = df["Temp_P2 [ｰC]"].to_numpy()
    temp_eprouvette = df["Temp_Eprouvette [ｰC]"].to_numpy()

    time=np.arange(len(pfeiffer1))  #i noticed that all the measurements are exactly separated by 1sec, check each case prolly


    pressure_check_amont = df["P_amont [Pa]"].to_numpy()
    pressure_check_avale = df["P_avale [Pa]"].to_numpy()

    return ExperimentalData(
        time=time,
        pfeiffer1=pfeiffer1,
        pfeiffer2=pfeiffer2,
        agilent1=agilent1,
        agilent2=agilent2,
        temp1=temp1,
        temp2=temp2,
        temp_eprouvette=temp_eprouvette,
        pressure_check_amont=pressure_check_amont,
        pressure_check_avale=pressure_check_avale,
    )

def capteur_selector(pf1,pf2,ag1,ag2):
    P_amont = []
    P_avale = []
    i=0
    for value in pf1:
        if value > 10:
            P_amont.append(value*100)
        else:
            P_amont.append(ag1[i]*100)
        i+=1
    i=0
    for value in pf2:
        if value > 10:
            P_avale.append(value*100)
        else:
            P_avale.append(ag2[i]*100)
        i+=1
    P_amont = np.array(P_amont)
    P_avale = np.array(P_avale)
    return P_amont, P_avale    



def main():
    data=load_excel_adrien()
    P_amont,P_avale=capteur_selector(data.pfeiffer1,data.pfeiffer2,data.agilent1,data.agilent2)
    
    print(np.allclose(P_amont, data.pressure_check_amont))
    print(np.allclose(P_avale, data.pressure_check_avale))


    

if __name__=="__main__":
    main()



   