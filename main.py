import pandas as pd
import csv
import test_helper as th


app_list = []
final_list = []

with open('./data/current.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

    # Skip the header in the csv file.
    next(csv_reader)

    for row in csv_reader:
        app_list.append(row)

# Use comprehensions to replace blank fields and 'N/A' with No_Value.
new_list = [[field or 'No_Value' for field in row] for row in app_list]
new_list = [['No_Value' if field == 'N/A' else field for field in row] for row in new_list]

# Create a csv with default values for empty fields.
th.create_appt_csv_from_list('complete', new_list)

data_file = pd.read_csv('data/complete.csv', encoding='latin1')
data_file.sort_values(by=['Name', 'Date', 'Start Time', 'Postcode'], inplace=True, ascending=True)


output_appt = ''
previous_appt = ''


def create_appt(appt_row):
    appointment = [None] * 12
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

    return appointment


def update_appt(current_row, previous_row):
    index = 0

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








