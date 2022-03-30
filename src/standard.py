import os
from pathlib import Path 
import pandas as pd


raw = Path('data/raw')

os.mkdir('data/standard')
standard = Path('data/standard')

file_name = os.listdir(raw)[1]

path_to_file = os.path.join(raw, file_name)



if __name__ == '__main__':
    df = pd.read_excel(path_to_file, sheet_name='2012')

    #rename columns
    new_column_names = [i for i in df['Commodity Description']]
    column_names = [i for i in df.columns]

    count = 2
    des_counter = 0
    while count < len(df.columns):
        df = df.rename(columns={column_names[count]: new_column_names[des_counter]})
        count +=1
        des_counter +=1

    #change code to first 4 characters
    df['Code'] = df['Code'].str[:4]

    #fixes missing values
    df.ffill(inplace=True)
    output = os.path.join(standard, file_name)

    #group by df
    group_df = df.groupby('Code').sum()
    
    #output
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, sheet_name='2012')
        group_df.to_excel(writer, sheet_name='Groupby Code')
    
    

