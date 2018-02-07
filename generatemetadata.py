# @Author: AUTHOR NAME <Raymond C. Rono><raymond dot rono at gmail dot com>
# @Date:   2017-12-31
# @Filename: generatemetadata.py
# DISTRIBUTION NOT ALLOWED

from collections import OrderedDict #   This will help to order dictionary elements in a certain order
import csv  #   CSV (Comma Separated Values) is imported to be used
            #   for import and export format for spreadsheets and databases
import os.path # portable way of using operating system dependent functionality to manipulate paths #[9]
import json #   JSON (JavaScript Object Notation) module for data interchange with JSON files
import re   #   Python module for providing regular expression. This will allow for matching operations for patterns and strings to be searched#[2]

#   The list of strings constants which may appear in numeric fields:  chars = ['NAN','NULL'] :there is room to add char like $ etc. Will b compared in upper case
MISSING_VALUE_CONSTANTS = ['NAN','NULL'] # missing_value_constants is a list of missing value constants which can be found in input data used instead of missing values. This is utilised by dropNull() and fillNull() functions. 

#   NUMERIC_REGEX is the regular expression used to decide ifa value is numeric as per the conditions described in the assignment.
NUMERIC_REGEX = re.compile(r"(\+|-)?([0-9- ]+\.?[\.0-9-]*|\.[0-9-]+)([eE](\+|-)?[0-9-]+)?$")


#   ##      ###         ####                START of user defined functions              ####            ###     ##  #

def removeMissingVars(list_of_values):
    """
    summary : code to removes missing variable constants in a list of values
    Function Name: removeMissingVars
    Function Use: Function will remove missing variable constants in a list of values before being processed
                    Utilizes 'MISSING_VALUE_CONSTANTS' constants which is a list of known missing values constants enumerated above  - msngValConstants = ['NAN','NULL','']
    FunctionsCalled: None
    Argument(s) Accepted: [list_of_values]: The string consisting of list of arguments/values. May contain NaN, Null etc which needs to be filtered
    Value(s) Returned: [new_list_of_values]: New List without missing value constants like NaN, Null etc. 
    """
    
    new_list_of_values = [e for e in list_of_values if (str(e).upper() not in MISSING_VALUE_CONSTANTS)] # all elements are converted to upper case string to match the case of chars
    return (new_list_of_values)

def getFieldType(list_of_values): #[3]
    """
    summary : code which accepts a list of values and determines type whether numeric or string
    Function Name: getFieldType
    Function Use: Function will test whether a list is composed of numeric elements or string elements. uses 'number_regex' to match numeric
    FunctionsCalled: removeMissingVars()- user defined function to strip missing constants variables like NaN, Null
                    str() - Python in built function for manipulating strings
                    REGEX.match() - Python regular expression which searches a string for a match. retruns true if it matches and false otherwise
                    all() - will Return True where any element in the iterable is boolean true
    Argument(s) Accepted: [list_of_values]: The string consisting of list of arguments/values to be tested. May contain NaN, Null etc which needs to be filtered
    Value(s) Returned: [str_type]: String ("numeric"/"string") indicating whether numeric or string   
    """
    
    new_list_of_values = removeMissingVars(list_of_values) # call removeMissingVars() to strip missing constants variables
    if all(NUMERIC_REGEX.match(str(e)) for e in new_list_of_values): # test if matching numeric regex. If all returns true then it is numeric else if at least one doesn't then string 
        str_type = "numeric"
    else:
        str_type = "string"
    return str_type

