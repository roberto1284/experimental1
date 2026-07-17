from data_loader import load_excel_adrien,extract_important_data
import matplotlib.pyplot as plt


def main():
    raw_data=load_excel_adrien()
    analysis_data=extract_important_data(raw_data)

    plt.plot(
    analysis_data.time,
    analysis_data.pressure_amont,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Pressure [Pa]")
    plt.grid()

    plt.show()
    


    

if __name__=="__main__":
    main()



   