"""
This file is used to perform both happy cases and exception cases unit testing
on the utils.py file

"""
import pytest, os, io 
from decimal import Decimal
from pytest_cases import parametrize, parametrize_with_cases
from test_utils_cases import utils_cases

#Class for unit testing utils.py

class Test_utils:

    #######################################################methods for happy cases (without failure)######################################################

    #test remove file for a valid path
    def test_remove_file(self,utils):
        expected = False
        file = '/tmp/testfile.txt'
        open(file,'a').close()
        utils.remove_file(file)
        result = os.path.exists(file)
        assert expected == result

    #test reset sums of the current app context
    def test_reset_sums(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,0,0]
        current_app.config['grossRevenue'] = 9123 
        current_app.config['expenses'] = 10
        current_app.config['netRevenue'] = -123
        utils.reset_sums()
        res = [current_app.config.get('grossRevenue',0),current_app.config.get('expenses',0), current_app.config.get('expenses',0)]
        assert res == expected
    
    #test reset entry counter of the current app context
    def test_reset_entries_counter(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,False]
        current_app.config['entries'] = 9111 
        current_app.config['calculated'] = True
        utils.reset_entries_counter()
        res = [current_app.config.get('entries',0), current_app.config.get('calculated',0)]
        assert res == expected

    #validate valid ImmutableMultiDict Filestorage object w/csv ext
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_file', import_fixtures = True)
    def test_validate_file(self,utils,helpers,mock_file_fields):
        expected = None
        mock_request_file, file_loc = mock_file_fields[0], mock_file_fields[1]
        #test validate_file method
        res = utils.validate_file(mock_request_file,helpers.get_file_storage_key(),helpers.get_filepath())
        #cleanup tmp files here
        os.remove(helpers.get_filepath())
        os.remove(file_loc)
        assert res == expected
    
    #validate csv rows for a valid csv file
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_process_csv_row(self,utils,helpers,mock_file_fields):
        expected = True
        res = False
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            #check only col A-D filled
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(list_entry) == list):
                res = True
            else:
                res = False
                break
        os.remove(file_loc)
        assert res == expected

    #validate date fields for valid dates (same yr + yyyy-mm-dd format)
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_verify_date(self,utils,helpers,mock_file_fields):
        expected = None
        res = True
        year = []
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            date = list_entry[0].lower().strip()
            res = utils.verify_date(date,file_open,year,helpers.get_file_storage_key(),file_loc)
            if(res):
                res = True
                break   
        os.remove(file_loc)
        assert res == expected
    
    #validate type field with valid type (expense/income)
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_process_type(self,utils,helpers,mock_file_fields):
        expected = True
        res = False
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            val_type = list_entry[1].lower().strip()
            res = utils.process_type(val_type,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(res) == int):
                res = True
            else:
                res = False
                break
        os.remove(file_loc)
        assert res == expected

    #validate memo field with valid memo (at least 1 char)
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_process_memo(self,utils,helpers,mock_file_fields):
        expected = None
        res = True
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            memo = list_entry[3].lower().strip()
            res = utils.process_memo(memo,file_open,helpers.get_file_storage_key(),file_loc)
            if(res):
                res = True
                break
        os.remove(file_loc)
        assert res == expected

    #validate amount field with valid amount
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_process_amount(self,utils,helpers,mock_file_fields):
        expected = True
        res = False
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            amount = list_entry[2].strip()
            res = utils.process_amount(amount,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(res) == float):
                res = True
            else:
                res = False
                break
        os.remove(file_loc)
        assert res == expected
    
    #validate sum of all expenses and income for current app
    @parametrize_with_cases("expenses_revenues", cases=utils_cases, has_tag='val_update_results', import_fixtures = True)
    def test_update_result(self,app,current_app,utils,expenses_revenues):
        utils.reset_sums()
        utils.reset_entries_counter()
        expenses = list(map(abs, expenses_revenues[0]))
        grossRevenues = list(map(abs, expenses_revenues[1]))
        expected = (round(Decimal(sum(expenses)),2),round(Decimal(sum(grossRevenues)),2),len(expenses)+len(grossRevenues))
        for expense in expenses:
            utils.update_result(-1,expense)
        for grossRevenue in grossRevenues:
            utils.update_result(1,grossRevenue)
        res = (round(current_app.config.get('expenses',0),2),round(current_app.config.get('grossRevenue',0),2),current_app.config['entries'])
        assert res == expected
    
    #validate difference of all income and expenses for current app
    @parametrize_with_cases("mock_file_fields", cases=utils_cases, has_tag='val_rows_and_fields', import_fixtures = True)
    def test_calculate_net_revenue(self,app,current_app,helpers,utils,mock_file_fields):
        expected = ({'request': 'transactions','result': 'data has been processed, send a GET request to the /report endpoint to retrieve the results','status': 'success'}, 200)
        utils.reset_sums()
        utils.reset_entries_counter()
        file_open, file_loc, file_contents = mock_file_fields[0], mock_file_fields[1], mock_file_fields[2]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            val_type = list_entry[1].lower().strip()
            net = utils.process_type(val_type,file_open,helpers.get_file_storage_key(),file_loc)
            amount = list_entry[2].strip()
            amount = utils.process_amount(amount,file_open,helpers.get_file_storage_key(),file_loc)
            utils.update_result(net,amount)
        app.app_context().push()
        res = utils.calculate_net_revenue(file_open,helpers.get_file_storage_key(),file_loc)
        assert (res[0].json,res[1]) == expected
    

    ##########################################################################################################################################################################

    #####################################################methods for failure/exception cases##################################################################################

    #validate exception msg for removing invalid file paths
    @parametrize_with_cases("exception_file", cases=utils_cases, has_tag='exception_files', import_fixtures = True)
    def test_remove_file_exception(self,utils,exception_file):
        expected = 'File does not exist in provided directory'
        with pytest.raises(FileNotFoundError) as exc_info:
            utils.remove_file(exception_file)
        assert str(exc_info.value) == expected
    
    #validate exceptions for opening files that dont exist
    @parametrize_with_cases("exception_file", cases=utils_cases, has_tag='exception_files', import_fixtures = True)
    def test_open_file_exception(self,utils,exception_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'error opening tmp file saved on server side'}, 404)
        res = utils.open_file(exception_file,os.O_RDONLY)
        assert (res[0].json,res[1]) == expected

    
    #cases: 1) more than 1 csv file at a time, 2) diff key other than data being used, 3)empty file name, 4) not csv ext, 5) empty file dize
    #validate invalid file exceptions
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='invalid_csv_files', import_fixtures = True)
    def test_validate_invalid_file(self,utils,helpers,test_file_info):
        #[mock_request_file,key,file_loc,expected]
        mock_request_file, key, file_loc, expected = test_file_info[0], test_file_info[1], test_file_info[2], test_file_info[3]
        #test validate_file method
        res = utils.validate_file(mock_request_file,key,helpers.get_filepath())
        #cleanup tmp files here
        #os.remove(helpers.get_filepath())
        for files in file_loc:
            os.remove(files)
        assert (res[0].json,res[1]) == expected

    #cases: 1) A-D not filled, but E-Z might be try with a) all missing, and b) some missing 2) Too many row entries >4
    #validate exceptions for invalid rows
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='val_invalid_rows', import_fixtures = True)
    def test_validate_invalid_rows(self,utils,helpers,app,current_app,test_file_info):
        #[file_open,file_loc,file_contents,expected]
        file_open, file_loc, file_contents, expected = test_file_info[0][0], test_file_info[1][0], test_file_info[2][0], test_file_info[3]

        for line in file_contents:
            #check only col A-D filled
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(list_entry) == list):
                res = True
            else:
                res = list_entry
                break
        if(os.path.isfile(file_loc)):
            os.remove(file_loc)
        expected_str = str(expected[0])[:-2] + str(current_app.config.get('entries',0)+1) + "'" + "}" 
        expected = (eval(expected_str), expected[1])
        assert (res[0].json,res[1]) == expected

    #cases: 1) date not formated as: yyyy-mm-dd (values that dont make sense), 2) date not formated as: yyyy-mm-dd (e.g: dd-mm-yyyy) , 3) not all same year
    #validate exceptions for invalid date
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='val_invalid_date', import_fixtures = True)
    def test_validate_invalid_date(self,utils,helpers,app,current_app,test_file_info):
        #[file_open,file_loc,file_contents,expected]
        file_open, file_loc, file_contents, expected = test_file_info[0][0], test_file_info[1][0], test_file_info[2][0], test_file_info[3]
        year_list = []

        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            date = list_entry[0].lower().strip()
            res = utils.verify_date(date,file_open,year_list,helpers.get_file_storage_key(),file_loc)
            if(res):
                break
        if(os.path.isfile(file_loc)):
            os.remove(file_loc)
        assert (res[0].json,res[1]) == expected

    #cases: 1) Not either income or expense
    #validate exceptions for invalid type field
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='val_invalid_type', import_fixtures = True)
    def test_validate_invalid_type(self,utils,helpers,app,current_app,test_file_info):
        #[file_open,file_loc,file_contents,expected]
        file_open, file_loc, file_contents, expected = test_file_info[0][0], test_file_info[1][0], test_file_info[2][0], test_file_info[3]

        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            val_type = list_entry[1].lower().strip()
            res = utils.process_type(val_type,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(res)!=int):
                break
        if(os.path.isfile(file_loc)):
            os.remove(file_loc)
        assert (res[0].json,res[1]) == expected   


    #cases: 1) No chars a-z/A-Z used
    #validate exceptions for invalid memo
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='val_invalid_memo', import_fixtures = True)
    def test_validate_invalid_memo(self,utils,helpers,app,current_app,test_file_info):
        #[file_open,file_loc,file_contents,expected]
        file_open, file_loc, file_contents, expected = test_file_info[0][0], test_file_info[1][0], test_file_info[2][0], test_file_info[3]

        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            memo = list_entry[3].lower().strip()
            res = utils.process_memo(memo,file_open,helpers.get_file_storage_key(),file_loc)
            if(res):
                break
        if(os.path.isfile(file_loc)):
            os.remove(file_loc)
        assert (res[0].json,res[1]) == expected    


    #cases: 1) valid float (no $), 2) <=32 bits, 3) < 2 decimal places, 4) scientific notation
    #validate exception for invalid amounts used
    @parametrize_with_cases("test_file_info", cases=utils_cases, has_tag='val_invalid_amount', import_fixtures = True)
    def test_validate_invalid_amount(self,utils,helpers,app,current_app,test_file_info):
        #[file_open,file_loc,file_contents,expected]
        file_open, file_loc, file_contents, expected = test_file_info[0][0], test_file_info[1][0], test_file_info[2][0], test_file_info[3]

        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            amount = list_entry[2].lower().strip()
            #process_amount
            res = utils.process_amount(amount,file_open,helpers.get_file_storage_key(),file_loc)
            if(type(res)!=float):
                break
        if(os.path.isfile(file_loc)):
            os.remove(file_loc)
        assert (res[0].json,res[1]) == expected    

###########################################################################################################################################################################