def getListSummary(name_of_field, list_of_values):
    """
    summary : code to extract summary information for list of values
    Function Name: getListSummary
    Function Use: Function will retrieve summary information like maximum, minimum
    FunctionsCalled:    removeMissingVars() - user defined function to strip missing constants variables like NaN, Null
                        getFieldType() - 
                        max() - Python in built function which returns the maximum value in a list of values
                        min() - Python in built function which returns the minimum value in a list of values
                        len() - Python in built function which returns the length of a given string
                        set() - Python in built function which returns the unique ordered values of a list.
    Argument(s) Accepted:   [list_of_values]: The string consisting of list of arguments/values. May contain NaN, Null etc which needs to be filtered
                            [name_of_field]: The name of the field/column which is bein summarised
    Value(s) Returned:  [str_summary_dict]: A dictionary of field summary information (name, type, max, min, uniquevals)
                        [dict_to_hold_max_min_for_column]: A dictionary containing the Minimum(min) and Maximum(max) values only for easy accessing later on.
    """
    
    dict_to_hold_max_min_for_column = {} # dictionary that will hold minimum and maximum values for numeric fields to be used for normalization e.g {"id":{"Max" : 24, "Min" : 1}, "age":{"Max" : 66, "Min" : 22}}
    str_summary_dict = OrderedDict() # dictionary that will hold fields summary information for meta data dictionary
    str_summary_dict["name"] = name_of_field
    str_summary_dict["type"] = getFieldType(list_of_values) # field type
    if (str_summary_dict["type"] == "numeric"):
        new_list_of_numeric_values = removeMissingVars(list_of_values) # strip the list of NaN, Null etc - get numeric only
        str_summary_dict["min"] = min(new_list_of_numeric_values)
        str_summary_dict["max"] = max(new_list_of_numeric_values)
        dict_to_hold_max_min_for_column = {"max" : max(new_list_of_numeric_values), "min" : min(new_list_of_numeric_values)} # dict_to_hold_max_min_for_column useful in normalisation
        
    else:
        str_summary_dict['uniquevals'] = len(set(list_of_values)) # set() to produce unique ordered list before getting the length
        
    return str_summary_dict, dict_to_hold_max_min_for_column

def readRawData(input_file):
    """
    summary : code to read data from the data input file
    Function Name: readRawData
    Function Use: Function will read data from the data input file irrespective of whether it is json, text or csv.
    FunctionsCalled:    Open() - In built Python function to help in opening and manipulating files (csv,txt,json)
                        append() - Python function to append items to a list, keys() - Python function to get keys from dictionary
                        DictReader() - Python function to read csv as dictionary file, append() - Python function to append items to a list
                        OrderedDict() - Python collections for ordered dictionaries
                        getFileExtension() - user defined function to get the extension of the input data file
    Argument(s) Accepted: [input_file] - string containing the file name of the input data e.g bank-data.csv.
    Value(s) Returned: [data_dict]: data dictionary containing dictionary of raw data, format type and list of field names.
    """

    """ More comments ''
    inputFile is a global varaiable that has already been assigned at readConfig() having input data file name
    Depending on whether the file is comma delimited, it has to be to defined.
    list_of_field_names is an list used to hold list of header names/field names.
    Data will be extracted and stored in data dictionary awaiting proccessing.
    After reading, the extracted summary information will be appended to the dictionary data_dict.
    """

    data_dict = {}
    list_of_field_names = [] # list variable to hold list of field names. A global variable defined in readConfig()
    
    input_file_extension = getFileExtension(input_file).lower() #calling user defined function to get the extension of the input data file # the input_file_extension is changed to lower case to allow for comparison below
    
    if (input_file_extension in ("csv","txt")):     # input_file_extension is the extension of the file and is received from getFileExtension() function
        data_dict["type"] = "tabular"               # file format type
        if (input_file_extension == "txt"):
            data_dict["sep"] = "\t"                 # JSON file has no separators and therefore no need for sep key
        else:
            data_dict["sep"] = ","
            
        list_of_raw_data_dict = []
        with open(input_file,"rb") as f:            # input_file is an inherited parameter from calling function. the intention is to read csv or txt data input file
            raw_data = csv.DictReader(f, delimiter = data_dict["sep"])
            list_of_field_names = [field_name for field_name in raw_data.fieldnames] # list_of_field_names will be used to hold list of Field Names
            for row in raw_data:
                list_of_raw_data_dict.append(row)
                
    elif(input_file_extension == "json"):           # JSON file is opened and contents read to determine data and fields. the intention is to read json data input file
        data_dict["type"] = "json"                  # file format type
        with open(input_file,"r") as f:             # input_file is an inherited parameter from calling function
            list_of_raw_data_dict = json.load(f)    # Passing the file handler to the json loading function.
            for obj in list_of_raw_data_dict:
                for key in obj:
                    if(key not in list_of_field_names): list_of_field_names.append(key) # list_of_field_names will be used to hold list of Field Names
    else:
        print "Sorry, the file you provided '{0}' has unrecognizable extension!. Please use a configuration file with json or csv or txt extension for this program. I will now exit".format(inputFile)
        sys.exit()
        
    data_dict["list_of_field_names"] = list_of_field_names 
    data_dict["list_of_raw_data_dict"] = list_of_raw_data_dict
    
    return data_dict  # returning dictionary data containing dictionary of raw data, format type and list of field names.

