# Project structure
```
GSE-Interpreter
├── Code
│   └── GSE
│       ├── Example
│       │   └── features
│       │       ├── Allow_student_request.feature
│       │       ├── Display_request_status.feature
│       │       ├── Show_curricular_grade.feature
│       │       ├── Show_discipline_status.feature
│       │       ├── Student_adjust_aplication.feature
│       │       ├── Student_fill_intership_documents.feature
│       │       ├── Student_register_aplication.feature
│       │       └── steps
│       │           └── Test_Definition.py
│       ├── README.md
│       ├── grammar
│       │   ├── Gramática.png
│       │   ├── gse.tx
│       │   └── gse.tx.dot
│       ├── requirements.txt
│       └── src
│           ├── Report
│           │   ├── Logo-Mestrado.png
│           │   ├── Report.html
│           │   ├── config.json
│           │   ├── metrics.json
│           │   └── ufpr_alta.jpg
│           ├── __pycache__
│           │   ├── actions.cpython-37.pyc
│           │   ├── doc_gen.cpython-37.pyc
│           │   └── gse.cpython-37.pyc
│           ├── actions.py
│           ├── doc_gen.py
│           ├── gse.py
│           ├── manage.py
│           └── template
│               └── Report.html
├── Docs
│   └── Formato GSE.txt
├── LICENSE.txt
├── README.md
└── install_depedencies_ubuntu.sh
```

The directory `Code` there is all the code for this project: the grammar, tests 
for it, the interpreter of the grammar and the web project that will be used as
a questionnaire to facilitate even more the end user to use this language. 


# Setup your environment

## Setting up the Grammar reader

1. Install python 3.X.Y in your computer: [Python download page](https://www.python.org/downloads/release)

    1a. If you are using Windows, add Python's bin directory to you PATH

2. Verify if you have pip installed. If you do, go to the next stage, otherwise install it

3. Install Graphviz: [Graphviz download page](https://www.graphviz.org/download/)

    3a.  If you are using Windows, add Graphviz's bin directory to you PATH

4. Install virtualenv: ``pip install virtualenv`

5. Clone this git directory

6. Open a terminal in the root directory of this project

7. Run `cd ./Code/GSE`

8. Run `virtualenv env`

9. If you are on Windows run: `.\env\Scripts\activate` otherwise run `source ./env/bin/activate.sh`

10. Run `pip install -r requirements.txt`

And you are done !!

## Activating / Deactivating virtualenv

Whenever you want deactivate virtualenv all you have to do is run `deactivate`

If want to activate virtualenv, repeat the step 9 above.


--------

Please use virtualenv as described above.


## Help section

Docs for textX: http://textx.github.io/textX/stable/grammar/

Grammar: http://textx.github.io/textX/stable/grammar/


Hello World: http://textx.github.io/textX/stable/tutorials/hello_world/
