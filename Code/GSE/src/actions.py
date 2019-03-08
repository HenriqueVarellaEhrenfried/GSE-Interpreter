# ---------------------------------------------------------------------------------------------
#   Copyright (c) Henrique Varella Ehrenfried. All rights reserved.
#   Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import gse 

def create_csv(files=None, directory=None, file_output='./requirements.csv', sep =';', encoding = 'utf-8'):    
	parsed = None
	if directory:
		parsed = gse.read_files(gse.get_files_from_dir(directory))
	elif files:
		files_raw = files.split('|')
		files_treated = [x.strip() for x in files_raw]
		parsed = gse.read_files(files_treated)

	if parsed:
		gse.to_csv(parsed, file_output)
	else:
		print('\nERROR: You have to provide a valid directory or list of files\n')

def create_json(files=None, directory=None, file_output='./requirements.json'):    
	parsed = None

	if directory:
		parsed = gse.read_files(gse.get_files_from_dir(directory))
	elif files:
		files_raw = files.split('|')
		files_treated = [x.strip() for x in files_raw]
		parsed = gse.read_files(files_treated)

	if parsed:	
		gse.to_json(parsed, file_output)
	else:
		print('\nERROR: You have to provide a valid directory or list of files\n')


def create_docs(files, directory):
	parsed = None

	if directory:
		parsed = gse.read_files(gse.get_files_from_dir(directory))
	elif files:
		files_raw = files.split('|')
		files_treated = [x.strip() for x in files_raw]
		parsed = gse.read_files(files_treated)

	if parsed:
		gse.generate_docs(parsed)
	else:
		print('\nERROR: You have to provide a valid directory or list of files\n')