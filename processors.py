from scipy.signal import savgol_filter
import numpy as np
from experimental_data import AnalysisData, Results
from processor_utils import build_results

class SavgolProcessor:

    def __init__(
        self,
        window_length=251,
        polyorder=3,
    ):
        self.window_length = window_length
        self.polyorder = polyorder

    def smooth(
        self,
        pressure,
    ):
        return savgol_filter(
            pressure,
            window_length=self.window_length,
            polyorder=self.polyorder,
        )

    def derivative(
        self,
        time,
        pressure,
    ):
        dt_mean = np.mean(np.diff(time))

        return savgol_filter(
            pressure,
            window_length=self.window_length,
            polyorder=self.polyorder,
            deriv=1,
            delta=dt_mean,
        )
    def process_pressure(
        self,
        time,
        pressure,
    ):
        pressure_smooth = self.smooth(pressure)
        pressure_derivative = self.derivative(time, pressure)

        return pressure_smooth, pressure_derivative   
    
    def process(
        self,
        analysis_data,
        model,
    ):

        p_amont_smooth, dP_dt = self.process_pressure(
            analysis_data.time,
            analysis_data.pressure_amont,
        )

        p_avale_smooth, _ = self.process_pressure(
            analysis_data.time,
            analysis_data.pressure_avale,
        )

        return build_results(
            analysis_data=analysis_data,
            model=model,
            p_amont_smooth=p_amont_smooth,
            p_avale_smooth=p_avale_smooth,
            dP_dt=dP_dt,
            method="Savitzky-Golay",
        )

class LocalLinearRegressionProcessor:

    def __init__(
        self,
        half_window=126,
    ):
        self.half_window = half_window
    
    def local_linear_regression(
        self,
        pressure,
        time,
    ):

        a_array = []
        b_array = []

        N = len(time)

        for i in range(N):

            start = max(i - self.half_window, 0)
            end = min(i + self.half_window + 1, N)

            t = time[start:end]
            P = pressure[start:end]

            a, b = np.polyfit(t, P, 1)

            a_array.append(a)
            b_array.append(b)

        a_array = np.array(a_array)
        b_array = np.array(b_array)

        pressure_smooth = a_array * time + b_array

        return a_array, b_array, pressure_smooth

    def process(
        self,
        analysis_data,
        model,
    ):

        a_amont, b_amont, p_amont_smooth = self.local_linear_regression(
            analysis_data.pressure_amont,
            time=analysis_data.time,
        )

        a_avale, b_avale, p_avale_smooth = self.local_linear_regression(
            analysis_data.pressure_avale,
            time=analysis_data.time,
        )

        return build_results(
            analysis_data=analysis_data,
            model=model,
            p_amont_smooth=p_amont_smooth,
            p_avale_smooth=p_avale_smooth,
            dP_dt=a_amont,
            method="Local Linear Regression",
        )