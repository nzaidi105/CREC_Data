import os
from pathlib import Path 
import pandas as pd


raw = Path('data/raw')

standard = Path('data/standard')
file_name = os.listdir(raw)[1]

path_to_file = os.path.join(raw, file_name)



if __name__ == '__main__':
    df = pd.read_excel(path_to_file, sheet_name='2012')
    #change code to first 4 characters
    df['Code'] = df['Code'].str[:4]
    output = os.path.join(standard, file_name)
    #output
    df.to_excel(output)
    
    print(df.head())
    

