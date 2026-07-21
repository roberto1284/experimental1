import numpy as np

from constants import (
    DYNAMIC_VISCOSITY,
    EPAISSEUR_ECHANTILLON,
    R_GAS,
    REFERENCE_TEMPERATURE,
    SECTION_PASSANTE,
    CYLINDER_SHAPE_FACTOR,
    V_AMONT,
    APPARENT_PRESSURE_FACTOR,
    KLINKENBERG_ORDER_1_REF,
    KLINKENBERG_ORDER_2_REF,
    PERMEABILITY_REF
)


class DarcyKlinkenbergModel:

    def __init__(
        self,
        analysis_data,
        permeability=PERMEABILITY_REF,
        b1=KLINKENBERG_ORDER_1_REF,
        b2=KLINKENBERG_ORDER_2_REF,
    ):

        self.data = analysis_data
        self.permeability = permeability
        self.b1 = b1
        self.b2 = b2
    
    def apparent_pressure(
        self,
        p_amont_smooth,
        p_avale_smooth,
    ):

        return (
            APPARENT_PRESSURE_FACTOR * p_amont_smooth
            + (1 - APPARENT_PRESSURE_FACTOR) * p_avale_smooth
        )

    def apparent_permeability_model(
        self,
        p_amont_smooth,
    ):

        return (
            self.permeability
            * (1 + self.b1 / p_amont_smooth + self.b2 / (p_amont_smooth**2))
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
    
    def knudsen_number(
        self,
        pressure,
        characteristic_length,
    ):
        
        mean_free_path = (
                DYNAMIC_VISCOSITY
                / (
                    pressure
                    / R_GAS
                    / REFERENCE_TEMPERATURE
                )
                / np.sqrt(
                    R_GAS
                    * REFERENCE_TEMPERATURE
                )
            )

        return mean_free_path / characteristic_length
    
    def pressure_amont(
            self,
            p_amont,
            p_avale,
            dt,
            order,           
    ):
        coef = (
            1 / V_AMONT
            * self.permeability
            / DYNAMIC_VISCOSITY
            * CYLINDER_SHAPE_FACTOR
            * SECTION_PASSANTE
            / EPAISSEUR_ECHANTILLON
        )

        term = 0.5 * (p_amont**2 - p_avale**2)

        if order >= 1:
            term += (
                self.b1
                * (p_amont - p_avale)
            )

        if order >= 2:
            term += (
                self.b2
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

            p_amont_next = self.pressure_amont(
                p_amont_simulated[-1],
                p_avale[i - 1],
                dt,
                order,
            )

            p_amont_simulated.append(p_amont_next)

        return np.array(p_amont_simulated)
    
    def apparent_permeability_experimental(
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
    def model_errors(
        self,
        pressure_exp,
        pressure_model,
    ):

        return {
            "viscous": np.abs(
                pressure_exp**2
                - pressure_model**2
            ),

            "rarefaction_order_1": np.abs(
                pressure_exp
                - pressure_model
            ),

            "rarefaction_order_2": np.abs(
                np.log(
                    pressure_exp
                    / pressure_model
                )
            ),

            "absolute": (
                np.abs(
                    pressure_exp
                    - pressure_model
                )
                / pressure_exp
            ),
        }


    
    
    
    


    
       

    





