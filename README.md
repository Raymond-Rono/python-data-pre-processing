# email: raymond dot rono at gmail dot com 
This program will read a configuration file which contains parameters of information which can be used to preprocess data in a given input file. The configuration file is in JSON format. The input data to be processed can be in comma delimited text file (csv), tab delimited text file(txt) or a json file. The program reads the data and generates meta data information about the data. It proceeds with the processing before writing the preprocessed data into the output file defined in the configuration file. The output can be in any format whether csv, txt or json.

The observation after running the program few times is that on average it took approx. 180 microseconds to pre-process 24 records and get 9 clean records. This suggests that on average it will take 7.5 microseconds per record with 17 columns. 1 million records will therefore take approximately 7.5 * 1M = 7500000 microseconds equivalent to 7.5 Seconds! Whether this is efficient will depend on coding the same in another language and comparing the results. However there is a lot of room to improve the efficiency of the code. Other observations include:
1. The decision to putg data in lists or leaving them in a dictionary before manipulating. This is one area I will want to test in the future with regards to data manipulation. Are there limits in data dictionaries or lists with regards to data that they can hold? As data grows, does the perfomance of the data structures get affected? There was the option of holding data as global variables. Not sure how this can affect the program perfomance, however this option was not used during implementation.
2. Error handling: Python uses try and catch to handle exception errors. The code attempted to trap most of the errors. However not all errors may have been captched. May be in future the program can implement a way of suprresing the minor errors so the program can be allowed to proceed for the not so serious errors. After all is said and done there is room to trap all expected errors. 
3. Scalability: This code has not been tested on multiple nodes running at the same time to see how it copes with concurrency especially with the lists and dictionaries that have been used to hold data. An interesting observation this would be.
4. Re-usability: As much as possible the program attempted to use user defined functions. One of them is getFileExtension(file_name)
was called multiple times by different functions like readRawData() and also by writePreprocessedData(). That means python is good for creating re-usable functions.
5. Suggestion is on the config file sorting key. It is suggested that the sorting values which represents the fields to sort and their order may be made flexible by making those values as dictionary of field name and order only e.g instead of {"field":"income","order":"desc"} we have {"income":"desc"}. This will accomodate more fields to be added to this parameter such that it can hold more like  {"sorting":{"income":"desc","id":"asce"}}. Same case applies for validate_card key. The user may require other fields to be validated. something like {"validate":{"debitcard":true,"phonenumber":true}} would make the field more flexible.

In conclusion and in general,  Python can be used to design large applications because of its flexibility, openess and interactive nature. However since Python is an interpreted language, it might be slower than a compiled language. But on the other hand this makes it stronger to be used for web applications since it will be relatively fast.


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
