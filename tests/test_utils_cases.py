from pytest_cases import parametrize, parametrize_with_cases, case
import os
########################### HAPPY CASES TESTCASES #####################################################
#regular data (happy case)
csv_testcase_1 = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
['2020-07-04',' Income',40, ' 347 Woodrow'],
['2020-07-06',' Income',15, '  219 Pleasant'],
['   2020-07-12',' income',35, ' Blackburn St.'],
['2020-07-12','  Expense',27.5, ' Repairs']]
#leading 0s (happy case)
csv_testcase_2 = [['    2020-07-01   ','expense', 00018.77, 'Fuel'],
['2020-07-04',' Income',40, ' 347 Woodrow'],
['2020-07-06',' Income',15, '  219 Pleasant'],
['   2020-07-12',' income',0035.0, ' Blackburn St.'],
['2020-07-12','  Expense',0027.5, ' Repairs']]

#regular expenses/revenue (happy case)
expenses_testcase_1 = [11.11,90.12,80,99.11,10.10]
grossRevenues_testcase_1 = [10.34,100.23,180.11,32.11,10.44]

#regular expenses/revenue (happy case) negatives and 0s thrown in
expenses_testcase_2 = [11.11,90.-12,80,99.11,10.10,0]
grossRevenues_testcase_2 = [10.34,-100.23,-180.11,32.11,10.44,0.00]

#regular expenses/revenue (happy case) all negative
expenses_testcase_3 = [-11.11,-90.-12,80,-99.11,-10.10,-20]
grossRevenues_testcase_3 = [-10.34,-100.23,-180.11,-32.11,-10.44,-1.00]

##########################################################################################################


########################### EXCEPTION TESTCASES ##########################################################

invalid_filepath_testcases = ['/tmp/notaRealFile.mmz','/tmp/fakeashell.ccv','/somenotrealdir/bob.txt']

expected_resp_1 = ({'request':'transactions', 'status': 'failed','result':'file not submitted correctly, use the following syntax: curl -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv" '}, 400)
expected_resp_2 = ({'request':'transactions', 'status': 'failed','result':'filename is empty, dont use special characters/only spaces when naming your csv file" '}, 400)
expected_resp_3 = ({'request':'transactions', 'status': 'failed','result':'incorrect file extension, ensure csv file is submitted'}, 415)
expected_resp_4 = ({'request':'transactions', 'status': 'failed','result':'input file is empty'}, 404)
partial_expected_resp_5 = ({'request':'transactions', 'status': 'failed','result':'columns A-D are not filled properly on row '}, 422)
partial_expected_resp_6 = ({'request':'transactions', 'status': 'failed','result':'too many column entries on row '}, 422)

valid_key = "data"
invalid_key = "bob"
tmp_test_path = "/tmp/tests/"

#cases: 1) more than 1 csv file at a time, 2) diff key other than data being used, 3)empty file name, 4) not csv ext, 5) empty file size
invalid_csv_file_testcase_1 = [valid_key,tmp_test_path,[csv_testcase_1,csv_testcase_2],["test.csv","test5.csv"],expected_resp_1]
invalid_csv_file_testcase_2 = [invalid_key,tmp_test_path,[csv_testcase_1],["test99.csv"],expected_resp_1]
invalid_csv_file_testcase_3 = [valid_key,tmp_test_path,[csv_testcase_1],["   .csv"],expected_resp_2]
invalid_csv_file_testcase_4 = [valid_key,tmp_test_path,[csv_testcase_1],["test77.txt"],expected_resp_3]
invalid_csv_file_testcase_5 = [valid_key,tmp_test_path,[True],["test69.csv"],expected_resp_4]

#cases: 1) A-D not filled, but E-Z might be try with a) all missing, and b) some missing 2) Too many row entries >4
#Col A-D data missing

tmp_path = "/tmp/"

csv_testcase_3 = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
['2020-07-04',' Income',40, ' 347 Woodrow'],
["", "", "","",'2020-07-06',' Income',15, '  219 Pleasant'],
['   2020-07-12',' income',35, ' Blackburn St.'],
['2020-07-12','  Expense',27.5, ' Repairs']]

#some col missing
csv_testcase_4 = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
['2020-07-04',' Income',40, ' 347 Woodrow'],
['2020-07-06',' Income',15, '  219 Pleasant'],
['   2020-07-12',' income',"", 35, ' Blackburn St.'],
['2020-07-12','  Expense',27.5, ' Repairs']]

#too many col entries (>4):
csv_testcase_5 = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
['2020-07-04',' Income',40, ' 347 Woodrow'],
['2020-07-06',' Income',15, '  219 Pleasant'],
['   2020-07-12',' income',"still_another_input", 35, ' Blackburn St.',"asadsa","sadsaqqq"],
['2020-07-12','  Expense',27.5, ' Repairs']]

