import os
from pathlib import Path 
import pandas as pd
import numpy as np
from sqlalchemy import true

#path to raw data
raw = Path('data/raw')

#creates standard folder for standardized data
os.mkdir('data/standard')
#path to standard data
standard = Path('data/standard')

#name of file
file_name = os.listdir(raw)[1]

#path to the file
path_to_file = os.path.join(raw, file_name)



if __name__ == '__main__':
    df = pd.read_excel(path_to_file, sheet_name='2012')

    print(df.shape)

    df['1'] = 0
    df['2'] = 0
    df['3'] = 0
    df['4'] = 0


    print(df.shape)

    #rename columns
    new_column_names = [i for i in df['Commodity Description']]
    column_names = [i for i in df.columns]
    print(len(new_column_names))
    print(len(column_names))

    count = 2
    des_counter = 0
    while count < df.shape[1]:
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

    #commodities table creation
    count = 0
    commodity_id = []
    for i in df['Commodity Description']:
        count +=1
        commodity_id.append(count)

    commodities = pd.DataFrame({'commodity_id': commodity_id, 'commodity':df['Commodity Description'],
                                    'code':df['Code']})
    commodities.set_index('commodity_id')

    #commodities has commodities linking table creation

    values = []
    commodity_id_a = []
    commodity_id_b = []
    commodity_a_count = 0
    commodity_b_count = 1
    while commodity_b_count <= len(commodities):
        commodity_id_b.append(commodity_b_count)
        commodity_a_count +=1
        commodity_id_a.append(commodity_a_count)
        if commodity_a_count == commodity_id[-1]:
            commodity_a_count = 0
            commodity_b_count +=1

    values_count = -1
    while values_count <= len(new_column_names):
        values_count +=1
        try:
            for i in range(len(df[new_column_names[values_count]])):
                values.append(df[new_column_names[values_count]][i])
        except IndexError:
            continue


    #for index, commodity in enumerate(new_column_names):
        #print(index, commodity)

    print("values:",len(values))
    print("commodity a", len(commodity_id_a))
    print("commodity b", len(commodity_id_b))
    #print(values)

    commodities_has_commodities = pd.DataFrame({"commodity_a_id":commodity_id_a,
                                                "commodity_b_id":commodity_id_b,
                                                "values":values})

    #sectors table creation
    sectors_dict = {
                "11":'Agriculture',
                "21":"Mining",
                "22":"Utilities",
                "23":"Construction",
                "33":"Durable Goods",
                "31":"Nondurable Goods",
                "42":"Wholesale Trade",
                "44":"Retail Trade",
                "48":"Transportation",
                "51":"Information",
                "52":"Finance and Insurance",
                "53":"Real Estate and Rental Leasing",
                "54":"Professional and Technical Services",
                "55":"Managment of Companies and Entreprises",
                "56":"Administration and Water Services",
                "61":"Educational Services",
                "62":"Health Care and Social Assistance",
                "71":"Arts, Entertainment, and Recreation",
                "72":"Accomodation and Food Services",
                "81":"Other Servies, Except Government",
                "GS":"Goverment",
                "S0":"Used or Other"}

    sector_names = [i for i in sectors_dict.values()]
    sector_codes = [i for i in sectors_dict.keys()]
    count = 1
    sector_id = []
    while count <= len(sector_names):
       sector_id.append(count)
       count +=1

    sectors = pd.DataFrame({"sector_id":sector_id,
                            "sector":sector_names}) 

    #sector_id forign key creation
    

    #output
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, sheet_name='2012')
        group_df.to_excel(writer, sheet_name='Groupby Code')
        commodities.to_excel(writer, sheet_name='commodities')
        commodities_has_commodities.to_excel(writer, sheet_name='commodities_has_commodities')
        sectors.to_excel(writer, sheet_name="sectors")
    
    

