import sys
from tkinter.tix import Tree

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

def remove_negative_values(data, by, over):
    for element in over:
        years = list(data[data[by] == element]['year'])
        if len(years) == 0:
            continue

        for i in range(len(years) - 1):
            year = years[-(i+1)]
            previous_year = years[-(i+2)]
            value = list(data[(data['year'] == year) & (data[by] == element)]['cap'])[0]
            if value < 0:
                data['cap'] = np.where((data['year'] == previous_year) &
                    (data[by] == element), data['cap'] + value, data['cap'])
                data['cap'] = np.where((data['year'] == year) & (data[by] == element),
                    0, data['cap'])

        data['cap'] = np.where((data[by] == element) & (data['year'] == years[0]) &
            (data['cap'] < 0), 0, data['cap'])

    return data


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

        if value_column == 'cap':
            data_by_type = remove_negative_values(data_by_type, 'country', config.COUNTRIES)

        print(f'Saving data for {type}')
        data_by_type.to_excel(writer, sheet_name = type, index = False)

    print(f'Results saved to: {file}')
    writer.save()

def append_missing_rows(data, gen = False):
    data.set_index(['year', 'ID-year'], inplace = True)

    if (2020, 2020) not in data.index:
        data.reset_index(inplace=True)
        data.loc[(data['year'] == 2020) & (data['ID-year'] == 2019), 'ID-year'] = 2020
        data.set_index(['year', 'ID-year'], inplace = True)
    elif gen is False:
        data.loc[(2020, 2020)] = data.loc[(2020, 2019)] + data.loc[(2020, 2020)]
        data.drop(index = (2020, 2019), inplace=True)
    else:
        data.drop(index = (2020, 2019), inplace=True)

    data.reset_index(inplace=True)

    for (year, ID_year) in config.EMPTY_ROWS_TO_ADD:
        if data[(data['year'] == year) &
                (data['ID-year'] == ID_year)].empty:
            data = data.append({'year': year, 'ID-year': ID_year}, ignore_index = True)

    return data.sort_values(by = ['year', 'ID-year'])

def add_missing_columns(data):
    for colname in config.TYPES_TO_SUMMARY:
        if colname not in data.columns.values:
            data[colname] = 0
    return data.reindex(columns=['year', 'ID-year'] + config.TYPES_TO_SUMMARY)

def get_data_for_all_sheet(irena_db, variable):
    data_for_all = irena_db.drop(columns = ['country'])
    data_for_all = data_for_all.groupby(by = ['year', 'type']).sum().reset_index()
    data_for_all = data_for_all[data_for_all['type'].isin(config.TYPES_TO_SUMMARY)]
    data_for_all.sort_values(by = ['type', 'year'], inplace=True)
    data_for_all['diffs'] = data_for_all.groupby(['type'])[variable]\
        .transform(lambda x: x.diff().fillna(data_for_all[variable]))
    data_for_all.sort_index(inplace=True)
    data_for_all.drop(columns = [variable], inplace=True)
    data_for_all.rename(columns={'diffs': variable, 'year': 'ID-year'}, inplace=True)
    data_for_all['year'] = config.YEAR_DATA
    if variable == 'cap':
        data_for_all = remove_negative_values(data_for_all, 'type', config.TYPES_TO_SUMMARY)

    data_for_all = data_for_all.set_index(['year', 'ID-year', 'type'])[variable]\
            .unstack().reset_index()

    data_for_all = add_missing_columns(data_for_all)
    data_for_all = append_missing_rows(data_for_all)

    return data_for_all

def get_data_for_country_sheet(irena_db, variable, country):
    data_by_country = (irena_db[(irena_db['country'] == country) &
                                (irena_db['type'].isin(config.TYPES_TO_SUMMARY))]).copy()
    data_by_country.sort_values(by = ['type', 'year'], inplace=True)
    data_by_country['diffs'] = data_by_country.groupby(['type'])[variable]\
        .transform(lambda x: x.diff().fillna(data_by_country[variable]))
    data_by_country.sort_index(inplace=True)

    data_by_country.drop(columns = [variable, 'country'], inplace=True)
    data_by_country.rename(columns={'diffs': 'cap', 'year': 'ID-year'}, inplace=True)
    data_by_country['year'] = config.YEAR_DATA
    if variable == 'cap':
        data_by_country = remove_negative_values(data_by_country, 'type', config.TYPES_TO_SUMMARY)

    data_by_country = data_by_country.set_index(['year', 'ID-year', 'type'])[variable]\
        .unstack().reset_index()

    data_by_country = add_missing_columns(data_by_country)
    data_by_country = append_missing_rows(data_by_country)

    return data_by_country

