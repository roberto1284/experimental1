import numpy as np

from constants import (
    DYNAMIC_VISCOSITY,
    EPAISSEUR_ECHANTILLON,
    SECTION_PASSANTE,
    CYLINDER_SHAPE_FACTOR,
    V_AMONT,
    APPARENT_PRESSURE_FACTOR,
    KLINKENBERG_ORDER_1_REF,
    KLINKENBERG_ORDER_2_REF,
    PERMEABILITY_REF
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
    
    def pamont(
        self,
        p_amont,
        p_avale,
        dt,
        order,
    ):
        
        coef = (
            1 / V_AMONT
            * PERMEABILITY_REF
            / DYNAMIC_VISCOSITY
            * CYLINDER_SHAPE_FACTOR
            * SECTION_PASSANTE
            / EPAISSEUR_ECHANTILLON
        )

        term = 0.5 * (p_amont**2 - p_avale**2)

        if order >= 1:
            term += (
                KLINKENBERG_ORDER_1_REF
                * (p_amont - p_avale)
            )

        if order >= 2:
            term += (
                KLINKENBERG_ORDER_2_REF
                * np.log(p_amont / p_avale)
            )

        return p_amont - dt * coef * term
    
    
    def simulate_pamont(
        self,
        p_amont_0,
        p_avale,
        time,
        order,
    ):

        p_amont_simulated = [p_amont_0]

        for i in range(1, len(time)):

            dt = time[i] - time[i - 1]

            p_amont_next = self.pamont(
                p_amont_simulated[-1],
                p_avale[i - 1],
                dt,
                order,
            )

            p_amont_simulated.append(p_amont_next)

        return np.array(p_amont_simulated)

    





