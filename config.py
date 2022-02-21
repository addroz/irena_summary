# Relative paths to original databases' main data files
IRENA_CAP_FILE_PATH = './data_original/IRENA_cap.xlsx'
IRENA_ELECGEN_FILE_PATH = './data_original/IRENA_elecgen.xlsx'

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Switzerland',
    'Sweden', 'United Kingdom']

YEARS = [2000, 2005, 2010, 2015, 2019, 2020]

YEARS_CAP = [2000, 2005, 2010, 2015, 2020]

YEAR_DATA = 2020

IRENA_TO_TYPES = {'Concentrated solar power': 'OpenSolarPV',
                  'Offshore wind energy': 'WindOff',
                  'Solar photovoltaic': 'RoofSolarPV',
                  'Mixed Hydro Plants': 'Hydro',
                  'Pumped storage': 'Other',
                  'Nuclear': 'Other',
                  'Renewable hydropower': 'Hydro',
                  'Onshore wind energy': 'WindOn'}

TYPES_TO_SUMMARY = ['Hydro', 'OpenSolarPV', 'RoofSolarPV', 'WindOn', 'WindOff']

COUNTRIES_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'HR',
    'Czechia':'CZ', 'Denmark':'DK', 'Estonia':'EE', 'Finland':'FI', 'France':'FR', 'Germany':'DE',
    'Greece':'EL', 'Ireland':'IE', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LT',
    'Luxembourg':'LU', 'Netherlands':'NL', 'Norway':'NO', 'Poland':'PL', 'Portugal':'PT',
    'Romania':'RO', 'Slovakia':'SK', 'Slovenia':'SI', 'Spain':'ES', 'Switzerland': 'CH',
    'Sweden':'SE', 'United Kingdom':'UK'}

ABBR = ['AT', 'BE', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'EL', 'IE', 'HU', 'IT',
    'LV', 'LT', 'LU', 'NL', 'NO', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES',  'CH', 'SE', 'UK']