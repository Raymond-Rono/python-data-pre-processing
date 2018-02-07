# @Author: AUTHOR NAME <Raymond C. Rono><raymond.rono@gmail.com>
# @Date:   2017-12-31
# @Filename: preprocess_functions.py
# DISTRIBUTION NOT ALLOWED

import re   #   Python module for providing regular expression. This will allow for matching operations for patterns and strings to be searched#[2]
from itertools import groupby # Python module for providing iteration grouping for repeating digits#[1]

#   The list of strings constants which may appear in numeric fields:  chars = ['NAN','NULL'] :there is room to add char like $ etc. Will b compared in upper case
MISSING_VALUE_CONSTANTS = ['NAN','NULL'] # missing_value_constants is a list of missing value constants which can be found in input data used instead of missing values. This is utilised by dropNull() and fillNull() functions. 

COLUMNS_TO_TEST_FOR_VALIDITY = ["debitcard"] # Constant holding the name(s) of columns to test for validity. The column/field list can be expanded

#   NUMERIC_REGEX is the regular expression used to decide ifa value is numeric as per the conditions described in the assignment.
NUMERIC_REGEX = re.compile(r"(\+|-)?([0-9- ]+\.?[\.0-9-]*|\.[0-9-]+)([eE](\+|-)?[0-9-]+)?$")

#   DEBIT_CARD_REGEX is the regular expression used to decide if a given number is valid debit card number or not as per the conditions described in the assignment.
#   A debit card number must start with 4,5 or 6. Must contain exactly 16 digits. Must only consist of digits(0-9).
#   A debit card may have digits in groups of 4, separated by one hyhen "-". Must NOT use any other separtor like '','_' etc.
#   A debit card must NOT have 4 or more consecutive repeated digits
DEBIT_CARD_REGEX = re.compile(r"^([4-6])\d{15}|^([4-6])\d{3}((-{1}\d{4}){3})$")

# FORMAT_CONSTANTS_TO_STRIP is a tuple of constants which will be used to replace separators in debit card before testing for consecutive repeated digits
FORMAT_CONSTANTS_TO_STRIP = (("-",""),("",""))  # this can have longer list and can be changed to suit different conditions e.g. (("-",""),(" ",""),,("_",""))
                                                # the second item ("","") is for replace to work well otherwise it will throw an exception [replace() takes at least 2 arguments]. It has no effect in string being tested

#   ##      ###         ####                START of user defined functions              ####            ###     ##  #

def dropNull(pre_processed_data, list_column_names_to_dropnull):
    """
    summary : code to drop all the rows having null or NaN in data (pre_processed_data) with respect to specified column(s) in list(list_column_names_to_dropnull)
    Function Name: dropnull
    Function Use: Function will delete corresponding rows for those columns whose fields have missing values in the input files 
    FunctionsCalled: upper() - In built Python function which converts string to upper case
                     append() - Python built-in function to append items to a list
    Argument(s) Accepted:   [pre_processed_data] : this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through dropping null values
                            [list_column_names_to_dropnull]: this is a list of column names having missing values to be used to delete their corresponding rows. accepts one or more column names in the list
    Value(s) Returned: [new_pre_processed_data] data in a list of dictionaries with null-row-dropped-data(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]
    """
    
    new_pre_processed_data = [] # pre_processed_data list will be used to hold list of all object dictionaries for 'clean' data
    for obj in pre_processed_data:
        hasMissing = False # so that if we find one with missing value in the required field, it is flagged off
        for key in obj:
            if key in list_column_names_to_dropnull:
                # if the value, for the key in column names for checking for missing values, has missing value equal to one in constants defined, then flagged the row/object as having missing value
                if str(obj[key]).upper() in MISSING_VALUE_CONSTANTS: # MISSING_VALUE_CONSTANTS is a constant list defined above currently containing ['NAN','NULL']
                    hasMissing = True
        # add only clean rows/objects - without missing values - to new_pre_processed_data data dictionary
        if not hasMissing:
            new_pre_processed_data.append(obj)
    
    return new_pre_processed_data

