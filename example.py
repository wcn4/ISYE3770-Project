import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv

df = 0
def main():
    global df
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
            #new_row = {'driverId': driver_id, 'avg_pitstop_time': avg_pitstop_time, 'position': position}
            csvwriter.writerow([driver_id, avg_pitstop_time, position])
            #new_df.append(new_row, ignore_index=True)


main()
    