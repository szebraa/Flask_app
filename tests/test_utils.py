import pytest, os, io

#Class for cases where utils runs without failure/error responses

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
        os.remove(helpers.get_filepath())
        os.remove(file_loc)
        assert res == expected
    