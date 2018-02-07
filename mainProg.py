# @Author: AUTHOR NAME <Raymond C. Rono><raymond.rono@gmail.com>
# @Date:   2017-12-31
# @Filename: mainProg.py
# DISTRIBUTION NOT ALLOWED

import sys  #   System-specific parameters and functions.#[1]
            #   This module will provide access to some variables used or maintained
            #   by the interpreter and to functions that interact with the interpreter.
from datetime import datetime # Python module for manipulating dates and times

from generatemetadata import *
from preprocess_data import *

#   ##      ###         ####                START OF main() and sys             ####            ###     ##  # 
           
def main(configFile):
    start_time = datetime.now() # getting the start time to be used in calculating time of doing the task
    print("Hi, Welcome to the Data Pre-Processing tool. \nStarting the pre-processing at {0}..." .format(start_time)) 
    
# 1. TASK A: GENERATING METADATA (15 Marks)
    # calling function readConfig(). get the configuration values from the data dictionary (config_values_dict) which is returned from readConfig
    if (configFile): # ensure the config file name provided is not empty
        print("Config file found. Will extract dict of config keys and values...")
        config_values_dict = readConfig(configFile)
        print("Dict of config keys and values extracted. Now onto reading data...")
    else:
        print "Sorry, the config file name has not been provide '{0}'. Kindly provide the required parameters. I will now exit".format(configFile)
        sys.exit()          

    # calling function readData(). passing input_file_name parameter to the readData() function so that it can be used to read data. readData() reads input data file and retrieves main summary information
    if (config_values_dict.has_key("inputfile")): # checking existence of inputfile file parameter in the configuration file.
        if (config_values_dict["inputfile"]): # ensure the inputfile file name provided is not empty
            input_file_name = str(config_values_dict["inputfile"]) # getting the name of the inputfile file from the configuration file for outputting the metadata
            data_dict, list_of_list_of_values = readData(input_file_name)
            print("Data read. Next is metadata generation ...")
        else:
            print "Sorry, the inputfile key has been found but the value for inputfile key is empty. No file name has been provided in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
            sys.exit()
    else:
        print "Sorry, the key for inputfile is not found in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
        sys.exit()       

    
    # calling function generateMetadata(). Dictionary 'meta_data_dict' will be used to hold metadata information. generateMetadata() generates metadata from from the input data information.
    # two objects are received: meta_data_dict which is a dictionary containing meta data and dict_holding_dicts_for_max_min which is a dictionary containing maximum and minimum values for numeric columns only.
    meta_data_dict, dict_holding_dicts_for_max_min = generateMetadata(config_values_dict, data_dict, list_of_list_of_values) 
    print("MetaData dict generated. Looking for metafile to write to ...")
    
    # after meta_data_dict dictionary has been generated, the data will be dumped into a json File
    # Writing metadata # This process involves writing the metadata information to metadata file defined in the configuration file.
    if (config_values_dict.has_key("metafile")): # checking existence of metadata file parameter in the configuration file.
        if (config_values_dict["metafile"]): # ensure the metadata file name provided is not empty
            metadata_file_name = str(config_values_dict["metafile"]) # getting the name of the metadata file from the configuration file for outputting the metadata            meta_data = json.dumps(meta_data_dict, indent = 4)
            meta_data = json.dumps(meta_data_dict, indent = 4)
            file_buffer = open(metadata_file_name, "w")
            print >> file_buffer, meta_data
            file_buffer.close()
            print("MetaData info written to {0}. Proceeding to data pre-proccessing... ".format(metadata_file_name))
        else:
            print "Sorry, the metadata key has been found but the value for metadata key is empty. No file name has been provided in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
            sys.exit()
    else:
        print "Sorry, the key for metadata is not found in the configuration file '{0}'. Kindly provide it in the appropriate location. I will now exit".format(configFile)
        sys.exit()    
    
# 2. TASK B: PRE-PROCESSING DATA (35 Marks)
    # calling function preprocessData() with arguments. pre-processing data will require the list of raw data in dictionaries, configuration parameters and dictionary holding maximum and minimun for numeric columns. 
    preprocessData(data_dict["list_of_raw_data_dict"], config_values_dict, dict_holding_dicts_for_max_min) # dict_holding_dicts_for_max_min (maximum and minimum) will be required for numeric fields in normalization function
    stop_time = datetime.now()
    time_diff = stop_time - start_time
    print("Completed the pre-processing at {0}...".format(stop_time))
    print("Started   the pre-processing at {0}..." .format(start_time))
    print("The pre-processing took approx.[H:MM:SS.MS] {0}...".format(time_diff))
    print "Thank you for utilising me in your pre-processing needs."
    print "See you soon again. Cheers!"

    return # # RETURNING MAIN FUNCTION

if __name__ == '__main__':
    if(len(sys.argv)>1):
        configFile = sys.argv[1]
    else:
        configFile = "config.json"
    main(configFile)
    
#   ##      ###         ####                END OF main() and sys             ####            ###     ##  # 
    """
    REFERENCES:
    [1]. https://docs.python.org/2/library/ Accessed 21/11/2017
    [2]. https://www.regular-expressions.info Accessed 21/11/2017
    [3]. http://www.rexegg.com/ Accessed 20/11/2017
    [4]. https://stackoverflow.com/questions/21068074/python-credit-card-validation-code Accessed 22/11/2017
    [5]. Lecture Notes by Prof Amir 
    [6]. Lecture Notes by Prof Amir and Mandar
    [7]. Advanced Regex Lectures by Prof Amir, Mandar 
    [8]. Introduction to Higher Order(Functional Programming) (Python) Lectures by Prof Amir , Mandar 
    [9]. Python, H., & Statements, C. The Python Quick Syntax Reference.
    [10]. 
    """
