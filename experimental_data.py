from dataclasses import dataclass
import numpy as np
@dataclass
class ExperimentalData:
    time: np.ndarray
    pfeiffer_amont: np.ndarray
    pfeiffer_avale: np.ndarray
    agilent_amont: np.ndarray
    agilent_avale: np.ndarray
    temp_amont: np.ndarray
    temp_avale: np.ndarray
    temp_eprouvette: np.ndarray
    pressure_check_amont: np.ndarray
    pressure_check_avale: np.ndarray


@dataclass
class AnalysisData:

    time: np.ndarray

    pressure_amont: np.ndarray
    pressure_avale: np.ndarray

    temp_moyenne_global: float

@dataclass
class Results:

    p_amont_smooth: np.ndarray
    p_avale_smooth: np.ndarray

    p_apparent_smooth: np.ndarray

    k_apparent_exp: np.ndarray
    k_apparent_model: np.ndarray

    conductance_apparent: np.ndarray

    p_amont_ordre0: np.ndarray
    p_amont_ordre1: np.ndarray
    p_amont_ordre2: np.ndarray

    knudsen: np.ndarray
    dP_dt: np.ndarray

    
    viscous_mask: np.ndarray
    slip_mask: np.ndarray
    transition_mask: np.ndarray
    free_molecular_mask: np.ndarray
    method: str