def fillNull(pre_processed_data, dict_column_names_to_fillnull): #[6]
    """
    summary : code to replace null or NaN with default values in data (pre_processed_data) with respect to specified column(s) in dictionary(dict_column_names_to_fillnull)
    Function Name: fillNull
    Function Use: Function will fill missing data with default values for rows whose corresponding columns have been defined as having missing values in data input files and need to be filled
    FunctionsCalled: str() - In built Python function which typecasts text to string
    Argument(s) Accepted:   [pre_processed_data] : this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through filling null/missing values with defaults
                            [dict_column_names_to_fillnull]:is a dictionary containing column names and default values 
    Value(s) Returned: [pre_processed_data] data in a list of dictionaries with null-filled-data in(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]
    """
    
    object_count = 0 # counter for the number of objects in pre_processed_data
    for obj in pre_processed_data: # obj is an object representing each individual row of data
        for key_in_data in obj: 
            for key_in_config in dict_column_names_to_fillnull:
                # the intention is to match the key(field_name) in data with the key(field_name) in list from the config file AND also the values assigned to those keys if they match the missing value constants defined 
                if ((str(key_in_data) == str(key_in_config)) and ((str(obj[key_in_data])).upper() in MISSING_VALUE_CONSTANTS)): # MISSING_VALUE_CONSTANTS is a constant list defined above currently containing ['NAN','NULL']
                    # values to be used to replace null/missing values can be accessed from config file through the dictionary dict_column_names_to_fillnull
                    pre_processed_data[object_count][key_in_data] = str(dict_column_names_to_fillnull[key_in_config])
        object_count += 1
        
    return pre_processed_data
    
def normalise(pre_processed_data, list_column_names_to_normalise, dict_holding_dicts_for_max_min): #[6]
    """
    summary : code to normalise data (pre_processed_data) with respect to specified column(s)(list_column_names_to_normalise) contained in dictionary(dict_holding_dicts_for_max_min)
    Function Name: normalise
    Function Use:   Function whill normalize numeric data columns to between 0 and 1. It replaces data in numeric field with normalized data in the pre_processed_data list of dictionaries
                    normalised_value = ((value - minimum_of_numeric_field)/(maximum_of_numeric_field - minimum_of_numeric_field))
    FunctionsCalled: float() - Python in-built function to convert numeric data to float. Python Lambda function can be used also.
    Argument(s) Accepted:   [pre_processed_data]: this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through normalization
                            [list_column_names_to_normalise]: is a list containing column names to be normalised. It can accepts zero, one or more column names. 
                            [dict_holding_dicts_for_max_min]: is a dictionary containing maximum and minimum of the numeric fields from the input data file. maximum and minimum of the numeric fields will be used in this function
    Value(s) Returned: None: [pre_processed_data] data in a list of dictionaries with normalised data in specified fields(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]  
    """

    # loop through the records in preProcData dictionary and normalize.
    object_count = 0
    for obj in pre_processed_data:
        for key in obj:
            if key in list_column_names_to_normalise:
                # the intention is to use the formulae -> normalised_value = ((value - minimum_of_numeric_field)/(maximum_of_numeric_field - minimum_of_numeric_field))
                maximum_value_in_field = float(dict_holding_dicts_for_max_min[key]["max"])
                minimum_value_in_field = float(dict_holding_dicts_for_max_min[key]["min"])
                # if already in normal form, break and return else normalise 
                if ((maximum_value_in_field == 1) and (minimum_value_in_field == 0)):
                    break  # program will break here if the key already meets the normalization requirement.
                else:
                    diff = maximum_value_in_field - minimum_value_in_field
                    # to avoid division by zero just normalise where difference is greater than zero else divide by itself where values in list are equal and get list of ones only
                    if (diff > 0):
                        pre_processed_data[object_count][key] = (float(obj[key]) - minimum_value_in_field)/diff
                    else:
                        pre_processed_data[object_count][key] = float(obj[key])/float(obj[key])
        object_count += 1
        
    return pre_processed_data
        
