import matplotlib.pyplot as plt
import numpy as np
def plot_pressure_smoothing(
    time,
    pressure_raw,
    pressure_smooth,
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        time,
        pressure_raw,
        label="Pamont raw",
    )

    plt.plot(
        time,
        pressure_smooth,
        label="Pamont smooth",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Pressure [Pa]")

    plt.legend()
    plt.grid()

    plt.show()


def plot_derivative_comparison(
    time,
    derivative_dummy,    
    *results,
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        time,
        derivative_dummy,
        alpha=0.5,
        linewidth=0.5,
        label="Raw derivative",
    )

    for result in results:

        plt.plot(
            result.time,      # <- tiempo propio del resultado
            result.dP_dt,
            linewidth=2,
            label=result.method,
        )

    plt.xlabel("Time [s]")
    plt.ylabel("dP/dt [Pa/s]")
    plt.xscale("log")

    plt.legend()
    plt.grid()





def plotting(x,name_x,y,name_y):
    plt.plot(
    x,y
    )

    plt.xlabel(name_x)
    plt.ylabel(name_y)
    plt.grid()

    plt.show()


def plot_pressure_models(
    time,
    pressure_exp,
    pressure_order0,
    pressure_order1,
    pressure_order2,
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        time,
        pressure_exp,
        label="Experimental",
        linewidth=2,
    )

    plt.plot(
        time,
        pressure_order0,
        label="Darcy (order 0)",
    )

    plt.plot(
        time,
        pressure_order1,
        label="Klinkenberg order 1",
    )

    plt.plot(
        time,
        pressure_order2,
        label="Klinkenberg order 2",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Pressure [Pa]")

    plt.legend()
    plt.grid()

    plt.show()


def plot_apparent_permeability(
    time,
    pressure,
    k_app_exp,
    k_app_model,
):

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10, 10),
        constrained_layout=True,
    )

    # Kapp vs pressure

    axes[0].plot(
        pressure,
        k_app_exp,
        label="Experimental",
    )

    axes[0].plot(
        pressure,
        k_app_model,
        label="Model",
    )

    axes[0].set_xlabel("Apparent pressure [Pa]")
    axes[0].set_ylabel("Apparent permeability [m²]")
    axes[0].set_title("Kapp vs apparent pressure")

    axes[0].grid()
    axes[0].legend()

    # Kapp vs time

    axes[1].plot(
        time,
        k_app_exp,
        label="Experimental",
    )

    axes[1].plot(
        time,
        k_app_model,
        label="Model",
    )

    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Apparent permeability [m²]")
    axes[1].set_title("Kapp vs time")

    axes[1].grid()
    axes[1].legend()

    plt.show()

def add_knudsen_regions(ax, x, mask, color, label):
    """
    Add translucent colored regions to a plot.
    """

    start = None

    for i, active in enumerate(mask):

        if active and start is None:
            start = i

        elif not active and start is not None:

            ax.axvspan(
                x[start],
                x[i - 1],
                color=color,
                alpha=0.15,
                label=label,
            )

            start = None
            label = None

    if start is not None:

        ax.axvspan(
            x[start],
            x[-1],
            color=color,
            alpha=0.15,
            label=label,
        )

def add_all_knudsen_regions(ax, x, results):

    add_knudsen_regions(
        ax,
        x,
        results.viscous_mask,
        "tab:blue",
        "Viscous",
    )

    add_knudsen_regions(
        ax,
        x,
        results.slip_mask,
        "tab:green",
        "Slip",
    )

    add_knudsen_regions(
        ax,
        x,
        results.transition_mask,
        "tab:orange",
        "Transition",
    )

    add_knudsen_regions(
        ax,
        x,
        results.free_molecular_mask,
        "tab:red",
        "Free molecular",
    )

