import os
import h5py
import pandas as pd
import numpy as np
import netCDF4 as nc4
from datetime import datetime, timedelta
from netCDF4 import Dataset

def conv_date_oco2(d):
    """
    Change the date type format for the satellite data OCO2

    Parameters:
      date (str): date format of the OCO 2 (Sounding_ID)
    Returns
      Date format: Y/M/D/Hr/min/Sec
    """
    return datetime.strptime(str(d), '%Y%m%d%H%M%S%f')

def conv_date_gosat2(d):
    """
    Change the date type format for the satellite data OCO2

    Parameters:
      date (str): date format of the OCO 2 (Sounding_ID)
    Returns
      Date format: Y/M/D/Hr/min/Sec
    """
    date_str = d.decode('utf-8')
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

def conv_date_tccon(d):
   '''
   '''
   base_date = datetime(1970, 1, 1)
   converted_date = base_date + timedelta(days=d)
   return converted_date.strftime('%Y-%m-%dT%H:%M:%S')

def gosat2_h5_to_csv(folder_path, output_path):
    '''
    Opens multiple H5 files with the format of the GOSAT2, converts them to CSV files, and saves the CSV files.

    CSV files format:
      Hour
      longitude
      Latitude
      XCO2
      XCH4
      year
      month
      day

    Parameters:
      folder_path (str): The path to the folder containing the H5 files.
      output_dir (str): The path to the output directory where the CSV files will be saved.

    Returns:
      None
    
    '''
    # Use os.listdir to find all HDF5 files in the folder.
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.h5')]
    #add counter
    counter = 0
    # Loop through each file and process it.
    for file_path in file_paths:
        with h5py.File(file_path, "r") as f:
            df_oco2 = pd.DataFrame()
            df_oco2['DateTime'] = f['/SoundingAttribute/observationTime'][:]
            df_oco2['Longitude'] = f['/SoundingGeometry/longitude'][:]
            df_oco2['Latitude'] = f['/SoundingGeometry/latitude'][:]
            df_oco2['Xco2'] = f['/RetrievalResult/xco2'][:]
          #  df_oco2['xch4'] = f['/RetrievalResult/xch4'][:]

            #saving date and time
            df_oco2['DateTime']= df_oco2['DateTime'].apply(conv_date_gosat2)
            df_oco2['DateTime']= pd.to_datetime(df_oco2['DateTime'])
            
            #Dividing the stored time
            df_oco2['Year']= df_oco2['DateTime'].dt.year
            df_oco2['Month']=df_oco2['DateTime'].dt.month
            df_oco2['Day']= df_oco2['DateTime'].dt.day
            df_oco2['Hour']= df_oco2['DateTime'].dt.hour

            #counter
            counter += 1

            #save the CSV file
            df = pd.DataFrame.from_dict(df_oco2)
            output_file = f"{output_path}/file_{counter}.csv"
            df.to_csv(output_file, index=False)
    print(f"{counter} files converted to CSV.")

def oco2_nc4_to_csv(folder_path, output_path):
    """
    Change the nc4 file from OCO2 and OCO3 to CSV

    CSV files format:
      Hour
      Longitude
      Latitude
      XCO2
      year
      month
      day

    Parameters:
      folder_path: path to the folder of the nc4 files from oco2/3
      output_path: path to store the CSV files

    Returns:
    """
    #fetching of file paths on a list
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.nc4')]
    #add counter
    counter = 0

    #open each file
    for file_path in file_paths:
      #open the netCDF4 file
      with nc4.Dataset(file_path, "r") as f:
         #substraction of the desired variables into a new dataframe
         df_oco2_xco2= pd.DataFrame()
         df_oco2_xco2['DateTime']= f['sounding_id'][:]
         df_oco2_xco2['Longitude']= f['longitude'][:]
         df_oco2_xco2['Latitude']= f['latitude'][:]
         df_oco2_xco2['Xco2']= f['xco2'][:]
         #Convert soundingID to datetime format
         df_oco2_xco2['DateTime']= df_oco2_xco2['DateTime'].apply(conv_date_oco2)
         df_oco2_xco2['DateTime']= pd.to_datetime(df_oco2_xco2['DateTime'])

         # YEAR and month column
         df_oco2_xco2['Year']= df_oco2_xco2['DateTime'].dt.year
         df_oco2_xco2['Month']= df_oco2_xco2['DateTime'].dt.month
         df_oco2_xco2['Day']= df_oco2_xco2['DateTime'].dt.day
         df_oco2_xco2['Hour']= df_oco2_xco2['DateTime'].dt.hour
         
         #count +1
         counter += 1

         #save the new Dataset to a CSV
         output_file = f"{output_path}/file2023_{counter}.csv"
         df_oco2_xco2.to_csv(output_file, index=False)

      print(f"{counter} files converted to CSV.")

