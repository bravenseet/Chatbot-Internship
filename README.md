# Internal Chatbot
An chatbot template that allows for reference of documentation in a WebUI interface
This project was created for my internship at GAO Capital. The purpose of this project was to help integrate new interns into the company by letting them use a chatbot to ask questions.

# Downloading and usage
Download all files from the Github and create the following files:
* "InternManualFormatted.docx" file (case-sensitive) and reference the explanation of extracting data below
* "db" file which will be used to store vector data
* .env and virtualenv file to store environment variables like CohereRerank API key (optional but highly recommended)

extract.py & InternManualFormatted.docx
-
The "InternManualFormatted.docx" is to be written in a certain format for extract.py to properly extract and filter the data into its respective classes

* ```<heading>``` is the name of the project
* ```<desc>``` is the description of the project
* ```<sub>``` are the subheadings of each project
* ```*``` are the pointers, which contain the bulk of the information retrieved and given to the LLM 

Example:
```
<heading>Introduction
<desc>This is a document about the writing format
<sub>Basics
* README.md is the documentation for the code
* guide.docx will contain your content
```

**extract.py** takes the data from guide.docx and filters it nicely into Python dictionaries, which will then be grouped all together in a Python list.

mainMemory.py
-
This file is the **backend code for the LLM to run on**. It can be run on its own in the command prompt. The main usage of this file is to be linked to the serverST.py file to be displayed as WebUI

When run on its own, mainMemory.py is used to convert the list of Dictionaries into a list of Documents, which will be embedded and stored locally in "./db" folder as vector data.

Explanation of each function is in the Python file itself.

serverST.py
-
This file acts as the frontend where streamlit will let the user interact with the LLM through a WebUI.

## Usage
Activate the virtualenv and do the following command ```pip install -r /path/to/requirements.txt```

When all files are downloaded and created as mentioned earlier:
1. Run ```python mainMemory.py``` in cmd using virtualenv
2. Once ./db has the vectorstore, run ```streamlit run serverST.py``` in cmd
3. The website should be hosted at ```http://localhost:8501/```
