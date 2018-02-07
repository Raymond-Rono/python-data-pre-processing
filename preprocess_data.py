# @Author: AUTHOR NAME <Raymond C. Rono><raymond dot rono at gmail dot com>
# @Date:   2017-12-31
# @Filename: preprocess_data.py
# DISTRIBUTION NOT ALLOWED

from preprocess_functions import *
from write_preprocess_data import *

#   ##      ###         ####                START OF preprocessData()             ####            ###     ##  # 

def preprocessData(list_of_raw_data_dict, config_values_dict, dict_holding_dicts_for_max_min):
    # 2. TASK B: PRE-PROCESSING DATA (35 Marks)  # Steps without pre-processing commands will be skipped
    """
    summary : code to preprocess data. Several steps are involved. step will be skipped if config command not found. several functions are called to match with the steps
    Function Name: preprocessData
    Function Use: Function will preprocess data as per rules in the config file. Steps without pre-processing commands will be skipped. Consists 4 main steps
    FunctionsCalled: Open() - In built Python function to help in opening and manipulating files (csv,txt,json)
                     DictReader() - Python function to read csv as dictionary file
                     dropNullValuesCSV() - user defined function to drop Null Values in data from CSV files
                     dropNullValuesJSON() - user defined function to drop Null Values in data from JSON files
                     OrderedDict() - Python collections for ordered dictionaries
    Argument(s) Accepted:   [list_of_raw_data_dict]: this argument contains the lists of dictionary of raw data so that it can be proccessed
                            [config_values_dict]: data dictionary containing configuration values/parameters useful in processing the data.
                            [dict_holding_dicts_for_max_min]: dictionary containing maximum and minimum for numeric columns. This will be required for numeric fields in normalization function
    Value(s) Returned: None
    """
    
    pre_processed_data = list_of_raw_data_dict # defaulting the pre_processed_data to the received data dictionary containing raw data
    
# 2.1 Missing Values (10 Marks)
    # 2.1.1: Dropping Null Values - calling function for dropping all the rows having null or NaN in a specific column(s)
    print "...checking drop nulls config command."
    if (config_values_dict["preprocess"]["missing"]).has_key("dropnull"): # checking existence of pre-processing command for dropping null values
        print "...command found now dropping nulls."
        list_column_names_to_dropnull = str(config_values_dict["preprocess"]["missing"]["dropnull"])
        pre_processed_data = dropNull(pre_processed_data, list_column_names_to_dropnull)
        print ".>>nulls dropped. "
        
    # 2.1.2: Filling Null Values - calling function for replacing null or NaN in a specific column(s) with default values
    print "...checking fill nulls config command."
    if (config_values_dict["preprocess"]["missing"]).has_key("fillnull"): # checking existence of pre-processing command for filling null field names and default values
        print "...command found now filling nulls."
        dict_column_names_to_fillnull = config_values_dict["preprocess"]["missing"]["fillnull"] # getting a dictionary containing column names and default values to pass as a parameter
        pre_processed_data = fillNull(pre_processed_data, dict_column_names_to_fillnull) 
        print ".>>nulls filled. "
        
# 2.2 Normalization (5 Marks) - calling function for normalising specified column(s)
    # 2.2.1: normalising numeric fields to between 0 and 1
    print "...checking normalise config command."
    if (config_values_dict["preprocess"]).has_key("normalise"): # checking existence of pre-processing command for list of normalised field names
        print "...command found now normalising fields."
        list_column_names_to_normalise = config_values_dict["preprocess"]["normalise"] # getting a list containing column names to be normalised
        pre_processed_data = normalise(pre_processed_data, list_column_names_to_normalise, dict_holding_dicts_for_max_min) # dict_holding_dicts_for_max_min(used to extract maximum and minimums for numeric fields)
        print ".>>normalisation done."
        
# 2.3 Data Sorting (10 Marks) - calling function to sort data with respect to specified column
    # 2.3.1: sorting data alphabetically or lowest to highest and vice versa depending on parameters in the configuration file.
    print "...checking sorting config command."
    if (config_values_dict["preprocess"]).has_key("sorting"): # checking existence of pre-processing command for the dictionary containing field names and order of sorting
        print "...command found now sorting fields."
        dict_column_names_to_sort = config_values_dict["preprocess"]["sorting"] # getting from config file a dictionary containing field names to sort and order of sorting
        pre_processed_data = sortData(pre_processed_data, dict_column_names_to_sort)
        print ".>>sorting done."
        
# 2.4 Validation (10 Marks) # This process will address both Validating debit card and Deleting entries where debit card number is invalid.       
    # 2.4.1: Validating debit card - calling function(validateDebitCard()) to check if a specified debit card is valid or not using conditions given in config file
    # 2.4.2: Removing Invalid Debit Card Entries - calling function(removeInvalidDebitCardEntries()) to remove all the rows having invalid debit card numbers.
    # The function validateDebitCard() will be called within removeInvalidDebitCardEntries() function 
    print "...checking validation config command."
    if (config_values_dict["preprocess"]).has_key("validate_card"): # checking existence of pre-processing command for validating card.    
        if (config_values_dict["preprocess"]["validate_card"]): # check if the value gives greenlight to proceed with validation. Must contain TRUE if so and FALSE otherwise.
            print "...command found and green light given."
            pre_processed_data = removeInvalidDebitCardEntries(pre_processed_data) 
            print ".>>validation done."

# 2.5 Writing preprocessed data # This process involves writing the processed data to output file defined in the config.
    print "...checking output file config command."
    if (config_values_dict.has_key("outputfile")): # checking existence of output file parameter in the configuration file.
        if (config_values_dict["outputfile"]): # ensure the file name provide is not empty
            print "...command found now writing preproccesed data to file."
            output_file_name = config_values_dict["outputfile"] # getting the name of the output file from the configuration file
            writePreprocessedData(pre_processed_data, output_file_name)
            print("Preproccessed data written to {0}...".format(output_file_name))
        else:
            print "Sorry, the key has been found but the value for outputfile key is empty. No file name has been provided in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
            sys.exit()
    else:
        print "Sorry, the key for outputfile is not found in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
        sys.exit()    

    return # # RETURNING preprocessData FUNCTION
    
#   ##      ###         ####                END OF preprocessData()             ####            ###     ##  # 