def plot_summary(
    analysis_data,
    results,
    title="Summary"
):

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 10),
        constrained_layout=True,
    )
    fig.suptitle(title, fontsize=16)

    # ==========================================================
    # Pamont models
    # ==========================================================

    add_all_knudsen_regions(
        axes[0, 0],
        analysis_data.time,
        results,
    )

    axes[0, 0].plot(
        analysis_data.time,
        analysis_data.pressure_amont,
        label="Experimental",
        linewidth=2,
    )

    axes[0, 0].plot(
        analysis_data.time,
        results.p_amont_ordre0,
        label="Vicous (order 0)",
    )

    axes[0, 0].plot(
        analysis_data.time,
        results.p_amont_ordre1,
        label="Viscous + rarefaction (order 1)",
    )

    axes[0, 0].plot(
        analysis_data.time,
        results.p_amont_ordre2,
        label="Viscous + rarefaction (order 1+2)",
        linestyle="--",
    )

    axes[0, 0].set_title("Pamont model comparison")
    axes[0, 0].set_xlabel("Time [s]")
    axes[0, 0].set_ylabel("Pressure [Pa]")
    axes[0, 0].set_yscale("log")
    axes[0, 0].grid()
    axes[0, 0].legend()

    # ==========================================================
    # Kapp vs apparent pressure
    # ==========================================================

    axes[0, 1].plot(
        results.p_apparent_smooth[results.viscous_mask],
        results.k_apparent_exp[results.viscous_mask],
        ".",
        color="tab:blue",
        label="Viscous",
    )

    axes[0, 1].plot(
        results.p_apparent_smooth[results.slip_mask],
        results.k_apparent_exp[results.slip_mask],
        ".",
        color="tab:green",
        label="Slip",
    )

    axes[0, 1].plot(
        results.p_apparent_smooth[results.transition_mask],
        results.k_apparent_exp[results.transition_mask],
        ".",
        color="tab:orange",
        label="Transition",
    )

    axes[0, 1].plot(
        results.p_apparent_smooth[results.free_molecular_mask],
        results.k_apparent_exp[results.free_molecular_mask],
        ".",
        color="tab:red",
        label="Free molecular",
    )

    axes[0, 1].plot(
        results.p_apparent_smooth,
        results.k_apparent_model,
        color="black",
        linewidth=2,
        label="K_app_model",
    )
    axes[0, 1].plot(
        results.p_apparent_smooth,
        results.k_recalee_apparent,
        ".",
        markersize=2,
        color="black",
        label="K_app_recalée",
    )

    axes[0, 1].set_title("Kapp vs apparent pressure")
    axes[0, 1].set_xlabel("Apparent pressure [Pa]")
    axes[0, 1].set_ylabel("Apparent permeability [m²]")
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_xscale("log")
    axes[0, 1].invert_xaxis()  # Invert x-axis for better visualization
    axes[0, 1].grid()
    axes[0, 1].legend()

    # ==========================================================
    # P apparent vs time
    # ==========================================================

    add_all_knudsen_regions(
        axes[1, 0],
        analysis_data.time,
        results,
    )

    axes[1, 0].plot(
        analysis_data.time,
        results.p_apparent_smooth,
        color="black",
        linewidth=2,
        label="P apparent smooth",
    )

    axes[1, 0].plot(
        analysis_data.time,
        results.p_amont_smooth,
        color="tab:blue",
        linewidth=2,
        label="Pamont smooth",
    )
    axes[1, 0].plot(
        analysis_data.time,
        results.p_avale_smooth,
        color="tab:orange",
        linewidth=2,
        label="Pavale smooth",
    )
    axes[1, 0].plot(
        analysis_data.time,
        analysis_data.pressure_amont,
        ".",
        color="tab:blue",
        alpha=0.7,
        markersize=4,
        label="Pamont raw",
    )
    axes[1, 0].plot(
        analysis_data.time,
        analysis_data.pressure_avale,   
        ".",
        color="tab:orange",
        alpha=0.7,
        markersize=4,
        label="Pavale raw",
    )


    axes[1, 0].set_title("Pressures vs time")
    axes[1, 0].set_xlabel("Time [s]")
    axes[1, 0].set_ylabel("Pressure [Pa]")
    axes[1, 0].set_yscale("log")
    axes[1, 0].grid()
    axes[1, 0].legend()

    # ==========================================================
    # Kapp vs time
    # ==========================================================

    add_all_knudsen_regions(
        axes[1, 1],
        analysis_data.time,
        results,
    )

    axes[1, 1].plot(
        analysis_data.time,
        results.k_apparent_exp,
        label="Experimental",
    )

    axes[1, 1].plot(
        analysis_data.time,
        results.k_apparent_model,
        label="Model",
    )

    axes[1, 1].set_title("Kapp vs time")
    axes[1, 1].set_xlabel("Time [s]")
    axes[1, 1].set_ylabel("Apparent permeability [m²]")
    axes[1, 1].grid()
    axes[1, 1].legend()
