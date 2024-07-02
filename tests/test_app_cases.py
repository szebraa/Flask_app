"""
This file is used to generate custom test cases (except + happy cases) for the
'test_app_integrations_test.py' file
"""
#unit test testcase file
from pytest_cases import parametrize, parametrize_with_cases, case
import os
########################### HAPPY CASES TESTCASES #####################################################
tmp_path = "/tmp/"
csv_ext = "csv"
csv_content = "text/csv"
#regular data (happy case)
csv_testcase_1 = [['    2020-07-01   ','expense', "18.77", 'Fuel'],
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

correct_filenames1 = ['test1.csv','test2.csv','test41.csv']

##########################################################################################################

########################### HTTP 400/exception TESTCASES #####################################################
#incorrect file ext name (415 HTTP response)
txt_filenames1 = ['test1.txt','test2.txt','test41.txt']
txt_ext = "txt"
txt_content = "text/plain"
utf_16_enc = "utf-16"

#utf-16 characters data (415 HTTP response)
csv_testcase_3 = [['    2020-07-01   ','expenseý', "18.77", 'Fuelý'],
['2020-07-04',' Income','40', ' 347 Woýodrow'],
['2020-07-06',' Inýcome','15', '  219 Pleýasant'],
['   2020-07-12',' incoýme','35', ' Blackburn St.'],
['2020-07-12','  Expýense','27.5', ' REPAIRS']]


#cases: 1) A-D not filled, but E-Z might be try with a) all missing, and b) some missing 2) Too many row entries >4
#Col A-D data missing


#all missing columns case (A-D)
csv_testcase_4 = [['    2020-07-01   ','expense', '18.77', 'Fuel'],
['2020-07-04',' Income','40', ' 347 Woodrow'],
["", "", "","",'2020-07-06',' Income','15', '  219 Pleasant'],
['   2020-07-12',' income','35', ' Blackburn St.'],
['2020-07-12','  Expense','27.5', ' Repairs']]

missing_row_ind1 = "3"

#some col missing
csv_testcase_5 = [['    2020-07-01   ','expense', '18.77', 'Fuel'],
['2020-07-04',' Income','40', ' 347 Woodrow'],
['2020-07-06',' Income','15', '  219 Pleasant'],
['   2020-07-12',' income',"", '35', ' Blackburn St.'],
['2020-07-12','  Expense','27.5', ' Repairs']]

missing_row_ind2 = "4"

#too many col entries (>4):
csv_testcase_6 = [['    2020-07-01   ','expense', '18.77', 'Fuel'],
['2020-07-04',' Income','40', ' 347 Woodrow'],
['2020-07-06',' Income','15', '  219 Pleasant'],
['   2020-07-12',' income',"still_another_input", '35', ' Blackburn St.',"asadsa","sadsaqqq"],
['2020-07-12','  Expense','27.5', ' Repairs']]

inval_row_ind3 = "4"




###############################################################################################################

class app_cases:

    ########################### happy cases HTTP 200s codes#################################

    #gen mock file + return opened file + full location and the file contents
    @case(tags="val_post_files")
    @parametrize(test_info=([correct_filenames1[0],csv_testcase_1], [correct_filenames1[1],csv_testcase_2],[correct_filenames1[2],csv_testcase_2]))
    def case_validate_valid_rows_1(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename]
    
    #########################################################################################


    ########################### exception cases HTTP 400s codes#################################
    #create csv file with empty name (i.e.: "    .csv" variations)
    @case(tags="empty_file_name")
    @parametrize(test_info=(['        .csv',csv_testcase_1], ['.csv',csv_testcase_2],['     .csv',csv_testcase_2]))
    def case_validate_empty_filename(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename]

    #create csv file with empty size (0B)
    @case(tags="0B_file")
    @parametrize(test_info=([correct_filenames1[0],True], [correct_filenames1[1],True],[correct_filenames1[2],True]))
    def case_validate_0B_file(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename]

    #create a large (16MB) csv file (HTTP 413)
    @case(tags="16MB_file")
    @parametrize(test_info=(correct_filenames1[0],correct_filenames1[1],correct_filenames1[2]))
    def case_validate_16MB_file(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = csv_content
        #create file and get file dir + name
        file_loc = helpers.write_big_file(file_type,abs_path,filename)
        return [file_loc,filename]

    
    #create txt file extension files (HTTP 415)
    @case(tags="txt_ext_file")
    @parametrize(test_info=([txt_filenames1[0],csv_testcase_1], [txt_filenames1[1],csv_testcase_2],[txt_filenames1[2],csv_testcase_2]))
    def case_validate_incorrect_ext(self,helpers,test_info):
        file_type, abs_path, filename = txt_ext,tmp_path, test_info[0]
        types_of_content = [txt_content]
        input_data = test_info[1]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename]


    #create file not encoded in UTF-8. (HTTP 415)
    @case(tags="utf-16_enc_file")
    @parametrize(test_info=([correct_filenames1[0],csv_testcase_3], [correct_filenames1[1],csv_testcase_3],[correct_filenames1[2],csv_testcase_3]))
    def case_validate_incorrect_enc(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data = test_info[1]
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data,utf_16_enc)
        return [file_loc,filename]


    #create csv file where col A-D not filled out (HTTP 422)
    @case(tags="col_A-D_not_filled")
    @parametrize(test_info=([correct_filenames1[0],csv_testcase_4,missing_row_ind1], [correct_filenames1[1],csv_testcase_5,missing_row_ind2]))
    def case_validate_inval_col_fill1(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data, inval_row = test_info[1], test_info[2]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename,inval_row]
    
    #create file where more than 4 col are filled out (HTTP)
    @case(tags="col_overfilled")
    @parametrize(test_info=([correct_filenames1[0],csv_testcase_6,inval_row_ind3],))
    def case_validate_inval_col_fill2(self,helpers,test_info):
        file_type, abs_path, filename = csv_ext,tmp_path, test_info[0]
        types_of_content = [csv_content]
        input_data, inval_row = test_info[1], test_info[2]
        #create file and get file dir + name
        file_loc = helpers.gen_file(file_type,abs_path,filename,input_data)
        return [file_loc,filename,inval_row]


    #########################################################################################










