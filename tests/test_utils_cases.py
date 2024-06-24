from pytest_cases import parametrize, parametrize_with_cases, case
import os

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

invalid_filepath_testcases = ['/tmp/notaRealFile.mmz','/tmp/fakeashell.ccv','/somenotrealdir/bob.txt']

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