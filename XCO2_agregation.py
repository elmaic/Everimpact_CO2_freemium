import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap
import seaborn as sns


oco2 = 'oco2\csv'
tccon = 'tccon\csv'
gosat = 'gosat\csv'
output_folder = 'data/oco2'

pathDict = {'oco2':'oco2\csv',
            'oco3': 'oco3\csv',
            'tccon':'tccon\csv',
            'gosat2':'gosat\csv',
            'icos':'ICOS\saclay\csv'}

satData = {'oco2':'oco2\csv',
            'oco3': 'oco3\csv',
            'gosat2':'gosat\csv'}

dateDict = {'Year':2023,
            'Month':2}

#Paris Coordinates
coordParis = {'latMax': 48.8, 'latMin':48.6, 'longMax':2.2, 'longMin' :2.1}

def xco2_geoloc(dictDB, coordParis, dateDict, output_folder):
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

            df = df[(df['Latitude'] >= coordParis['latMin'])&(df['Latitude'] <= coordParis['latMax'])]
            df = df[(df['Longitude']>= coordParis['longMin'])&(df['Longitude']<=coordParis['longMax'])]
            df = df[df['Year'] == dateDict['Year']]
            df['source'] = i

            #dfmonth = monthly_csv(df,satData)
            #if dateDict.get('Month'):
                #df = df[df['Month'] == dateDict['Month']]

            df_filter = pd.concat([df_filter, df], ignore_index=True)
        df_merge = pd.concat([df_merge, df_filter], ignore_index=True)
    
    
    # save the filtered data to a CSV file
    output_file = f"{output_folder}/file.csv"
    df_merge.to_csv(output_file, index=False)

def monthly_csv(a, satData, output_file):

    df = pd.read_csv(a)
    dfDayFilter = pd.DataFrame()
    dfMonthFilter = pd.DataFrame()
    dfmonth = pd.DataFrame()

    for m in range(1, 13):
        df_filtered = df[df['Month'] == m]
        dfDayFilter = hour_csv(df_filtered, satData)
        
        print(dfDayFilter)
        dfMonthFilter = pd.concat([dfMonthFilter, dfDayFilter], ignore_index=True)

    output_file = f"{output_folder}/file_month.csv"
    dfMonthFilter.to_csv(output_file, index=False)

    return dfMonthFilter

def hour_csv(df, satData):
    dfMerge = pd.DataFrame()
    dfDays = pd.DataFrame()
    dfhour = pd.DataFrame()
    dffinal = pd.DataFrame()
    days = []
    hours = []

    for src in satData.values():
            filtered_df = df[df['source'] == src]
            if not filtered_df.empty:
                days.extend(filtered_df['Day'].tolist())
                hours.extend(filtered_df['Hour'].tolist())

    unDays = set(days)
    unique_Days = (list(unDays))

    unhours = set(hours)
    unique_Hours = (list(unhours))

    for d in unique_Days:
        df = df[df['Day'] == d]
        dfDays = pd.concat([dfDays, df], ignore_index=True)

    print(dfMerge)

    for h in unique_Hours:
        dfhour = dfDays[dfDays['Hour'] == h]
        dffinal = pd.concat([dffinal, dfhour], ignore_index=True)

    print(dffinal)

    return dffinal

#f = xco2_geoloc(pathDict,coordParis, dateDict ,output_folder)
g = r'data/oco2/file.csv'
h = monthly_csv(g, satData, output_folder)

 
""" Scatter_plot = r'data/oco2/file_hours.csv'
df_sct = pd.read_csv(Scatter_plot)
print(df_sct)
dfSat = df_sct[df_sct['source'] == 'oco3\csv']
dfSat = dfSat['Xco2'].mean()

print(dfSat)

dfGnd100 = df_sct[df_sct['SamplingHeight'] == 100]
dfGnd15 = df_sct[df_sct['SamplingHeight'] == 15]
dfGnd60 = df_sct[df_sct['SamplingHeight'] == 60]

plt.subplot(3,2,1)
sns.scatterplot(x= dfSat, y=dfGnd100['Xco2'])
plt.subplot(3,2,2)
sns.scatterplot(x= dfSat, y=dfGnd15['Xco2'])
plt.subplot(3,2,3)
sns.scatterplot(x= dfSat, y=dfGnd60['Xco2'])
plt.show() 
 """
""" 
df_plot = pd.read_csv(r'data/oco2/file.csv')
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

fig, axes = plt.subplots(5, 1, figsize=(10, 20))  # Create a 4x1 array of subplots

for index, source in enumerate(pathDict.values()):
    y2020_paris = df_plot[(df_plot['Year'] == 2023) & (df_plot['source'] == source)]
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


#MEAN DATA FRAME LOOP
df_mean = pd.DataFrame()
for i in pathDict.values():
    if not df_plot[df_plot['source'] == i].empty:
        df_meanToMerge = df_plot[df_plot['source'] == i].groupby(['source', 'Year', 'Month'])['Xco2'].mean().reset_index()
        df_meanToMerge['source'] = i
        df_mean = pd.concat([df_mean, df_meanToMerge], ignore_index=True)

output_file = f"{output_folder}/file_mean.csv"
df_mean.to_csv(output_file, index=False)


#PLOTTING MEAN DATA FRAME

df_mean_plot = pd.read_csv(r'data\oco2\file_mean.csv')

year_to_plot = 2023

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


# Set the x-axis labels as month names
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

'''
AGGREGATION

'''

#AGGREGATION DATA FRAME
df_agg = pd.DataFrame()
for i in pathDict.values():
    if not df_plot[df_plot['source'] == i].empty:
        df_aggToMerge = df_plot[df_plot['source'] == i].groupby(['source', 'Year', 'Month'])['Xco2'].agg([np.mean, np.std]).reset_index()
        df_aggToMerge.columns = ['source', 'Year', 'Month', 'Xco2_mean', 'Xco2_std']
        df_aggToMerge['source'] = i
        df_agg = pd.concat([df_agg, df_aggToMerge], ignore_index=True)

output_file_agg = f"{output_folder}/file_agg.csv"
df_agg.to_csv(output_file_agg, index=False)

#PLOTTING MEAN DATA FRAME

df_agg_plot = pd.read_csv(r'data\oco2\file_agg.csv')

# Filter the DataFrame for the specified year
df_year_agg = df_agg_plot[df_agg_plot['Year'] == year_to_plot]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

for i, (source, path) in enumerate(pathDict.items()):
    if not df_year_agg[df_year_agg['source'] == path].empty:
        df_source = df_year_agg[df_year_agg['source'] == path]
        ax1.plot(df_source['Month'], df_source['Xco2_std'], marker='o', label=source, color=color_palette(i))
        ax2.plot(df_source['Month'], df_source['Xco2_mean'], marker='o', label=source, color=color_palette(i))

# Set the x-axis labels as month names (assuming 'Month' column contains month numbers)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
ax1.set_xticks(range(1, len(months) + 1))
ax1.set_xticklabels(months)
ax2.set_xticks(range(1, len(months) + 1))
ax2.set_xticklabels(months)

# Set labels and title for the first subplot
ax1.set_xlabel('Month')
ax1.set_ylabel('Xco2_std')
ax1.set_title(f'Xco2 Standard Deviation Comparison by Month and Source for Year {year_to_plot}')

# Set labels and title for the second subplot
ax2.set_xlabel('Month')
ax2.set_ylabel('Xco2_mean')
ax2.set_title(f'Xco2 Mean Comparison by Month and Source for Year {year_to_plot}')

# Add legend to both subplots
ax1.legend()
ax2.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()
 """