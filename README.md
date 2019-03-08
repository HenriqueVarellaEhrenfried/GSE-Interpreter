# Project structure
```
Grammar_GSE/
├── Code
│   ├── GSE
│   │   ├── examples
│   │   │   ├── example2.feature
│   │   │   ├── example.feature
│   │   │   ├── example.feature.dot
│   │   │   ├── example.hello
│   │   │   └── example.hello.dot
│   │   ├── grammar
│   │   │   ├── Gramática.png
│   │   │   ├── gse.tx
│   │   │   └── gse.tx.dot
│   │   ├── Modelagem.md
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── src
│   │       ├── actions.py
│   │       ├── gse.py
│   │       ├── manage.py
│   │       └── __pycache__
│   │           ├── actions.cpython-37.pyc
│   │           └── gse.cpython-37.pyc
│   └── questionnaire
│       ├── package.json
│       ├── package-lock.json
│       ├── public
│       │   ├── favicon.ico
│       │   ├── index.html
│       │   └── manifest.json
│       ├── README.md
│       └── src
│           ├── App.css
│           ├── App.js
│           ├── App.test.js
│           ├── environment.js
│           ├── i18n.js
│           ├── index.css
│           ├── index.js
│           ├── logo.svg
│           ├── Pages
│           │   └── Questionnaire.js
│           └── registerServiceWorker.js
├── Docs
│   └── Formato GSE.txt
├── LICENSE
└── README.md
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

Docs for textX: http://www.igordejanovic.net/textX/grammar/

Grammar: http://www.igordejanovic.net/textX/grammar/


Hello World: http://www.igordejanovic.net/textX/tutorials/hello_world/
