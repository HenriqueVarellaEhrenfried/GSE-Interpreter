# ---------------------------------------------------------------------------------------------
#   Copyright (c) Henrique Varella Ehrenfried. All rights reserved.
#   Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------


'''CLI for database module'''
from manager import Manager

import actions


manager = Manager()

@manager.command
def create_csv(files=None, directory=None, file_output='./requirements.csv', sep =';', encoding = 'utf-8'):
    '''Transform all your requirment files in a csv
    
			   PARAMS: files, directory, 
			     --files: list of files | Example: --files './example/example.feature | ./example/example2.feature'
			     --directory: a single direcotry | Example: --directory "./example'
			     --file_output: the expected file | Example: --file_output '/home/user/my_requirements.json'
			     --sep: the CSV separator token | Example: --sep '|'
			     --encoding: the econding of the result csv file | Example: --encoding 'ASCII' 
    '''
    actions.create_csv(files, directory, file_output='./requirements.csv', sep =';', encoding = 'utf-8')

@manager.command
def create_json(files=None, directory=None, file_output='./requirements.json'):
    '''Transform all your requirment files in a json

			   PARAMS: files, directory, 
			     --files: list of files | Example: --files './example/example.feature | ./example/example2.feature'
			     --directory: a single direcotry | Example: --directory "./example'
			     --file_output: the expected file | Example: --file_output '/home/user/my_requirements.json'
    '''
    actions.create_json(files, directory, file_output='./requirements.json')

@manager.command
def create_docs(files=None, directory=None):
    '''Generate HTML and PDF documentation

			   PARAMS: files, directory, 
			     --files: list of files | Example: --files './example/example.feature | ./example/example2.feature'
			     --directory: a single direcotry | Example: --directory "./example'
    '''
    actions.create_docs(files, directory)

if __name__ == "__main__":
    manager.main()
