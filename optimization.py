import numpy as np

from scipy.optimize import least_squares,minimize, minimize_scalar

from models import DarcyKlinkenbergModel

from constants import (
    PERMEABILITY_REF,
    KLINKENBERG_ORDER_1_REF,
    KLINKENBERG_ORDER_2_REF,
)



class DarcyKlinkenbergOptimizer:

    def __init__(
        self,
        analysis_data,
        initial_guess=None,
    ):
        self.data = analysis_data
        
        

        
        reference_model = DarcyKlinkenbergModel(
            self.data,
            PERMEABILITY_REF,
            KLINKENBERG_ORDER_1_REF,
            KLINKENBERG_ORDER_2_REF,
        )

        p_reference = reference_model.simulate_pression_amont(
            self.data.pressure_amont[0],
            self.data.pressure_avale,
            self.data.time,
            order=2,
        )

        reference_errors = reference_model.model_errors(
            self.data.pressure_amont,
            p_reference,
        )

        self.viscous_ref = np.mean(
            reference_errors["viscous"]
        )

        self.order1_ref = np.mean(
            reference_errors["rarefaction_order_1"]
        )

        self.order2_ref = np.mean(
            reference_errors["rarefaction_order_2"]
        )       

        
        self.initial_guess = (
            initial_guess
            if initial_guess is not None
            else [
                PERMEABILITY_REF,
                KLINKENBERG_ORDER_1_REF,
                KLINKENBERG_ORDER_2_REF,
            ]
        )

        self.permeability = self.initial_guess[0]
        self.b1 = self.initial_guess[1]
        self.b2 = self.initial_guess[2]

    def objective_permeability(
        self,
        permeability,
    ):

        model = DarcyKlinkenbergModel(
            self.data,
            permeability,
            self.b1,
            self.b2,
        )

        p_model = model.simulate_pression_amont(
            self.data.pressure_amont[0],
            self.data.pressure_avale,
            self.data.time,
            order=2,
        )

        

        if np.any(p_model <= 0):
            return 1e30

        if not np.all(np.isfinite(p_model)):
            return 1e30
        
        errors = model.model_errors(
            self.data.pressure_amont,
            p_model,
        )

        return np.mean(
            errors["viscous"]
        )     
    
    
    def optimize_permeability(self):
        
        result = minimize_scalar(
                self.objective_permeability,
                bounds=(0.1*PERMEABILITY_REF, 10*PERMEABILITY_REF),
                method="bounded",
                options={"xatol": 1e-16, "maxiter": 1000},
            )

        print(result)
        self.permeability = result.x
        return result.x
    

    def objective_b1(
        self,
        b1,
    ):

        model = DarcyKlinkenbergModel(
            self.data,
            self.permeability,
            b1,
            self.b2,
        )

        p_model = model.simulate_pression_amont(
            self.data.pressure_amont[0],
            self.data.pressure_avale,
            self.data.time,
            order=2,
        )

        if np.any(p_model <= 0):
            return 1e30

        if not np.all(np.isfinite(p_model)):
            return 1e30

        errors = model.model_errors(
            self.data.pressure_amont,
            p_model,
        )

        return np.mean(
            errors["rarefaction_order_1"]
        )


    def optimize_b1(self):

        result = minimize_scalar(
            self.objective_b1,
            bounds=(
                0.1 * KLINKENBERG_ORDER_1_REF,
                10 * KLINKENBERG_ORDER_1_REF,
            ),
            method="bounded",
            options={"maxiter": 1000},
        )

        print(result)

        self.b1 = result.x

        return result.x
    
    def objective_b2(
        self,
        b2,
    ):

        model = DarcyKlinkenbergModel(
            self.data,
            self.permeability,
            self.b1,
            b2,
        )

        p_model = model.simulate_pression_amont(
            self.data.pressure_amont[0],
            self.data.pressure_avale,
            self.data.time,
            order=2,
        )

        if np.any(p_model <= 0):
            return 1e30

        if not np.all(np.isfinite(p_model)):
            return 1e30

        errors = model.model_errors(
            self.data.pressure_amont,
            p_model,
        )

        return np.mean(
            errors["rarefaction_order_2"]
        )


    def optimize_b2(self):

        result = minimize_scalar(
            self.objective_b2,
            bounds=(
                0.1 * KLINKENBERG_ORDER_2_REF,
                10 * KLINKENBERG_ORDER_2_REF,
            ),
            method="bounded",
            options={"maxiter": 1000},
        )

        print(result)

        self.b2 = result.x

        return result.x




    
    def objective(
        self,
        params,
    ):

        permeability, b1, b2 = params

        model = DarcyKlinkenbergModel(
            self.data,
            permeability,
            b1,
            b2,
        )

        p_model = model.simulate_pression_amont(
            self.data.pressure_amont[0],
            self.data.pressure_avale,
            self.data.time,
            order=2,
        )

        if np.any(p_model <= 0):
            return 1e30
        
        if not np.all(np.isfinite(p_model)):
            return 1e30        



        errors = model.model_errors(
            self.data.pressure_amont,
            p_model,
        )
        DEPURE = False
        if DEPURE==True:            
            print(np.mean(errors["viscous"]))
            print(np.mean(errors["rarefaction_order_1"]))
            print(np.mean(errors["rarefaction_order_2"]))
            print("--------------------")
        

        cost = (
            np.mean(errors["viscous"]) / self.viscous_ref
            + np.mean(errors["rarefaction_order_1"]) / self.order1_ref
            + np.mean(errors["rarefaction_order_2"]) / self.order2_ref
        )



        return cost
    
    def fit(
        self,
    ):

        result = minimize(
            self.objective,
            x0=self.initial_guess,            
            bounds=[
                    (1e-20, None),
                    (0, None),
                    (0, None),
                ],

            #method="Nelder-Mead",
        )

        return{
            "permeability": result.x[0],
            "b1": result.x[1],
            "b2": result.x[2],
            "cost": result.fun,
            "success": result.success,
            "result": result,
        }



        