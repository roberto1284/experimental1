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
    derivative_raw,
    derivative_smooth,
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        time,
        derivative_raw,
        alpha=0.5,
        label="Raw derivative (np.gradient)",
    )

    plt.plot(
        time,
        derivative_smooth,
        linewidth=2,
        label="Smoothed derivative (linear regression)",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("dP/dt [Pa/s]")

    plt.legend()
    plt.grid()

    plt.show()

def plotting(x,name_x,y,name_y):
    plt.plot(
    x,y
    )

    plt.xlabel(name_x)
    plt.ylabel(name_y)
    plt.grid()

    plt.show()