def getFileExtension(fileName):
    """
    summary : code to get the extension of a file name
    Function Name: getFileExtension
    Function Use: Function which gets the extension of the input data   `file so that appropriate configurations are applied
    FunctionsCalled: Python library os.path.splitext () to split text
    Argument(s) Accepted: [fileName]: The string of file name or absolute path to check.
    Value(s) Returned: [fileExt]: A string of file extension e.g csv, json etc.
    """

    fileExt = os.path.splitext(fileName)[1][1:].strip()
    return fileExt
#   ##      ###         ####                END OF user defined functions              ####            ###     ##  # 

#   ##      ###         ####                START OF readConfig()                       ####            ###     ##  #                   

def readConfig(configFile):
    """
    summary : code to read configuration file and store data in a dictionary.
    Function Name: readConfig
    Function Use: Function will read and extract keys and values from the configuration file.
    FunctionsCalled:json.load() - Python Json function to load json files          
    Argument(s) Accepted: configFile: File string name to read and extract keys and values from
    Value(s) Returned: [config_values_dict] - data dictionary containing configuration values/parameters
    """
    
#   The file length needs to at least have length greater than zero.
    try:
        if not configFile:
            print "Sorry, you must have forgoten to provide a configuration file. It is important in order to run this program. The program will not proceed. "
            sys.exit()
    except OSError ,e:
        print "Sorry(opening file), something went wrong in attempting to read the file because of '{0}'. Kindly sort this before proceeding. ".format(e.message)
        sys.exit()
        
#   The configFile is parsed. Raise an exception if value for the configFile is not a json file
    try:
        with open(configFile) as config_file:
            config_values_dict = json.load(config_file) #extracting configuration keys and values from config file and storing in a dictionary called configValues
    except IOError:
        print "Sorry, the file you provided '{0}' does not have a json extension!. Please use a configuration file with json extension for this program. I will now exit".format(configFile)
        sys.exit()

    return config_values_dict # returning a data dictionary with configuration values

#   ##      ###         ####                END OF readConfig()             ####            ###     ##  # 

#   ##      ###         ####                START OF readData()             ####            ###     ##  # 

def readData(input_file): #[5][6]
    """
    summary : code to read data from the input data file and summary information.
    Function Name: readData
    Function Use: Function will read data from the input data file and summary information. Data read is stored in columnar manner and stored as two dimensional list. It is more of data pivoting
    FunctionsCalled: Open() - In built Python function to help in opening and manipulating files (csv,txt,json)
                     len() - Python function to get length of list
                     range() - Python function to iterate items in given range
                     append() - Python function to append items to a list, keys() - Python function to get keys from dictionary
                     readRawData() - user defined function to read raw data and store them in a dictionary. It returns a dictionary and accepts no argument
    Argument(s) Accepted:   [input_file]: string containing the file name of the input data e.g bank-data.csv.
    Value(s) Returned:      [data_dict]: data dictionary containing dictionary of raw data, summary information of the raw data like number of entries and
                            [list_of_list_of_values]: list of list of values(two dimensional list). This has data in columnar manner e.g first list contains IDs only, second list first_names only , third age only and so on.
                            Example of list_of_list_of_values derived: [[1,2,3],["Ray","Peter","Sim"]["22","44","30"]]
    """

    """ More comments ''
    list_of_field_names is a list of column headings for CSV or unique keys for JSON
    list_of_list_of_values is an list of lists used to hold lists of individual column values.
    Values will be held in individual lists for manipulation. They will be extracted columnwise
    object_count will help in tracking row/record numbers and will be initialized.
    object_count will be incremented to get the latest count
    After reading, the extracted summary information will be appended to the dictionary dataDict file.
    NOTE: assigning of list names and values - this is designed to match indexes of field lists.
    e.g if in the list_of_field_names, ID is index 5, then all the list of values for ID will be in index 5 in the list_of_list_of_values.
    If first_name is index 1 in list_of_field_names, then all the values for first_names will be in index 1 in the list_of_list_of_values
    This will be useful during generation of metadata. see function generateMetadata()
    """

    data_dict = readRawData(input_file) # calling user defined function readRawData() to get the list of raw data dict, format type, list of field names
    raw_data = data_dict["list_of_raw_data_dict"]
    list_of_field_names = data_dict["list_of_field_names"]
    list_of_list_of_values = [[] for i in range(len(list_of_field_names))] # list_of_list_of_values is a two dimensional list for storing lists of values per column
    object_count = 0
    for obj in raw_data:
        for key in obj.keys():
            list_of_list_of_values[list_of_field_names.index(key)].append(obj[key]) # this is designed to match field indexes. see 'assigning of list names and values' note above
        object_count += 1
    data_dict["numentries"] = object_count
    data_dict["numfields"] = len(list_of_field_names)
    
    return data_dict, list_of_list_of_values
    
