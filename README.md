# Video Creator
Create videos using our data dump.

You will get a sample data dump. You have to create a video of below sample output. The whole process of creating video should be automated. The voice can be modulated using Amazon Polly.

## Sample output
https://www.youtube.com/watch?v=s52CTJiUFM8


## Technology
Text to speech: https://aws.amazon.com/polly/

## Scale of Project
Create 50 Videos automatically every day.

## Input
2 JSON files are added.
You may use any JSON beautifier tool like https://codebeautify.org/jsonviewer to parse the contents of the file and understand their structure.



### 10313_qdata.json
-------------------------
```
This file contains the questions.
Its immediate keys that will be relevant for your task are described below:
test_name  
Datatype: String
Meaning : Name of the test
sec_details 
Datatype    : Array
Meaning     : Holds the various sections in a desired order
Descendants :
sec_id 
Datatype: String
Meaning : Unique id for the section
sec_name
Datatype: Dictionary
Meaning : Has a "key-value" pair.
key
Datatype: String
Meaning : Unique code for the language of test
value
Datatype: String
Meaning : Section name in that language
sec_questions 
Datatype    : Array
Meaning     : Holds the various sections in a desired order
Descendants :  
qid
Datatype: String
Meaning:   Unique id for the question
que 
Datatype: Dictionary
Meaning:   Has a "key-value" pair.
key
Datatype: String
Meaning : Unique code for the language of question
value
Datatype    : Dictionary
Meaning     : Holds the question details
Descendants :
q_string
Datatype: String
Meaning : The HTML for the question
q_option
Datatype: Array
Meaning : Possible options. Each element of the option is a HTML string
```

### 10313_answers.json
-----------------------------

This file contains the answers for the questions listed in file 10313_qdata.json
After unsparing at https://codebeautify.org/jsonviewer, its contents aredescribed in the image file: 10313_answer_description.png



### 
![10313_answer_description](https://user-images.githubusercontent.com/677634/54827094-35743a80-4cd7-11e9-9af5-d4ba1f783e4e.png)
