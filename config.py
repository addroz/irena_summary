# Relative paths to original databases' main data files
IRENA_CAP_FILE_PATH = './data_original/IRENA_cap.xlsx'
IRENA_ELECGEN_FILE_PATH = './data_original/IRENA_elecgen.xlsx'

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Switzerland', 'Czechia', 'Germany', 'Denmark', 'Estonia',
    'Greece', 'Spain', 'Finland', 'France', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania',
    'Luxembourg', 'Latvia', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia',
    'Slovakia', 'United Kingdom']

YEARS = [2000, 2005, 2010, 2015, 2019, 2020]

YEARS_CAP = [2000, 2005, 2010, 2015, 2020]

YEAR_DATA = 2020

IRENA_TO_TYPES = {'Concentrated solar power': 'Other',
                  'Offshore wind energy': 'WindOff',
                  'Solar photovoltaic': 'RoofSolarPV',
                  'Mixed Hydro Plants': 'Hydro',
                  'Pumped storage': 'Other',
                  'Nuclear': 'Other',
                  'Renewable hydropower': 'Hydro',
                  'Onshore wind energy': 'WindOn'}

TYPES_TO_SUMMARY = ['Hydro', 'OpenSolarPV', 'RoofSolarPV', 'WindOn', 'WindOff']

COUNTRIES_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'HR', 'Czechia':'CZ',
    'Denmark':'DK', 'Estonia':'EE', 'Finland':'FI', 'France':'FR', 'Germany':'DE', 'Greece':'EL',
    'Ireland':'IE', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LT', 'Luxembourg':'LU',
    'Malta':'MT', 'Netherlands':'NL', 'Norway':'NO', 'Poland':'PL', 'Portugal':'PT', 'Romania':'RO',
    'Slovakia':'SK', 'Slovenia':'SI', 'Spain':'ES', 'Sweden':'SE', 'United Kingdom':'UK',
    'Switzerland': 'CH'}

ABBR = [COUNTRIES_TO_ABBR[country] for country in COUNTRIES]

EMPTY_ROWS_TO_ADD = [(2020,	1960), (2020, 1965), (2020, 1970), (2020, 1975), (2020, 1980),
    (2020, 1985), (2020, 1990), (2020, 1995), (2020, 2000), (2020, 2005), (2020, 2010),
    (2020, 2015), (2020, 2020), (2025, 2025), (2030, 2030), (2035, 2035), (2040, 2040),
    (2045, 2045), (2050, 2050), (2055, 2055), (2060, 2060), (2065, 2065), (2070, 2070),
    (2075, 2075), (2080, 2080), (2085, 2085), (2090, 2090), (2095, 2095), (2100, 2100)]