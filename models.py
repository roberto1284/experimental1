import numpy as np

class DarcyKlinkenbergModel:

    def __init__(
        self,
        analysis_data,
        constants,
        permeability=None,
        b1=None,
        b2=None,
    ):

        self.data = analysis_data
        self.constants = constants

        self.permeability = (
            permeability
            if permeability is not None
            else constants.PERMEABILITY_REF
        )

        self.b1 = (
            b1
            if b1 is not None
            else constants.KLINKENBERG_ORDER_1_REF
        )

        self.b2 = (
            b2
            if b2 is not None
            else constants.KLINKENBERG_ORDER_2_REF
        )

    
    def apparent_pressure(
        self,
        p_amont_smooth,
        p_avale_smooth,
    ):

        return (
            self.constants.APPARENT_PRESSURE_FACTOR * p_amont_smooth
            + (1 - self.constants.APPARENT_PRESSURE_FACTOR) * p_avale_smooth
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
            self.constants.SECTION_PASSANTE
            * permeability_apparent
            * p_apparent_smooth
            / self.constants.DYNAMIC_VISCOSITY
            / self.constants.EPAISSEUR_ECHANTILLON
        )
    
    def knudsen_number(
        self,
        pressure,
        characteristic_length,
    ):
        
        mean_free_path = (
                self.constants.DYNAMIC_VISCOSITY
                / (
                    pressure
                    / self.constants.R_GAS
                    / self.constants.REFERENCE_TEMPERATURE
                )
                / np.sqrt(
                    self.constants.R_GAS
                    * self.constants.REFERENCE_TEMPERATURE
                )
            )

        return mean_free_path / characteristic_length
    
    def compute_next_pressure_amont(
            self,
            p_amont,
            p_avale,
            dt,
            order,           
    ):
        coef = (
            1 / self.constants.V_AMONT
            * self.permeability
            / self.constants.DYNAMIC_VISCOSITY
            * self.constants.CYLINDER_SHAPE_FACTOR
            * self.constants.SECTION_PASSANTE
            / self.constants.EPAISSEUR_ECHANTILLON
        )

        term = 0.5 * (p_amont**2 - p_avale**2)

        if order >= 1:
            term += (
                self.b1
                * (p_amont - p_avale)
            )
            
        if order >= 2:
            #print(f"p_amont: {p_amont}, p_avale: {p_avale}")
            term += (
                self.b2
                * np.log(p_amont / p_avale)
            )

        return p_amont - dt * coef * term
    
    def simulate_pression_amont(
        self,
        p_amont_0,
        p_avale,
        time,
        order,
    ):
        #print(f"Initial p_amont: {p_amont_0}")

        p_amont_simulated = [p_amont_0]

        for i in range(1, len(time)):

            dt = time[i] - time[i - 1]
            
          

            p_amont_next = self.compute_next_pressure_amont(
                p_amont_simulated[-1],
                p_avale[i - 1],
                dt,
                order,
            )
            DEPURE = False

            if DEPURE==True:

                if i in [1, 2, 3, 4, 5]:  # Print for the first few time steps
                    print(f"Time step {i}: dt = {dt}, p_avale = {p_avale[i]}")
                    print(f"Computed p_amont: {p_amont_next}")

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
            * self.constants.V_AMONT
            * self.constants.DYNAMIC_VISCOSITY
            * self.constants.EPAISSEUR_ECHANTILLON
            / self.constants.SECTION_PASSANTE
            / self.constants.CYLINDER_SHAPE_FACTOR
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


    
    
    
    


    
       

    