def sortData(pre_processed_data, dict_column_names_to_sort): #[8]
    """
    summary : code to sort data (pre_processed_data) with respect to specified column contained in dictionary(dict_column_names_to_sort)
    Function Name: sortData
    Function Use:   Function will sort data. Data can be sorted by text (A to Z or Z to A),
                    numbers (smallest to largest and largest to smallest, dates and times(oldest to newest and newest to oldest)
                    It takes a dictionary with sorting fields and order of sorting.
    FunctionsCalled:    sorted() - Python in-built function to sort values.
                        float() - Python in-built function to convert numeric data to float. Python Lambda function can be used also.
                        lambda - Python in-built for anonymising a function
    Argument(s) Accepted:   [pre_processed_data]: this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through sorting
                            [dict_column_names_to_sort]:  A dictionary consisting of field to be sorted and its sorting order. 
    Value(s) Returned: None: [pre_processed_data] data in a list of dictionaries with sorted data in specified columns/fields(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]  
    """
    
    # testing what the user has presented as the sorting order. If not in defined scope the user will be notified to present appropriate order.
    sort_field = dict_column_names_to_sort["field"]
    if (dict_column_names_to_sort["order"] == "desc"):
        order = True
    elif (dict_column_names_to_sort["order"] == "asce"):
        order = False
    else:
        print "Sorry, the sorting order field cannot be understood. Kindly use 'asce' or 'desc' only in the configuration file. I will now exit".format(configFile)
        sys.exit()
    # using sorted function and passing the key to use as well as the order. This will sort out objects in the list with respect to dictionaries in the object based on key used
    pre_processed_data = sorted(pre_processed_data, key = lambda k: float(k[sort_field]), reverse = order)

    return pre_processed_data

