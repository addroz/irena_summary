import sys

import geopy.distance
import pandas as pd
import numpy as np
import config

def remove_trailing_whitespaces(df):
    return df.replace({"^\s*|\s*$":""}, regex = True)

def read_and_prepare_data():
    irena_cap_db = remove_trailing_whitespaces(
        pd.read_excel(config.IRENA_CAP_FILE_PATH, skiprows=2, header=None))
    irena_gen_db = remove_trailing_whitespaces(
        pd.read_excel(config.IRENA_ELECGEN_FILE_PATH, skiprows=2, header=None))

    irena_cap_db.set_axis(['country', 'type', 'subtype', 'year', 'cap'], axis=1, inplace=True)
    irena_gen_db.set_axis(['country', 'type', 'subtype', 'year', 'gen'], axis=1, inplace=True)

    irena_cap_db.fillna(method='ffill', inplace=True)
    irena_gen_db.fillna(method='ffill', inplace=True)

    irena_cap_db.replace('..', 0, inplace=True)
    irena_gen_db.replace('..', 0, inplace=True)

    irena_cap_db = irena_cap_db[irena_cap_db['country'].isin(config.COUNTRIES)]
    irena_gen_db = irena_gen_db[irena_gen_db['country'].isin(config.COUNTRIES)]

    irena_cap_db = irena_cap_db[~irena_cap_db['year'].isna()]
    irena_gen_db = irena_gen_db[~irena_gen_db['year'].isna()]

    irena_cap_db['year'] = irena_cap_db['year'].astype(int)
    irena_gen_db['year'] = irena_gen_db['year'].astype(int)

    irena_cap_db = irena_cap_db[irena_cap_db['year'].isin(config.YEARS)]
    irena_gen_db = irena_gen_db[irena_gen_db['year'].isin(config.YEARS)]

    irena_cap_db = irena_cap_db[~((irena_cap_db['type'] == 'On-grid Solar photovoltaic') &
        (irena_cap_db['subtype'] == 'Off-grid'))]
    irena_cap_db = irena_cap_db[~((irena_cap_db['type'] == 'Off-grid Solar photovoltaic') &
        (irena_cap_db['subtype'] == 'On-grid'))]
    irena_gen_db = irena_gen_db[~((irena_gen_db['type'] == 'On-grid Solar photovoltaic') &
        (irena_gen_db['subtype'] == 'Off-grid'))]
    irena_gen_db = irena_gen_db[~((irena_gen_db['type'] == 'Off-grid Solar photovoltaic') &
        (irena_gen_db['subtype'] == 'On-grid'))]

    irena_cap_db.replace(['On-grid Solar photovoltaic', 'Off-grid Solar photovoltaic'],
        'Solar photovoltaic', inplace = True)
    irena_gen_db.replace(['On-grid Solar photovoltaic', 'Off-grid Solar photovoltaic'],
        'Solar photovoltaic', inplace = True)

    irena_cap_db.reset_index(drop = True, inplace = True)
    irena_gen_db.reset_index(drop = True, inplace = True)

    return (irena_cap_db, irena_gen_db)

def summarize_and_save(data, file, value_column):
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    for type in set(data['type']):
        data_by_type = (data[data['type'] == type]).copy()
        data_by_type.drop(columns=['subtype', 'type'], inplace=True)

        data_by_type = data_by_type.groupby(by=['country', 'year']).sum()
        data_by_type.reset_index(inplace = True)
        data_by_type.sort_values(by=['country', 'year'], inplace=True)

        for country in config.COUNTRIES:
            if not data_by_type[(data_by_type['country'] == country) &
                (data_by_type['year'] == 2020)].empty:
                data_by_type = data_by_type[~((data_by_type['country'] == country) &
                    (data_by_type['year'] == 2019))]

        data_by_type.sort_values(by = ['country', 'year'], inplace=True)
        data_by_type['diffs'] = data_by_type.groupby(['country'])[value_column]\
            .transform(lambda x: x.diff().fillna(data_by_type[value_column]))
        data_by_type.sort_index(inplace=True)

        data_by_type.drop(columns = [value_column], inplace=True)
        data_by_type.rename(columns={'diffs': value_column}, inplace=True)

        print(f'Saving data for {type}')
        data_by_type.to_excel(writer, sheet_name = type, index = False)

    print(f'Results saved to: {file}')
    writer.save()

if __name__ == '__main__':
    print('Fetching and processing data')
    irena_cap_db, irena_gen_db = read_and_prepare_data()

    print('Saving capacity data')
    summarize_and_save(irena_cap_db, 'irena_cap_summary.xlsx', 'cap')

    print('Saving generation data')
    summarize_and_save(irena_gen_db, 'irena_elecgen_summary.xlsx', 'gen')
