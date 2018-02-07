# @Author: AUTHOR NAME <Raymond C. Rono><raymond.rono@gmail.com>
# @Date:   2017-12-31
# @Filename: write_preprocess_data.py
# DISTRIBUTION NOT ALLOWED

import os.path # portable way of using operating system dependent functionality to manipulate paths #[9]
import csv  #   CSV (Comma Separated Values) is imported to be used
            #   for import and export format for spreadsheets and databases

#   ##      ###         ####                START of user defined functions              ####            ###     ##  #                   
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

def writePreprocessedData(pre_processed_data, output_file_name):
    """
    summary : code to write pre proccessed data to a file. Accepts preproccessed data and output file name and returns nothing
    Function Name: writePreprocessedData
    Function Use:   Function will write pre proccessed data to a file
    FunctionsCalled:    validateDebitCard() - user defined function to check if a given number is a valid debit card number or not
                        append() - Python built-in function to append items to a list.
                        getFileExtension() - user defined function to get the extension of the input data file
    Argument(s) Accepted:   [pre_processed_data]: this argument contains the lists of dictionary of raw/pre_processed_data data so that it can be written to a file specified in output_file
                            [output_file_name]: name(string) of the output file to write data to.
    Value(s) Returned: None: [new_pre_processed_data] data in a list of dictionaries without invalid debit card numbers in specified columns/fields(JSON format) e.g [{1,2,3},{"Ray","Peter","John"},{"5534-3534","25363","6353-454"}]  
    """

    output_file_extension = getFileExtension(output_file_name).lower() #calling user defined function to get the extension of the input data file # the output_file_extension is changed to lower case to allow for comparison below
    if (output_file_extension in ("csv","txt")):     # output_file_extension is the extension of the file and is received from getFileExtension() function
        if (output_file_extension == "txt"): # getting separators to use as delimiters for the type of output file
            separator = "\t"                 
        else:
            separator = ","
        with open(output_file_name, "wb") as ofn:
            csv_writer = csv.writer(ofn, delimiter = separator,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([key for key in pre_processed_data[0]])
            for obj in pre_processed_data:
                csv_writer.writerow([obj[key] for key in obj])
                
    elif (output_file_extension in ("json")):     # output_file_extension is the extension of the file and is received from getFileExtension() function
        pre_processed_data = json.dumps(pre_processed_data, indent=4)
        output_file_name = open(output_file_name, "w")
        print >> output_file_name, pre_processed_data
        output_file_name.close()
        
    return

#   ##      ###         ####                END OF user defined functions              ####            ###     ##  # 

