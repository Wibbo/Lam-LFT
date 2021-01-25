import pandas as pd
import csv
import test_helper as th
import pgeocode
from AppConfig import AppConfig

def read_config_file(ini_file_name):
    """
    Read parameters from the application config file.
    :param ini_file_name: The name of the ini file to read.
    :return: An object that represents the configuration parameters.
    """
    try:  # Changed something.
        params = AppConfig(ini_file_name)
    except FileNotFoundError as ff:
        print(ff)
        sys.exit()
    except KeyError as ke:
        print(f'Cannot find {ke} parameter in the ini file, The application cannot continue.')
        sys.exit()
    except ValueError as ve:
        print(ve)
        sys.exit()
    except Exception as e:  # noqa
        print(f'Unexpected error: has occurred, The application cannot continue.')
        sys.exit()
    else:
        return params

app_list = []
final_list = []

# Read configuration details from the INI file.
cfg = read_config_file('lam.ini')

# Initiate the geocode module (for UK).
geo_pcode = pgeocode.Nominatim(cfg.national_code)
geo_dist = pgeocode.GeoDistance(cfg.national_code)

with open('./data/current.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

    # Skip the header in the csv file.
    head = next(csv_reader)
    head.append(['Place', 'Distance', 'County'])

    for row in csv_reader:
        row.append(cfg.empty_field_default)
        row.append(cfg.empty_field_default)
        row.append(cfg.empty_field_default)

        app_list.append(row)

# Use comprehensions to replace blank fields and 'N/A' with No_Value.
new_list = [[field or cfg.empty_field_default for field in row] for row in app_list]
new_list = [[cfg.empty_field_default if field == 'N/A' else field for field in row] for row in new_list]

# Create a csv with default values for empty fields.
th.create_appt_csv_from_list('complete', new_list)

data_file = pd.read_csv('data/complete.csv', encoding='latin1')
data_file['Date'] = pd.to_datetime(data_file['Date'], dayfirst=True)
data_file.sort_values(by=['Name', 'Date', 'Start Time', 'Postcode'], inplace=True, ascending=True)

#data_file['Postcode'].apply(lambda x: th.format_postcode(x, cfg.empty_field_default))

output_appt = ''
previous_appt = ''

def create_appt(appt_row):

    postcode = th.format_postcode(appt_row['Postcode'], cfg.empty_field_default)
    geo_data_for_appoinment = geo_pcode.query_postal_code(postcode)


    #a = geo_pcode.query_postal_code('SW22 2ET')
    #b = geo_pcode.query_postal_code('SW2 2AU')

    # distance_from_test_centre = geo_dist.query_postal_code('B64 5QQ', 'DY2 0AJ')

    appointment = [None] * 15
    appointment[0] = appt_row['Office']
    appointment[1] = appt_row['Diary']
    appointment[2] = appt_row['Date']
    appointment[3] = appt_row['Start Time']
    appointment[4] = appt_row['Name']
    appointment[5] = appt_row['Email Address']
    appointment[6] = appt_row['Telephone Number']
    appointment[7] = appt_row['Postcode']
    appointment[8] = appt_row['Date of Birth']
    appointment[9] = appt_row['Reasons']
    appointment[10] = appt_row['Ethnicity']
    appointment[11] = th.get_test_outcome(appt_row['Notes'])
    appointment[12] = geo_data_for_appoinment['place_name']
    appointment[13] = appt_row['Distance']
    appointment[14] = geo_data_for_appoinment['county_name']

    return appointment




def update_appt(current_row, previous_row):
    index = 0


    current_row[11] = th.get_test_outcome(current_row[11])
    # current_row[7] = th.format_postcode(current_row[7], cfg.empty_field_default)


    postcode = th.format_postcode(current_row[7], cfg.empty_field_default)
    geo_data_for_appoinment = geo_pcode.query_postal_code(postcode)
    current_row[14] = geo_data_for_appoinment['county_name']

    for col_value in current_row:
        if col_value == cfg.empty_field_default:
            current_row[index] = previous_row[index]
        index += 1

    return current_row

appt = None
appt_count = 0

current = None
previous = None
current_id =None
previous_id = None

# Loop through every appointment.
for index, row in data_file.iterrows():
    #TODO Just use name for now.
    current_id = row['Name'].lower()
    current = row

    if appt_count == 0:
        appt = create_appt(row)
        final_list.append(appt)
    else:
        if current_id == previous_id:
            appt = update_appt(current, previous)
        else:
            appt = create_appt(current)

        final_list.append(appt)

    appt_count += 1

    previous = appt
    previous_id = current_id

# Create a final csv file.
th.create_appt_csv_from_list('final', final_list)