def validateDebitCard(str_debit_card): #[7][4][6]
    """
    summary : code to take a string input and return if the debit card number is valid or not (TRUE if valid, FALSE if NOT).
    Function Name: validateDeditCard
    Function Use: Function will check if a given number is valid debit card number or not
    FunctionsCalled:    REGEX.match() - Python regular expression which searches a string for a match. retruns true if it matches and false otherwise
                        replace() - Python in-built string function which returns a copy of string with all occurrences of old substring old replaced by new
                        max() - Python in-built function which returns largest item in an iterable
                        len() - Python in-built function which returns the number of items of an object
                        list() - Python in-built object function which a list whose items are the same
                        Decimal() - Python in-built object fixed-point for representing values in an exact manner
    Argument(s) Accepted: [str_debit_card]: The string consisting of debit card value which needs to be tested
    Value(s) Returned: Boolean True or False. True if conditions are met, False otherwise.
    """
    # importing Decimal to be used in converting exponential debit card strings to decimal for analysis
    from decimal import Decimal # to assist in conversion # used in validateDebitCard to convert exponential strings to decimal common in text files for input data

    # this regular expression is used to test whether a number string is in exponential form. If so it needs to be converted to Decimal before being tested. Otherwise the string remains as is.
    EXPONENT_NUMERIC_REGEX = re.compile(r"(\+|-)?([0-9- ]+\.?[\.0-9-]*|\.[0-9-]+)([eE](\+|-)[0-9-]+)$")

    
    #   Check if the debit card meets conditions described below:
    #   1. A debit card number must start with 4,5 or 6. Must contain exactly 16 digits. Must only consist of digits(0-9).
    #   2. A debit card may have digits in groups of 4, separated by one hyhen "-". Must NOT use any other separtor like '','_' etc.
    #   3. A debit card must NOT have 4 or more consecutive repeated digits
    #   DEBIT_CARD_REGEX = re.compile(r"^([4-6])\d{15}|^([4-6])\d{3}((-{1}\d{4}){3})$")
    #   DEBIT_CARD_REGEX is the regular expression costant used to decide if a given number is valid debit card number or not as per the conditions described in the assignment.

    # if it matches the regex constant defined, then proceed to remove separators and test for 4 or more consecutive repeated digits
    # But before testing debit card conditions , the string must be tested first to check if it meets the basic numeric conditions neccessary for a debit card to exist as numeric
    is_valid = False # Assuming initially the debit card string is not valid. The code will be looking for an opportunity to confirm its validity and assign boolean true to is_valid variable.
                     # Until all the conditions are met, is_valid will remain False
    if NUMERIC_REGEX.match(str_debit_card): # check if debit card string is numeric and meeting the basic conditions of being considered so. The strings not meeting the condition will return false.

        # if string is in exponential form, convert it to float then to decimal then revert it back to string to allow for debit card regex testing. some debit cards especially in tabular text input files may be expressed exponentially
        if EXPONENT_NUMERIC_REGEX.match(str_debit_card): # check if in exponent form.
            num_debit_card = str(Decimal(float(str_debit_card))) #  convert to float then to decimal and revert to string 
        else: # else leave it the way it is if not exponential
            num_debit_card = str_debit_card
        # testing debit card conditions starts.
        if DEBIT_CARD_REGEX.match(num_debit_card): # is the str_debit_card matching the DEBIT_CARD_REGEX regex? DEBIT_CARD_REGEX contains 1 and 2 conditions above. (Testing condition 1 and 2 above)
            for constant in FORMAT_CONSTANTS_TO_STRIP: # currently defined FORMAT_CONSTANTS_TO_STRIP = (("-","")). This can be expanded depending on configs. 
                num_debit_card = num_debit_card.replace(*constant) # strip/remove separators from the debit card string. Remove as many constants as defined before returning the string to be tested for repeating digits
            max_len_for_repeating_digits = max(len(list(e)) for _, e in groupby(num_debit_card)) # get the maximum length for repeating digits after grouping them
            is_valid =  (max_len_for_repeating_digits < 4) # test for 4 or more consecutive repeated digits. Will return FALSE if having 4 or more consecutive repeated digits and TRUE otherwise. (Testing condition 3 above)
    return is_valid # return false to mean debit card string is not matching the regex defined hence not meeting conditions presented. It may also not be meeting even the numeric conditions let alone debit card conditions
 
def removeInvalidDebitCardEntries(pre_processed_data): #[8]
    """
    summary : code to remove all the rows having invalid debit card numbers. Accepts preproccessed data and returns data without invalid debit card entries
    Function Name: removeInvalidDebitCardEntries
    Function Use:   Function will remove all the rows having invalid debit card numbers
    FunctionsCalled:    validateDebitCard() - user defined function to check if a given number is a valid debit card number or not
                        append() - Python built-in function to append items to a list.
    Argument(s) Accepted:   [pre_processed_data]: this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be proccessed further through sorting
    Value(s) Returned: None: [new_pre_processed_data] data in a list of dictionaries without invalid debit card numbers in specified columns/fields(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]  
    """
   
    new_pre_processed_data = []
    for obj in pre_processed_data:
        debit_card_is_valid = False  # assuming the debit card is not valid as per prescribed conditions.
        for key in obj:
            # test whether we are testing values in the correct columns/fields as per the constant COLUMNS_TO_TEST_FOR_VALIDITY and also whether debit card is valid. Both must be TRUE
            if ((key in COLUMNS_TO_TEST_FOR_VALIDITY)):
                if ((validateDebitCard(str(obj[key])))): # convert to string before validating if not in string format
                    debit_card_is_valid = True # if the test is passed then debit_card_is_valid is assigned boolean value TRUE and so row/object with the debit card qualifies to be retained.
        if debit_card_is_valid: # if the debit_card_is_valid has value TRUE, its corresponding row/object can be appended to the list of those objects with valid debit cards.
            new_pre_processed_data.append(obj)

    return new_pre_processed_data
#   ##      ###         ####                END OF user defined functions              ####            ###     ##  #

