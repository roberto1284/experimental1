from experimental_data import Results


def build_results(
    analysis_data,
    model,
    p_amont_smooth,
    p_avale_smooth,
    dP_dt,
    method,
):

    p_apparent_smooth = model.apparent_pressure(
        p_amont_smooth,
        p_avale_smooth,
    )

    k_apparent_exp = (
        model.apparent_permeability_experimental(
            dP_dt,
            p_amont_smooth,
            p_avale_smooth,
        )
    )

    conductance_apparent = (
        model.apparent_conductance(
            k_apparent_exp,
            p_apparent_smooth,
        )
    )

    p_amont_ordre0 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=0,
    )

    p_amont_ordre1 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=1,
    )

    p_amont_ordre2 = model.simulate_pamont(
        analysis_data.pressure_amont[0],
        analysis_data.pressure_avale,
        analysis_data.time,
        order=2,
    )

    k_apparent_model = (
        model.apparent_permeability_model(
            p_apparent_smooth,
        )
    )

    knudsen = model.knudsen_number(
        p_apparent_smooth,
        characteristic_length=300e-6,
    )

    viscous_mask = knudsen < 0.01

    slip_mask = (
        (knudsen >= 0.01)
        & (knudsen < 0.1)
    )

    transition_mask = (
        (knudsen >= 0.1)
        & (knudsen < 10)
    )

    free_molecular_mask = knudsen >= 10

    return Results(
        p_amont_smooth=p_amont_smooth,
        p_avale_smooth=p_avale_smooth,
        p_apparent_smooth=p_apparent_smooth,
        k_apparent_exp=k_apparent_exp,
        k_apparent_model=k_apparent_model,
        conductance_apparent=conductance_apparent,
        p_amont_ordre0=p_amont_ordre0,
        p_amont_ordre1=p_amont_ordre1,
        p_amont_ordre2=p_amont_ordre2,
        knudsen=knudsen,
        viscous_mask=viscous_mask,
        slip_mask=slip_mask,
        transition_mask=transition_mask,
        free_molecular_mask=free_molecular_mask,
        dP_dt=dP_dt,
        method=method,
    )