def tccon_nc_to_csv(folder_path, output_path):
    """
    Open an NC file of the TCCON database and transforms it to a CSV file

    CSV files format:
      Longitude
      Latitude
      year
      XCO2
      year
      month
      day

    Parameters:
      folder_path: path to the folder of the nc4 files from oco2/3
      output_path: path to store the CSV files

    Returns:
    """
    #fetching of file paths on a list
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.nc')]
    #add counter
    counter = 0

    #open each file
    for file_path in file_paths:
      #open the netCDF4 file
      with Dataset(file_path) as f:
       df_tccon = pd.DataFrame()
       # Extract the variable data
       df_tccon['DateTime'] = f.variables['time'][:]
       df_tccon['Longitude'] = f.variables['long_deg'][:]
       df_tccon['Latitude'] = f.variables['lat_deg'][:]
#       df_tccon['Geometric Altitude'] = f.variables['zobs_km'][:]
#       df_tccon['Pressure Altitude'] = f.variables['zmin_km'][:]
       df_tccon['Xco2'] = f.variables['xco2_ppm'][:]
#       df_tccon['xch4'] = f.variables['xch4_ppm'][:]
        #Convert soundingID to datetime format
       df_tccon['DateTime']= df_tccon['DateTime'].apply(conv_date_tccon)
       df_tccon['DateTime']= pd.to_datetime(df_tccon['DateTime'])

        # YEAR and month column
       df_tccon['Year']= df_tccon['DateTime'].dt.year
       df_tccon['Month']= df_tccon['DateTime'].dt.month
       df_tccon['Day']= df_tccon['DateTime'].dt.day
       #    df_tccon['prior_co2'] = f.variables['prior_co2'][:]
       #    df_tccon['prior_ch4'] = f.variables['prior_ch4'][:]
       #    df_tccon['ak_co2'] = f.variables['ak_co2'][:]
       #    df_tccon['ak_ch4'] = f.variables['ak_ch4'][:]

       counter += 1

       output_file = f"{output_path}/file_{counter}.csv"
       df_tccon.to_csv(output_file, index=False)
    print(f"{counter} files converted to CSV.")

def icos_to_csv(file_in):
    
    file = pd.read_csv(file_in, delimiter=';', nrows=18)

    latitude_line = file[file.apply(lambda row: '# LATITUDE:' in str(row), axis=1)].values[0][0]
    latitude_str = latitude_line.split(':')[1].strip()
    latitude = None
    
    if latitude_str and latitude_str != 'CO2':
        try:
            latitude = float(latitude_str.split(' ')[0]) * (-1 if 'S' in latitude_str else 1)
        except ValueError:
            pass  # or any other desired handling

    longitude_line = file[file.apply(lambda row: '# LONGITUDE:' in str(row), axis=1)].values[0][0]
    longitude_str = longitude_line.split(':')[1].strip()
    longitude = None
    
    if longitude_str and longitude_str != 'CO2':
        try:
            longitude = float(longitude_str.split(' ')[0]) * (-1 if 'W' in longitude_str else 1)
        except ValueError:
            pass  # or any other desired handling
    
    df_ICOS = pd.read_csv(file_in, delimiter=';', skiprows=38)
    df_ICOS['Latitude'] = latitude
    df_ICOS['Longitude'] = longitude

    df_ICOS.loc[~df_ICOS['Flag'].isin(['U', 'N']), 'Flag'] = None
    df_ICOS.dropna(subset=['Flag'], inplace=True)

    df_ICOS['Xco2'] = df_ICOS['co2'][:]
    df_ICOS = df_ICOS[['Latitude', 'Longitude','Xco2', 'Year', 'Month','Day', 'Hour', 'SamplingHeight', 'Flag']]

    return df_ICOS

def icos_file_scrapper(folder_path, output_path):
    '''
    cokngóij
    '''
    #fetching of file paths on a list
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.CO2')]
    #add counter
    counter = 0
    df_agregation = pd.DataFrame()
    for file in file_paths:
      df_h = icos_to_csv(file)
      # Ensure consistent column names
      if counter == 0:
         df_agregation = df_h
      else:
         df_agregation = pd.concat([df_agregation, df_h], ignore_index=True)
      counter += 1
      print(df_agregation)

    output_file_agg = f"{output_path}/icos.csv"
    df_agregation.to_csv(output_file_agg, index=False)
    print(counter)
        

file_out= 'ICOS\saclay\csv'
file_in = 'ICOS\saclay'
h = icos_file_scrapper(file_in, file_out)