#   ##      ###         ####                END OF readData()              ####            ###     ##  #

#   ##      ###         ####                START OF generateMetadata()             ####            ###     ##  # 

def generateMetadata(config_values_dict, data_dict, list_of_list_of_values):
    """
    summary : code to generate metadata from from the input data information.
    Function Name: generateMetadata
    Function Use: Function will generate metadata from from the input data information.
    FunctionsCalled: Open() - In built Python function to help in opening and manipulating files (csv,txt,json)
                     json.dumps() - Python Json function to write and read a json file
                     OrderedDict() - Python collections for ordered dictionaries
                     testIfNumericText() - user defined function to test if numeric text
                     numericTypeSummary() - user defined function which extracts summary information for numeric fields
                     stringTypeSummary() - user defined function which extracts summary information for string/text fields
                     has_key() - Python Json function to check whether dictionary has key
    Argument(s) Accepted:   [data_dict]: data dictionary containing dictionary of raw data, summary information of the raw data like number of entries
                            [list_of_list_of_values]: list of list of values(two dimensional list). This has data in columnar manner e.g first list contains IDs only, second list first_names only , third age only and so on.
    Value(s) Returned: [meta_data_dict]: dictionary for holding meta data information
    """
    
    # declare and initilaize a dictionary meta_data_dict that will be used to hold metadata information
    meta_data_dict = OrderedDict() #  An ordered dictionary 'meta_data_dict' for holding meta data information
    meta_data_dict["filename"] =  str(config_values_dict["inputfile"])

    # format_dict is an ordered dictionary used to hold format summary details.
    format_dict = OrderedDict()
    format_dict["type"] = data_dict["type"]
    if data_dict.has_key("sep"): format_dict["sep"] = data_dict["sep"] # checking whether dictionary has separator key. JSON file has no separators and therefore no need for sep key

    meta_data_dict["format"] =  format_dict
    meta_data_dict["numentries"] =  data_dict["numentries"]
    meta_data_dict["numfields"] =  data_dict["numfields"]

    """ Building fields summary -   list_of_field_summary is a list of dictionaries containing summary of fields. meta_file_dict["fields"] is a list of dictionaries.
                                    It will be used to temporarily hold data that will be assigned to meta_data_dict['fields']
                                    """
    list_of_field_summary = [] #  list of dictionaries for holding summary of fields

    # Each field summary is an ordered dictionary field_summary_dict
    field_summary_dict = OrderedDict() #  declaring and initializing dictionary variable for holding separately name, type, minimum, maximum, uniqueval values of lists of data.

    list_of_field_names = data_dict["list_of_field_names"]

    dict_holding_dicts_for_max_min = {}    # This dictionary is for holding field name, maximum and minimum values for easier access later on.
    for lst in list_of_field_names:
        field_summary_dict, dict_to_hold_max_min_for_column = getListSummary(lst, list_of_list_of_values[list_of_field_names.index(lst)]) # the index had been designed to match in both lists. see readData() function
        list_of_field_summary.append(field_summary_dict) #appending each dictionary of summary to the list list_of_field_summary
        if (dict_to_hold_max_min_for_column): dict_holding_dicts_for_max_min[lst] = dict_to_hold_max_min_for_column # passing the values to dict_to_hold_max_min_for_column which is for holding field name, maximum and minimum values for easier access later on.
        
    # appending the information now to the main meta file dictionary
    meta_data_dict["fields"] =  list_of_field_summary
    
    return meta_data_dict, dict_holding_dicts_for_max_min  # returning a dictionary containing meta data of the input data file and dictionary holding maximum and minimun values of numeric columns to be used in normalisation

#   ##      ###         ####                END OF generateMetadata()             ####            ###     ##  # 

