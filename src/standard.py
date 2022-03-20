import openpyxl as xl
import os
from pathlib import Path 
import pandas as pd


raw = Path('data/raw')

path_to_file = os.path.join(raw,'CxI_DR_2007_2012_PRO_DET.xlsx')

df = pd.read_excel(path_to_file, sheet_name='2012')

if __name__ == '__main__':

    #change code to first 4 characters
    df['Code'] = df['Code'].str[:4]
    print(df.head())
    

