import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv

def create_csv():
    
    pitstops = pd.read_csv("archive/pit_stops.csv")
    results = pd.read_csv("archive/results.csv")

    race_ids = pitstops['raceId'].unique()

    for race_id in race_ids:
        
        csvfile = open(f"pitstop_results/race_{race_id}.csv", 'w')
        csvwriter = csv.writer(csvfile)

        fields = ['driverId', 'avg_pitstop_time', 'position']
        csvwriter.writerow(fields)

        #Extract Data
        race_data = pitstops[pitstops['raceId'] == race_id] #Get all pitstop entries with the same race id
        race_results = results[results['raceId'] == race_id] #Get the results of that race

        driver_ids = race_results['driverId'].unique()
        #Now for each driver, need to get their average pitstop time, and map it to their race results
        for driver_id in driver_ids:

            #Line breakdown:
            #    race_data[race_data['driverId'] == driver_id]: Gets the pitstop data per driver
            #    ['milliseconds'].mean(): Finds the average of the milliseconds column from the data above
            avg_pitstop_time = race_data[race_data['driverId'] == driver_id]['milliseconds'].mean()

            #Get the position of the driver. Not necessarily going to be valid
            position = race_results[race_results['driverId'] == driver_id]['position'].iloc[0]
            csvwriter.writerow([driver_id, avg_pitstop_time, position])

def create_histogram(race_id, bins=20):
    race_results = pd.read_csv(f"pitstop_results/race_{race_id}.csv")
    pitstop_times = np.array(race_results['avg_pitstop_time'])
    plt.hist(pitstop_times, bins='auto')
    plt.xlabel('Pitstop Time in Milliseconds')
    plt.ylabel('Frequency')
    plt.title(f"Average Pitstop Time Histogram for Race {race_id}")
    plt.savefig(f"race_pitstop_histograms/race_{race_id}.png")
    #plt.show()


def generate_relative_differences():
    pitstops = pd.read_csv("archive/pit_stops.csv")
    results = pd.read_csv("archive/results.csv")

    csvfile = open(f"pitstop_results/relative_differences.csv", 'w')
    csvwriter = csv.writer(csvfile)

    fields = ['raceId', 'driverId', 'position', 'relative_diff', 'driver_avg', 'race_avg']
    csvwriter.writerow(fields)

    #For each race, look at the average pitstop time generated already
    race_ids = pitstops['raceId'].unique()

    for race_id in race_ids:
        race_data = pitstops[pitstops['raceId'] == race_id]
        race_results = results[results['raceId'] == race_id]
        
        driver_ids = race_results['driverId'].unique()

        race_avg_pitstop_time = race_data['milliseconds'].mean()
        
        #Now for each driver, need to get their average pitstop time, and map it to their race results
        for driver_id in driver_ids:

            #Line breakdown:
            #    race_data[race_data['driverId'] == driver_id]: Gets the pitstop data per driver
            #    ['milliseconds'].mean(): Finds the average of the milliseconds column from the data above
            driver_avg_pitstop_time = race_data[race_data['driverId'] == driver_id]['milliseconds'].mean()

            #Get the position of the driver. Not necessarily going to be valid
            position = race_results[race_results['driverId'] == driver_id]['position'].iloc[0]

            relative_diff = (driver_avg_pitstop_time - race_avg_pitstop_time) / race_avg_pitstop_time

            csvwriter.writerow([race_id, driver_id, position, relative_diff, driver_avg_pitstop_time, race_avg_pitstop_time])

def show_scatter():
    relative_diff_data = pd.read_csv('pitstop_results/relative_differences.csv')

    #Drop all invalid position ranks
    relative_diff_data = relative_diff_data[relative_diff_data['position'] != r'\N']
    relative_diff_data = relative_diff_data[relative_diff_data['relative_diff'].notna()]

    #relative_diff_data = relative_diff_data[np.abs(relative_diff_data['relative_diff']) < 0.1]

    relative_diffs = np.array(relative_diff_data['relative_diff'])
    positions = np.array(relative_diff_data['position'])
    positions = positions.astype(np.int32)

    b, m = np.polynomial.polynomial.polyfit(relative_diffs, positions, deg=1)


    # Calculate predicted values
    predicted_positions = b + m * relative_diffs

    # Calculate R-squared value
    ss_total = np.sum((positions - np.mean(positions))**2)
    ss_residual = np.sum((positions - predicted_positions)**2)
    r_squared = 1 - (ss_residual / ss_total)

    print(f"y=mx+b where:\nm: {m}\nb: {b}\nR^2: {r_squared}")

    plt.plot(relative_diffs, (m * relative_diffs) + b, '-', color='orange')
    plt.scatter(relative_diffs, positions)
    plt.show()




#create_csv()
#pitstops = pd.read_csv("archive/pit_stops.csv")
#race_ids = pitstops['raceId'].unique()
#for race_id in race_ids:
#    create_histogram(race_id)

#generate_relative_differences()

#show_scatter()