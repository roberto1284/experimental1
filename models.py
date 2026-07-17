import numpy as np

from constants import (
    DYNAMIC_VISCOSITY,
    EPAISSEUR_ECHANTILLON,
    SECTION_PASSANTE,
    CYLINDER_SHAPE_FACTOR,
    V_AMONT,
    APPARENT_PRESSURE_FACTOR,
)


class ExcelAdrien:

    def __init__(self, analysis_data):

        self.data = analysis_data

    def local_linear_regression(
        self,
        pressure,
        half_window=126,
    ):

        a_array = []
        b_array = []

        time = self.data.time
        N = len(time)

        for i in range(N):

            start = max(i - half_window, 0)
            end = min(i + half_window + 1, N)

            t = time[start:end]
            P = pressure[start:end]

            a, b = np.polyfit(t, P, 1)

            a_array.append(a)
            b_array.append(b)

        a_array = np.array(a_array)
        b_array = np.array(b_array)

        pressure_smooth = a_array * time + b_array

        return a_array, b_array, pressure_smooth

    def apparent_pressure(
        self,
        p_amont_smooth,
        p_avale_smooth,
    ):

        return (
            APPARENT_PRESSURE_FACTOR * p_amont_smooth
            + (1 - APPARENT_PRESSURE_FACTOR) * p_avale_smooth
        )

    def apparent_permeability(
        self,
        a_amont,
        p_amont_smooth,
        p_avale_smooth,
    ):

        return (
            np.abs(a_amont)
            * V_AMONT
            * DYNAMIC_VISCOSITY
            * EPAISSEUR_ECHANTILLON
            / SECTION_PASSANTE
            / CYLINDER_SHAPE_FACTOR
            / (
                0.5
                * (
                    p_amont_smooth**2
                    - p_avale_smooth**2
                )
            )
        )

    def apparent_conductance(
        self,
        permeability_apparent,
        p_apparent_smooth,
    ):

        return (
            SECTION_PASSANTE
            * permeability_apparent
            * p_apparent_smooth
            / DYNAMIC_VISCOSITY
            / EPAISSEUR_ECHANTILLON
        )