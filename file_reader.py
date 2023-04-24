import os
import h5py
import pandas as pd
import netCDF4 as nc
from datetime import datetime

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

def gosat2_h5_to_csv(folder_path, output_path):
    '''
    Opens multiple H5 files with the format of the GOSAT2, converts them to CSV files, and saves the CSV files.

    CSV files format:
      Hour
      Longitude
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
            df_oco2['longitude'] = f['/SoundingGeometry/longitude'][:]
            df_oco2['latitude'] = f['/SoundingGeometry/latitude'][:]
            df_oco2['Xco2'] = f['/RetrievalResult/xco2'][:]
            df_oco2['xch4'] = f['/RetrievalResult/xch4'][:]

            #saving date and time
            df_oco2['DateTime']= df_oco2['DateTime'].apply(conv_date_gosat2)
            df_oco2['DateTime']= pd.to_datetime(df_oco2['DateTime'])
            
            #Dividing the stored time
            df_oco2['Year']= df_oco2['DateTime'].dt.year
            df_oco2['Month']=df_oco2['DateTime'].dt.month
            df_oco2['Day']= df_oco2['DateTime'].dt.day

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
      XCO2 Quality flag
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
      with nc.Dataset(file_path, "r") as f:
         #substraction of the desired variables into a new dataframe
         df_oco2_xco2= pd.DataFrame()
         df_oco2_xco2['DateTime']= f['sounding_id'][:]
         df_oco2_xco2['Longitude']= f['longitude'][:]
         df_oco2_xco2['Latitude']= f['latitude'][:]
         df_oco2_xco2['Xco2']= f['xco2'][:]
         df_oco2_xco2['quality_flag']= f['xco2_quality_flag'][:]

         #Convert soundingID to datetime format
         df_oco2_xco2['DateTime']= df_oco2_xco2['DateTime'].apply(conv_date_oco2)
         df_oco2_xco2['DateTime']= pd.to_datetime(df_oco2_xco2['DateTime'])

         # YEAR and month column
         df_oco2_xco2['Year']= df_oco2_xco2['DateTime'].dt.year
         df_oco2_xco2['Month']= df_oco2_xco2['DateTime'].dt.month
         df_oco2_xco2['Day']= df_oco2_xco2['DateTime'].dt.day
         
         #count +1
         counter += 1

         #save the new Dataset to a CSV
         output_file = f"{output_path}/file_{counter}.csv"
         df_oco2_xco2.to_csv(output_file, index=False)

      print(f"{counter} files converted to CSV.")

file_in = 'gosat'
file_out= 'gosat\csv'
h = gosat2_h5_to_csv(file_in, file_out)