invalid_csv_file_testcase_6 = [valid_key,tmp_path,[csv_testcase_3],["test.csv"],partial_expected_resp_5]
invalid_csv_file_testcase_7 = [valid_key,tmp_path,[csv_testcase_4],["test.csv"],partial_expected_resp_5]
invalid_csv_file_testcase_8 = [valid_key,tmp_path,[csv_testcase_5],["test.csv"],partial_expected_resp_6]

##########################################################################################################

class utils_cases:
    #gen valid csv file and pass back Immutable MultiDict File Storage object (mock request file), and file_loc (full path + filename)
    @case(tags="val_file")
    @parametrize(testfilename=('test1.csv', 'test2.csv','test41.csv'))
    def case_validate_valid_file_1(self,helpers,testfilename):
        file_type, abs_path, filename = "csv","/tmp/tests/", testfilename
        types_of_content, num_of_files = ["text/csv"], 1
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        return [mock_request_file,file_loc]

    #gen mock file + return opened file + full location and the file contents
    @case(tags="val_rows_and_fields")
    @parametrize(test_info=(['test1.csv',csv_testcase_1], ['test2.csv',csv_testcase_2],['test41.csv',csv_testcase_2]))
    def case_validate_valid_rows_1(self,helpers,test_info,utils):
        file_type, abs_path, filename = "csv","/tmp/", test_info[0]
        types_of_content, num_of_files = ["text/csv"], 1
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
        return [file_open,file_loc,file_contents]

    
    #gen mock expenses and revenue testcases
    @case(tags="val_update_results")
    @parametrize(expenses_revenues=([expenses_testcase_1,grossRevenues_testcase_1], [expenses_testcase_2,grossRevenues_testcase_2],[expenses_testcase_3,grossRevenues_testcase_3]))
    def case_validate_valid_update_results(self,expenses_revenues):
        return [expenses_revenues[0],expenses_revenues[1]]
    

    #gen mock expenses and revenue testcases
    @case(tags="exception_files")
    @parametrize(test_file_path=(invalid_filepath_testcases[0],invalid_filepath_testcases[1],invalid_filepath_testcases[2]))
    def case_validate_file_exceptions(self,test_file_path):
        return test_file_path
    

    #gen mock [request_files,key,filepath,expected]
    @case(tags="invalid_csv_files")
    @parametrize(test_file_info=(invalid_csv_file_testcase_1,invalid_csv_file_testcase_2,invalid_csv_file_testcase_3,invalid_csv_file_testcase_4,invalid_csv_file_testcase_5))
    def case_validate_invalid_file_1(self,helpers,test_file_info):
        #testinput = [key,filepath,data,files,expected_resp]
        #testoutput = [request_files,key,filepath,expected]
        key, abs_path, file_data, filename,expected = test_file_info[0], test_file_info[1], test_file_info[2], test_file_info[3], test_file_info[4]
        num_of_files = len(filename)
        types_of_content = []
        file_loc = []
        i = 0
        for content in filename:
            content_list = content.split(".")
            types_of_content.append(content_list[-1].lower())
            file_loc.append(helpers.gen_file(types_of_content[i],abs_path,content,file_data[i]))
            i+=1
        mock_request_file = helpers.gen_mock_request_file(file_loc,filename,types_of_content, num_of_files,key)
        return [mock_request_file,key,file_loc,expected]

    #cases: 1) A-D not filled, but E-Z might be try with a) all missing, and b) some missing 2) Too many row entries >4
    #gen mock expenses and revenue testcases
    @case(tags="val_invalid_rows")
    @parametrize(test_file_info=(invalid_csv_file_testcase_6,invalid_csv_file_testcase_7,invalid_csv_file_testcase_8))
    def case_validate_invalid_rows_1(self,helpers,utils,test_file_info):
        #testinput = [key,filepath,data,files,expected_resp]
        #testoutput = [request_files,key,filepath,expected]
        key, abs_path, file_data, filename,expected = test_file_info[0], test_file_info[1], test_file_info[2], test_file_info[3], test_file_info[4]
        num_of_files = len(filename)
        types_of_content, file_loc, file_open, byte_len, file, file_contents = [], [], [], [], [], []
        i = 0
        for content in filename:
            content_list = content.split(".")
            types_of_content.append(content_list[-1].lower())
            file_loc.append(helpers.gen_file(types_of_content[i],abs_path,content,file_data[i]))
            mock_request_file = helpers.gen_mock_request_file(file_loc,filename,types_of_content, num_of_files,key)
            file_open.append(utils.open_file(file_loc[i], os.O_RDONLY))
            byte_len.append(os.stat(file_loc[i]).st_size)
            file.append(os.read(file_open[i],byte_len[i]).decode('utf-8'))
            file_contents.append(file[i].split('\n')[:-1])
            i+=1
        return [file_open,file_loc,file_contents,expected]



'''

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
'''