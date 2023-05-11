import pandas as pd
import os
import csv

oco2 = 'oco2\csv'
tccon = 'tccon\csv'
gosat = 'gosat\csv'
output_folder = 'data/oco2'


# set filter conditions
latitude = 'Latitude'
longitude = 'Longitude'
quality_flag = 'quality_flag'

#London Coordinates
latitud_max_london = 52
latitud_min_london = 51
longitud_max_london = 0.241015
longitud_min_london = -0.608676

#Paris Coordinates
latitud_max_paris = 49
latitud_min_paris = 48
longitud_max_paris= 3
longitud_min_paris= 1.5

df_paris = pd.DataFrame()
for i in [oco2, tccon]:
    # loop through each file in the input folder
    file_paths = [os.path.join(i, f) for f in os.listdir(i) if f.endswith('.csv')]

    df_filter = pd.DataFrame()
    for filename in file_paths:
        # read the CSV file into a dataframe
        df = pd.read_csv(filename)

        df = df[df[latitude] >= latitud_min_paris]
        df = df[df[latitude] <= latitud_max_paris]
        df = df[df[longitude]>= longitud_min_paris]
        df = df[df[longitude]<=longitud_max_paris]

        df['source'] = i

        df_filter = pd.concat([df_filter, df], ignore_index=True)
    df_paris = pd.concat([df_paris, df_filter], ignore_index=True)
    # save the filtered data to a CSV file
    output_file = f"{output_folder}/file.csv"
    df_paris.to_csv(output_file, index=False)
