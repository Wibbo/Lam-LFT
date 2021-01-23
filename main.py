import pandas as pd
import csv
import test_helper as th


app_list = []
final_list = []

with open('./data/current.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

    # Skip the header in the csv file.
    head = next(csv_reader)
    head.append(['Ward', 'Distance'])

    for row in csv_reader:
        row.append('Ward')
        row.append('Distance')
        app_list.append(row)

# Use comprehensions to replace blank fields and 'N/A' with No_Value.
new_list = [[field or 'No_Value' for field in row] for row in app_list]
new_list = [['No_Value' if field == 'N/A' else field for field in row] for row in new_list]

# Create a csv with default values for empty fields.
th.create_appt_csv_from_list('complete', new_list)

data_file = pd.read_csv('data/complete.csv', encoding='latin1')
data_file.sort_values(by=['Name', 'Date', 'Start Time', 'Postcode'], inplace=True, ascending=True)

postcodes = pd.read_csv('data/postcodes.csv', encoding='latin1')
wards = pd.read_csv('data/wards.csv', encoding='latin1')

output_appt = ''
previous_appt = ''

def create_appt(appt_row):

    postcode = th.get_test_postcode(appt_row['Postcode'])
    ward = th.get_ward_from_postcode(postcode, postcodes, wards)




    appointment = [None] * 14
    appointment[0] = appt_row['Office']
    appointment[1] = appt_row['Diary']
    appointment[2] = appt_row['Date']
    appointment[3] = appt_row['Start Time']
    appointment[4] = appt_row['Name']
    appointment[5] = appt_row['Email Address']
    appointment[6] = appt_row['Telephone Number']
    appointment[7] = postcode
    appointment[8] = appt_row['Date of Birth']
    appointment[9] = appt_row['Reasons']
    appointment[10] = appt_row['Ethnicity']
    appointment[11] = th.get_test_outcome(appt_row['Notes'])
    appointment[12] = ward
    appointment[13] = appt_row['Distance']

    return appointment




def update_appt(current_row, previous_row):
    index = 0

    current_row[11] = th.get_test_outcome(current_row[11])

    for col_value in current_row:
        if col_value == 'No_Value':
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

    previous = current
    previous_id = current_id

# Create a final csv file.
th.create_appt_csv_from_list('final', final_list)