def create_irnw_inst_cap_file(irena_cap_db):
    irena_cap_db.replace(config.IRENA_TO_TYPES, inplace = True)
    irena_cap_db.replace(config.COUNTRIES_TO_ABBR, inplace = True)
    irena_cap_db = irena_cap_db.groupby(by = ['country', 'year', 'type']).sum()
    irena_cap_db.reset_index(inplace= True)

    writer = pd.ExcelWriter('process_irnw_inst-cap_intermediate.xlsx', engine='xlsxwriter')

    data_for_all = get_data_for_all_sheet(irena_cap_db, 'cap')
    data_for_all.to_excel(writer, sheet_name = 'ALL', index = False)

    for country in config.ABBR:
        data_by_country = get_data_for_country_sheet(irena_cap_db, 'cap', country)
        data_by_country.to_excel(writer, sheet_name = country, index = False)

    print(f'Results saved')
    writer.save()

def create_irnw_gen_file(irena_gen_db):
    irena_gen_db.replace(config.IRENA_TO_TYPES, inplace = True)
    irena_gen_db.replace(config.COUNTRIES_TO_ABBR, inplace = True)
    irena_gen_db = irena_gen_db.groupby(by = ['country', 'year', 'type']).sum()
    irena_gen_db.reset_index(inplace= True)

    writer = pd.ExcelWriter('process_irnw_gen_intermediate.xlsx', engine='xlsxwriter')

    data_for_all = irena_gen_db.drop(columns = ['country'])
    data_for_all = data_for_all.groupby(by = ['year', 'type']).sum().reset_index()
    data_for_all = data_for_all[data_for_all['type'].isin(config.TYPES_TO_SUMMARY)]
    data_for_all.sort_values(by = ['type', 'year'], inplace=True)
    data_for_all['ID-year'] = data_for_all['year']
    data_for_all['year'] = config.YEAR_DATA
    data_for_all = data_for_all.set_index(['year', 'ID-year', 'type'])['gen']\
        .unstack().reset_index()

    data_for_all = add_missing_columns(data_for_all)
    data_for_all = append_missing_rows(data_for_all, gen=True)
    data_for_all.to_excel(writer, sheet_name = 'ALL', index = False)

    for country in config.ABBR:
        data_by_country = (irena_gen_db[(irena_gen_db['country'] == country) &
                                (irena_gen_db['type'].isin(config.TYPES_TO_SUMMARY))]).copy()
        data_by_country.sort_values(by = ['type', 'year'], inplace=True)
        data_by_country['ID-year'] = data_by_country['year']
        data_by_country['year'] = config.YEAR_DATA
        data_by_country = data_by_country.set_index(['year', 'ID-year', 'type'])['gen']\
            .unstack().reset_index()

        data_by_country = add_missing_columns(data_by_country)
        data_by_country = append_missing_rows(data_by_country, gen=True)
        data_by_country.to_excel(writer, sheet_name = country, index = False)

    print(f'Results saved')
    writer.save()

if __name__ == '__main__':
    print('Fetching and processing data')
    irena_cap_db, irena_gen_db = read_and_prepare_data()

    print('Saving capacity data')
    summarize_and_save(irena_cap_db, 'irena_cap_summary.xlsx', 'cap')

    print('Saving generation data')
    summarize_and_save(irena_gen_db, 'irena_elecgen_summary.xlsx', 'gen')

    print('Creating process_irnw_inst-cap_intermediate.xlsx file')
    create_irnw_inst_cap_file(irena_cap_db)

    print('Creating process_irnw_gen_intermediate.xlsx file')
    create_irnw_gen_file(irena_gen_db)