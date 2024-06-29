"""
This file is used to generate custom test cases (except + happy cases) for the
'test_app_integrations_test.py' file
"""
#unit test testcase file
from pytest_cases import parametrize, parametrize_with_cases, case
import os
########################### HAPPY CASES TESTCASES #####################################################
#regular data (happy case)
csv_testcase_1 = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
['2020-07-04',' Income','40', ' 347 Woodrow'],
['2020-07-06',' Income','15', '  219 Pleasant'],
['   2020-07-12',' income','35', ' Blackburn St.'],
['2020-07-12','  Expense','27.5', ' REPAIRS']]

#leading 0s (happy case)
csv_testcase_2 = [['    2020-07-01   ','expense', 00018.77, 'Fuel'],
['2020-07-04',' Income','40', ' 347 Woodrow'],
['2020-07-06',' Income','15', '  219 Pleasant'],
['   2020-07-12',' income','0035.0', ' Blackburn St.'],
['2020-07-12','  Expense','0027.5', ' Repairs']]

##########################################################################################################

class app_cases:

    ########################### happy cases #################################

    #gen mock file + return opened file + full location and the file contents
    @case(tags="val_post_files")
    @parametrize(test_info=(['test1.csv',csv_testcase_1], ['test2.csv',csv_testcase_2],['test41.csv',csv_testcase_2]))
    def case_validate_valid_rows_1(self,helpers,test_info):
        file_type, abs_path, filename = "csv","/tmp/", test_info[0]
        types_of_content, num_of_files = ["text/csv"], 1
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename)
        return [file_loc,filename]