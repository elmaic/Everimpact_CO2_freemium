import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap


oco2 = 'oco2\csv'
tccon = 'tccon\csv'
gosat = 'gosat\csv'
output_folder = 'data/oco2'

pathDict = {'oco2':'oco2\csv',
            'oco3': 'oco3\csv',
            'tccon':'tccon\csv',
            'gosat2':'gosat\csv'}


# set filter conditions
latitude = 'Latitude'
longitude = 'Longitude'
quality_flag = 'quality_flag'

#London Coordinates
latitud_max_london = 52
latitud_min_london = 51
longitud_max_london = 0.3
longitud_min_london = -0.6

#Paris Coordinates
coordParis = {'latMax': 49, 'latMin':48, 'longMax':3, 'longMin' :1.5}
latitud_max_paris = 49
latitud_min_paris = 48
longitud_max_paris= 3
longitud_min_paris= 1.5

def xco2_geoloc(dictDB, latMax, latMin, longMax, longMin, output_folder):
    '''
    Geolocation filter data

    Arguments:

    dictDB: Dictionary, with the key as the name of the DataBase folder, and value with the string of the datapath 
    latMax: latitud max of the Region of Interest
    latMin: latitud min of the Region of Interest
    longMax: longitud max of the Region of Interest
    longMin: longitud min of the Region of Interest
    output_folder: String of the output folder to save the CSV

    Returns
    '''
    df_merge = pd.DataFrame()
    for i in dictDB.values():
        # loop through each file in the input folder
        file_paths = [os.path.join(i, f) for f in os.listdir(i) if f.endswith('.csv')]

        df_filter = pd.DataFrame()
        for filename in file_paths:
            # read the CSV file into a dataframe
            df = pd.read_csv(filename)

            df = df[df[latitude] >= latMin]
            df = df[df[latitude] <= latMax]
            df = df[df[longitude]>= longMin]
            df = df[df[longitude]<=longMax]
            df['source'] = i

            df_filter = pd.concat([df_filter, df], ignore_index=True)
        df_merge = pd.concat([df_merge, df_filter], ignore_index=True)
        # save the filtered data to a CSV file
        output_file = f"{output_folder}/file.csv"
        df_merge.to_csv(output_file, index=False)

#h = xco2_geoloc(pathDict,latitud_max_paris, latitud_min_paris, longitud_max_paris, longitud_min_paris, output_folder)

df_plot = pd.read_csv(r'data/oco2/file.csv')
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

fig, axes = plt.subplots(4, 1, figsize=(8, 16))  # Create a 4x1 array of subplots

for index, source in enumerate(pathDict.values()):
    y2020_paris = df_plot[(df_plot['Year'] == 2020) & (df_plot['source'] == source)]
    ax = axes[index]  # Select the subplot for the current source

    boxprops = dict(facecolor='blue')
    boxplot_data = []

    for month in months:
        month_data = y2020_paris[y2020_paris['Month'] == month]['Xco2']
        boxplot_data.append(month_data.tolist())

    ax.boxplot(boxplot_data, patch_artist=True, boxprops=boxprops)
    ax.set_ylabel('xco2')
    ax.set_title(f'{source}')

    ax.set_xticklabels(months)
    ax.set_xlabel('Month')

plt.tight_layout()
plt.show() 

""" df = pd.DataFrame()
for i in pathDict.values():
    df_toMerge = pd.DataFrame()
    if not df_plot[df_plot['source'] == i].empty:
        df_toMerge = pd.DataFrame(pd.unique(df_plot[df_plot['source'] == i]['Day']), columns=['Day'])
        df_toMerge['source'] = i
    df = pd.concat([df, df_toMerge], ignore_index=True)
output_file = f"{output_folder}/file_unique.csv"
df.to_csv(output_file, index=False) """

""" df_mean = pd.DataFrame()
for i in pathDict.values():
    df_meanToMerge = pd.DataFrame()
    if not df_plot[df_plot['source'] == i].empty:
        numeric_columns = df_plot.select_dtypes(include=np.number).columns
        df_meanToMerge = df_plot.groupby(['source','Year', 'Month'])['Xco2'].mean().reset_index()
        df_meanToMerge['source'] = i
    df_mean = pd.concat([df_mean, df_meanToMerge], ignore_index=True)

output_file = f"{output_folder}/file_mean.csv"
df_mean.to_csv(output_file, index=False) """

df_mean_plot = pd.read_csv(r'data\oco2\file_mean.csv')

year_to_plot = 2020

# Filter the DataFrame for the specified year
df_year = df_mean_plot[df_mean_plot['Year'] == year_to_plot]

# Set up the figure and axes
fig, ax = plt.subplots()

# Set a color palette for the sources
color_palette = plt.cm.get_cmap('tab10')

for i, (source, path) in enumerate(pathDict.items()):
    if not df_year[df_year['source'] == path].empty:
        df_source = df_year[df_year['source'] == path]
        ax.plot(df_source['Month'], df_source['Xco2'], marker='o', label=source, color=color_palette(i))


# Set the x-axis labels as month names (assuming 'Month' column contains month numbers)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
ax.set_xticks(range(1, len(months) + 1))
ax.set_xticklabels(months)

# Set labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Xco2')
ax.set_title(f'Xco2 Comparison by Month and Source for Year {year_to_plot}')

# Add legend
ax.legend()

# Display the plot
plt.show()

# Specify the year you want to plot
year_to_plot = 2020

# Filter the DataFrame for the specified year
df_year = df_mean2[df_mean2['Year'] == year_to_plot]

# Set up the figure and axes
fig, axs = plt.subplots(len(pathDict), 1, sharex=True, figsize=(8, 12))

# Set a color palette for the sources
color_palette = plt.cm.get_cmap('tab10')

# Iterate over each source and plot the Xco2 values in separate subplots
for i, (source, path) in enumerate(pathDict.items()):
    if not df_year[df_year['source'] == source].empty:
        df_source = df_year[df_year['source'] == source]
        ax = axs[i]
        ax.plot(df_source['Month'], df_source['Xco2'], marker='o', label=source, color=color_palette(i))
        ax.set_ylabel('Xco2')
        ax.set_title(f'Xco2 Comparison for {source}')

# Set the x-axis labels for the last subplot
axs[-1].set_xlabel('Month')

# Adjust the spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()