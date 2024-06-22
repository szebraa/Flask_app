import pytest, os, io 
from decimal import Decimal

#Class for cases where utils runs without failure/HTTP error responses

class Test_utils:

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
    def test_validate_file(self,app,current_app,utils,helpers):
        expected = None
        file_type, abs_path, filename = "csv","/tmp/tests/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        #test validate_file method
        res = utils.validate_file(mock_request_file,helpers.get_file_storage_key(),helpers.get_filepath())
        #cleanup tmp files here
        #first remove might not be needed as itll get removed through the unit test cases
        os.remove(helpers.get_filepath())
        os.remove(file_loc)
        assert res == expected
    
    def test_process_csv_row(self,app,current_app,utils,helpers):
        expected = True
        res = False
        file_type, abs_path, filename = "csv","/tmp/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
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

    def test_verify_date(self,app,current_app,utils,helpers):
        expected = None
        res = True
        year = []
        file_type, abs_path, filename = "csv","/tmp/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            date = list_entry[0].lower().strip()
            res = utils.verify_date(date,file_open,year,helpers.get_file_storage_key(),file_loc)
            if(res):
                res = True
                break
            
        os.remove(file_loc)
        assert res == expected
    
    def test_process_type(self,app,current_app,utils,helpers):
        expected = True
        res = False
        file_type, abs_path, filename = "csv","/tmp/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
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

    def test_process_memo(self,app,current_app,utils,helpers):
        expected = None
        res = True
        file_type, abs_path, filename = "csv","/tmp/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
        for line in file_contents:
            list_entry = utils.process_csv_row(line,file_open,helpers.get_file_storage_key(),file_loc)
            memo = list_entry[3].lower().strip()
            res = utils.process_memo(memo,file_open,helpers.get_file_storage_key(),file_loc)
            if(res):
                res = True
                break
            
        os.remove(file_loc)
        assert res == expected

    def test_process_amount(self,app,current_app,utils,helpers):
        expected = True
        res = False
        file_type, abs_path, filename = "csv","/tmp/","test1.csv"
        types_of_content, num_of_files = ["text/csv"], 1
        #probably good idea to put this in conftest somewhere
        input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
        ['2020-07-04',' Income',40, ' 347 Woodrow']]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        #create Immutable MultiDict File Storage object (mock request file)
        mock_request_file = helpers.gen_mock_request_file([file_loc],[filename],[types_of_content], num_of_files)
        file_open = utils.open_file(file_loc, os.O_RDONLY)
        byte_len = os.stat(file_loc).st_size
        file = os.read(file_open,byte_len).decode('utf-8')
        file_contents= file.split('\n')[:-1]
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
    
    def test_update_result(self,app,current_app,utils):
        expenses = [11.11,90.12,80,99.11,10.10]
        grossRevenues = [10.34,100.23,180.11,32.11,10.44]
        expected = (round(Decimal(sum(expenses)),2),round(Decimal(sum(grossRevenues)),2),len(expenses)+len(grossRevenues))
        for expense in expenses:
            utils.update_result(-1,expense)
        for grossRevenue in grossRevenues:
            utils.update_result(1,grossRevenue)
        res = (round(current_app.config.get('expenses',0),2),round(current_app.config.get('grossRevenue',0),2),current_app.config['entries'])
        assert res == expected