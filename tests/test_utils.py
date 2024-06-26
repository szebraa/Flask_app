import pytest, os, io 
from decimal import Decimal
from pytest_cases import parametrize, parametrize_with_cases
from test_utils_cases import utils_cases

#Class for cases where utils runs without failure/HTTP error responses (happy cases)

class Test_utils:

    #methods for happy cases (without failure)

    def test_remove_file(self,utils):
        expected = False
        file = '/tmp/testfile.txt'
        open(file,'a').close()
        utils.remove_file(file)
        result = os.path.exists(file)
        assert expected == result

    def test_reset_sums(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,0,0]
        current_app.config['grossRevenue'] = 9123 
        current_app.config['expenses'] = 10
        current_app.config['netRevenue'] = -123
        utils.reset_sums()
        res = [current_app.config.get('grossRevenue',0),current_app.config.get('expenses',0), current_app.config.get('expenses',0)]
        assert res == expected
    
    def test_reset_entries_counter(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,False]
        current_app.config['entries'] = 9111 
        current_app.config['calculated'] = True
        utils.reset_entries_counter()
        res = [current_app.config.get('entries',0), current_app.config.get('calculated',0)]
        assert res == expected

    #to test for http invalid responses, note that jsonify returns tuples
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
    

    #methods for failure/exception cases

    @parametrize_with_cases("exception_file", cases=utils_cases, has_tag='exception_files', import_fixtures = True)
    def test_remove_file_exception(self,utils,exception_file):
        expected = 'File does not exist in provided directory'
        with pytest.raises(FileNotFoundError) as exc_info:
            utils.remove_file(exception_file)
        assert str(exc_info.value) == expected
    
    @parametrize_with_cases("exception_file", cases=utils_cases, has_tag='exception_files', import_fixtures = True)
    def test_open_file_exception(self,utils,exception_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'error opening tmp file saved on server side'}, 404)
        res = utils.open_file(exception_file,os.O_RDONLY)
        assert (res[0].json,res[1]) == expected

    
    #cases: 1) more than 1 csv file at a time, 2) diff key other than data being used, 3)empty file name, 4) not csv ext, 5) empty file dize

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

    '''
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
    '''
