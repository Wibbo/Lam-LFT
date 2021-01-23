import os
import csv

def format_postcode(raw_code):
    """
    Ensures the supplied postcode is correctly formatted.
    Args:
        raw_code (): The postcode from the appointments file.
    Returns: A correctly formatted postcode.

    """
    if raw_code is None:
        return 'Unknown'

    raw_code = str(raw_code)

    raw_code = raw_code.replace(" ", "")
    code_length = len(raw_code)
    postfix = raw_code[code_length - 3:].upper()
    prefix = raw_code[:code_length - 3].upper()

    return prefix + " " + postfix


def get_ward_from_postcode(pc_to_find, postcodes, wards):


    result = postcodes.loc[postcodes['Postcode'] == pc_to_find]

    pass

def get_test_postcode(postcode):
    """
    Removes all spaces from a postcode.
    Args:
        postcode (): The postcode to be processed.
    Returns: A postcode with no spaces.
    """
    return postcode.replace(' ', '')

def get_test_outcome(test_code):
    """
    Determines the outcome of a test based on the supplied status code.
    Args:
        test_code (): The test code to process.
    Returns: A textual description of the test outcome.
    """
    test_code = str(test_code)

    if test_code is None:
        return 'Awaiting'

    # TODO Empty result fields for negative.

    if test_code == 'No_Value':
        return 'Awaiting'

    test_code = test_code.lower()

    if test_code == 'zz89':
        return 'Negative'
    elif test_code == 'bb87':
        return 'Positive'
    elif test_code == 'dna':
        return 'Did not show'
    elif test_code == 'tt89':
        return 'Void'
    elif test_code == '':
        return 'Awaiting'
    else:
        return 'Unknown'


def create_appt_csv_from_list(file_name, appt_list, header=None):
    """
    Creates an appointment based csv file from the data supplied.
    The file has a .csv extentsion and is created in the data directory.
    Args:
        file_name (): The name of the file to create.
        appt_list (): A list containing the file data.

    Returns: Nothing
    """
    dir_name = 'data/'
    file = os.path.join(dir_name, file_name + '.csv')

    with open(file, 'w', newline='') as f:
        wr = csv.writer(f)
        if header is None:
            wr.writerow(['Office', 'Diary', 'Date', 'Start Time', 'Name',
                         'Email Address', 'Telephone Number', 'Postcode',
                         'Date of Birth', 'Reasons', 'Ethnicity', 'Notes', 'Ward', 'Distance'])
        else:
            wr.writerow(header)
        wr.writerows(appt_list)