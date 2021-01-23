
def format_postcode(raw_code):
    """
    Ensures the supplied postcode is correctly formatted.
    param: raw_code: The postcode from the testing file.
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


def get_test_outcome(test_code):
    """
    Determines the outcome of a test based on the supplied status code.
    param: test_code: The test code from the testing file.
    Returns: A textual description of the test outcome.
    """
    test_code = str(test_code)

    if test_code is None:
        return 'Awaiting'

    # TODO If the result is No_Value then we should text to see if the
    # date has passed and assume a negative result if it has.
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
