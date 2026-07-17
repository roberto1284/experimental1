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