import pandas as pd
import numpy as np
import csv
import test_helper as th

appt_list = []


# Read in appointment data from the corresponding data file.
data_file = pd.read_csv('data/RawData-03.csv', encoding='utf8')
data_file.sort_values(by=['Name', 'Postcode', 'Date', 'Start Time'], inplace=True, ascending=False)

output_appt = ''
previous_appt = ''

def create_appt(appt_row):
    appointment = [None] * 24
    
    appointment[0] = appt_row['Name']
    appointment[1] = appt_row['Postcode']
    appointment[2] = appt_row['Date of Birth']
    appointment[3] = appt_row['Reasons']    
    appointment[4] = appt_row['Ethnicity']   
    appointment[5] = appt_row['Office']  
    appointment[6] = appt_row['Date'] 
    appointment[7] = th.get_test_outcome(appt_row['Notes']) 

    return appointment


def update_appt(appt_row, count, app):

    app[count + 8] = appt_row['Date']
    app[count + 9] = th.get_test_outcome(appt_row['Notes'])

    return app


field_offset = 0
appt = None

# Loop through every appointment.
for index, row in data_file.iterrows():

     #TODO Just use name for now.
    current_appt = row['Name'].lower()
 
    if current_appt != previous_appt:
        if previous_appt != '':
            appt_list.append(appt) 

    if current_appt == previous_appt:
        appt = update_appt(row, field_offset, appt)
        field_offset += 2
    else:
        appt = create_appt(row)
        field_offset = 0
    
    previous_appt = current_appt


with open('data/consolidated.csv', 'w', newline='') as f:
     wr = csv.writer(f)
     wr.writerows(appt_list)




