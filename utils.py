from flask import request, jsonify, current_app
import os, logging
from datetime import datetime
from decimal import Decimal

#safety for os removing file (incase not there)
def remove_file(filepath):
	try:
		os.remove(filepath)
	except OSError:
		pass

#safety for os opening file (incase not there)
def open_file(path,mode):
	try:
		return os.open(path,mode)
	except FileNotFoundError:
		return jsonify({'request':'transactions', 'status': 'failed','result':'error opening tmp file saved on server side'}), 404

#whenever invalid data is encountered we want to reset the revenue and expenses
def reset_sums():
	current_app.config['grossRevenue'] = 0
	current_app.config['expenses'] = 0
	current_app.config['netRevenue'] = 0

#reset row counter of entries and change calculated state to false
def reset_entries_counter():
	current_app.config['entries'] = 0
	current_app.config['calculated'] = False

#cleanup temp file + close files
def file_cleanup(file_open,key,filepath):
	os.close(file_open)
	request.files.get(key).close()
	remove_file(filepath)


#function to check: #check: if file exists -> .csv ext -> 0<size<=16mb
def validate_file(request_files,key,filepath):
	#check "data=@any_csv_file.csv" and only 1 file is being used
	if(request_files.get(key,0) and (len(request_files.getlist(key)) == 1)):
		#filename without spaces to test for empty file names
		filename = (request_files.get(key).filename).strip()
		#valid file name
		if(filename):
			#check if csv file by checking last element in list after a split by '.'
			filename_list = (request_files.get(key).filename).split('.')
			#csv file
			if(filename_list[-1].lower() == 'csv'):
					#save file first to tmp, get size, then remove
					request_files.get(key,0).save(filepath)
					filesize = os.stat(filepath).st_size
					#non-empty files <= 16mb
					if(filesize):
						return 
					#empty file
					else:
						remove_file(filepath)
						return jsonify({'request':'transactions', 'status': 'failed','result':'input file is empty'}), 404

			#not a csv file file
			else:
				return jsonify({'request':'transactions', 'status': 'failed','result':'incorrect file extension, ensure csv file is submitted'}), 415
		#empty file name (special chars/spaces only)
		else:
			return jsonify({'request':'transactions', 'status': 'failed','result':'filename is empty, dont use special characters/only spaces when naming your csv file" '}), 400
	#incorrect CURL syntax (e.g.: too many files sent with POST)
	else:
		return jsonify({'request':'transactions', 'status': 'failed','result':'file not submitted correctly, use the following syntax: curl -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv" '}), 400

#function to check check only col A-D filled in csv
def process_csv_row(line,file_open,key,filepath):
	#remove new line char and leading/trailing white spaces in full string
	line = line.strip()
	#get rid of white spaces & empty entries for each string in the list
	list_entry = line.split(',')
	list_entry = [ent.strip() for ent in list_entry]
	
	#get index of empty columns
	empty_col = [i for i,element in enumerate(list_entry) if not element]
	#empty column cases col A-D (0-3) isnt filled, but E-Z might be (missing column entries case)
	if(0 in empty_col or 1 in empty_col or 2 in empty_col or 3 in empty_col):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		return jsonify({'request':'transactions', 'status': 'failed','result':'columns A-D are not filled properly on row '+ str(current_app.config.get('entries',0)+1)}), 422

	#get rid of all empty string entries
	list_entry[:] = [ent for ent in list_entry if ent]
	' '.join(list_entry).split()


	#ensure each row only 1st 4 columns are filled
	if(len(list_entry) == 4):
		return list_entry

	#too many row entries
	else:
		file_cleanup(file_open,key,filepath)
		reset_sums()
		return jsonify({'request':'transactions', 'status': 'failed','result':'too many column entries on row '+ str(current_app.config.get('entries',0)+1)}), 422

#function to check date field has been filled correctly (YYYY-mm-dd) and all of the same year
def verify_date(date,file_open,year_list,key,filepath):
	#process date
	format = "%Y-%m-%d"

	#here we want to make sure date is formatted correctly
	try:
		date_format = bool(datetime.strptime(date, format))
	except ValueError:
		date_format = False
	if(not date_format):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'incorrectly formatted date, format as yyyy-mm-dd'}), 422

	#check all dates are within same year
	#empty year_list, append to year_list 
	if(not len(year_list)):
		year_list.append(date.split('-')[0])
		return
	#entry not of the same year as the rest of the entries
	elif(date.split('-')[0] not in year_list):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'Please ensure all entries are from the same year'}), 422
	#same year as the rest of the entries
	else:
		return

#function to process value_type (income or expenses)
def process_type(val_type,file_open,key,filepath):
	if(val_type == 'expense'):
		return -1
	elif(val_type == 'income'):
		return 1
	else:
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'incorrectly formatted type, please specify either expense or income'}), 422

#function to process memo (check if not all numbers)
def process_memo(memo,file_open,key,filepath):
	#use ascii to check if theres at least 1 letter in this string (97 - 122 ;a-z)
	valid_memo = False
	for char in memo:
		if(ord(char)>=97 and ord(char)<=122):
			valid_memo = True
			break
	#all numbers/no letters in memo
	if(not valid_memo):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'your memo does not have any english characters (a-z), which does not make sense'}), 422
	else:
		return

#function to verify amount provided is: valid float, <=32 bits, < 2 decimal places
def process_amount(amount,file_open,key,filepath):
	#assumptions: no $ symbol infront of the values in csv file, no commas present in the amount field (e.g.: 1,23), scientific notation not valid

	#check if valid float
	invalid_amount = False
	try:
		float(amount)
	except ValueError:
		invalid_amount = True
	if(invalid_amount):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'your amount is not formatted properly. please ensure to put just the numerical value (e.g.: 50.2 or 50 or 50.79) with no $ preceeding the value'}), 422
	amount = float(amount)

	#limit amount to 32 bit
	if(abs(amount)> 0xffffffff):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'Please input a realistic value in the amount field (>32 bit number is not realistic for your income or expense)'}), 422

	#confirm amount is limited to at most 2 decimal places (51.32 makes sense, 51.323 doesnt)
	if(len(str(amount).split('.')[-1]) > 2):
		file_cleanup(file_open,key,filepath)
		reset_sums()
		reset_entries_counter()
		return jsonify({'request':'transactions', 'status': 'failed','result':'your amount has more than 2 decimal places which is not a real life money value. Please format to 2 decimal places or less (avoid scientific notation)'}), 422

	return amount

#func to update expenses, gross revenue and row entries
def update_result(net,amount):
	#expenses
	if(net == -1):
		current_app.config['expenses'] = Decimal(str(current_app.config.get('expenses',0))) + Decimal(str(abs(amount))) 
	#income
	elif(net == 1): 
		current_app.config['grossRevenue'] = Decimal(str(current_app.config.get('grossRevenue',0))) + Decimal(str(abs(amount)))

	#inc amount of row entries that doesn't have missing data
	current_app.config['entries'] = current_app.config.get('entries',0) + 1

#func to calculate net revenue, set calculated state to True, and return HTTP 200 code
def calculate_net_revenue(file_open,key,filepath):
	file_cleanup(file_open,key,filepath)
	current_app.config['netRevenue'] = current_app.config.get('grossRevenue',0) - current_app.config.get('expenses',0)
	current_app.config['calculated'] = True
	return jsonify({'request':'transactions', 'status': 'success','result':'data has been processed, send a GET request to the /report endpoint to retrieve the results'}), 200
