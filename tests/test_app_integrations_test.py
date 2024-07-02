"""
This file is used to perform both happy cases and exception cases integration testing
of the apis of the app.py file

"""
import os
from pytest_cases import parametrize, parametrize_with_cases
from test_app_cases import app_cases
from decimal import Decimal

ENDPOINT = "https://127.0.0.1"

class Test_app:

    #######################################################methods for happy cases (HTTP 200/204 responses)######################################################

    #test report GET without posting a file first
    def test_empty_get_report(self,client):
        expected = 204
        resp = client.get("/api/report")
        assert expected == resp.status_code

    #test transactions POST for valid files
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_post_valid_transactions(self,client,created_file):
        expected = ({'request': 'transactions','result': 'data has been processed, send a GET request to the /report endpoint to retrieve the results','status': 'success'}, 200)
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        assert expected == (resp.json,resp.status_code)


    #test report GET after valid transactions POST
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_get_report_after_post_valid_transactions(self,client,current_app,app,created_file):
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        #csv_data = open(csv, "rb")
        data = {"data": (csv, filename)}
        app.app_context().push()
        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        net_revenue, gross_revenue, expenses = float(current_app.config.get('netRevenue',0)),float(current_app.config.get('grossRevenue',0)),float(current_app.config.get('expenses',0))
        resp = client.get("/api/report")
        expected = ({'gross-revenue':gross_revenue, 'expenses':expenses,'net-revenue':net_revenue}, 200)
        #csv_data.close()
        assert expected == (resp.json,resp.status_code)
    
    #test double GET report after valid transactions POST
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_double_get_report_after_post_transactions(self,client,current_app,app,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        #csv_data = open(csv, "rb")
        data = {"data": (csv, filename)}
        app.app_context().push()
        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        resp = client.get("/api/report")
        #csv_data.close()
        assert expected == resp.status_code

###################################################################################################################################################################

#######################################################methods for (HTTP 400s responses)###########################################################################



#####################################################methods HTTP POST 400 response###############################################################################

#cases: 1) more than 1 csv file at a time, 2) diff key other than data being used, 3)empty file name


    #test invalid transactions POST, case 1: more than 1 csv file at a time
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_post_2_simult_files_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'file not submitted correctly, use the following syntax: curl -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv" '}, 400)
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": [(csv, filename),(csv, filename)]}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 1: more than 1 csv file at a time
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_get_report_after_failed_post_transactions1(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": [(csv, filename),(csv, filename)]}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        assert expected == resp.status_code

    #test invalid transactions POST, case 2: diff key other than data being used
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_post_inval_key_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'file not submitted correctly, use the following syntax: curl -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv" '}, 400)
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"file": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 2: diff key other than data being used
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_get_report_after_failed_post_transactions2(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"file": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        assert expected == resp.status_code

    #test invalid transactions POST, case 3: empty file name
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='empty_file_name', import_fixtures = True)
    def test_post_empty_filename_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'filename is empty, dont use special characters/only spaces when naming your csv file" '}, 400)
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == (resp.json,resp.status_code)
    

    #test GET report following an invalid transactions POST, case 3: empty file name
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='empty_file_name', import_fixtures = True)
    def test_get_report_after_failed_post_transactions3(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == resp.status_code


##########################################################################################################################################################

#####################################################methods HTTP POST 404 response###############################################################################



    #expected_resp_4 = ({'request':'transactions', 'status': 'failed','result':'input file is empty'}, 404)  

    #cases: 1) more than 1 csv file at a time, 2) diff key other than data being used, 3)empty file name


    #test invalid transactions POST, case 1: empty CSV file (0B)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='0B_file', import_fixtures = True)
    def test_post_0B_file_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'input file is empty'}, 404)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 1: empty CSV file (0B)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='0B_file', import_fixtures = True)
    def test_get_report_after_failed_post_transactions4(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        assert expected == resp.status_code
    
    ######################################################################################################################################################################

    #####################################################methods HTTP POST/GET 405 response###############################################################################

    #test invalid transactions method (GET)
    def test_inval_get_transactions(self,client):
        expected =  405  
        resp = client.get("/api/transactions")
        assert expected == resp.status_code

    #test invalid transactions method (PUT)
    def test_inval_put_transactions(self,client):
        expected =  405  
        resp = client.put("/api/transactions")
        assert expected == resp.status_code
    
    #test invalid transactions method (DELETE)
    def test_inval_delete_transactions(self,client):
        expected =  405  
        resp = client.delete("/api/transactions")
        assert expected == resp.status_code
    
    #test put report (invalid method)
    def test_invalid_delete_report(self,client):
        expected = 405
        resp = client.delete("/api/report")
        assert expected == resp.status_code


    #test put report (invalid method)
    def test_invalid_put_report(self,client):
        expected = 405
        resp = client.put("/api/report")
        assert expected == resp.status_code



    #test post report (invalid method)
    def test_inval_post_report(self,client):
        expected = 405
        resp = client.post("/api/report")
        assert expected == resp.status_code


    ######################################################################################################################################################################

    #####################################################methods HTTP POST 413 response###############################################################################

    #cases: 1) CSV file input is too big > 16MB
    #test invalid transactions POST, case 1: CSV file input is > 16MB
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='16MB_file', import_fixtures = True)
    def test_post_large_file_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'file is too big, limit is 16mb'}, 413)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 1: CSV file input is > 16MB
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='16MB_file', import_fixtures = True)
    def test_get_report_after_failed_post_transactions5(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == resp.status_code




    ######################################################################################################################################################################


    #####################################################methods HTTP POST 415 response###############################################################################

    #cases: 1) Incorrect file extension (not .csv) , 2) not encoded in UTF-8 (e.g.: LATIN-1)


    #test invalid transactions POST, case 1: Incorrect file extension (not .csv)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='txt_ext_file', import_fixtures = True)
    def test_post_txt_file_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'incorrect file extension, ensure csv file is submitted'}, 415)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 1: Incorrect file extension (not .csv)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='txt_ext_file', import_fixtures = True)
    def test_get_report_after_failed_post_transactions6(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        if(os.path.isfile(csv)):
            os.remove(csv)
        assert expected == resp.status_code



    #test invalid transactions POST, case 2: not encoded in UTF-8 (e.g.: utf-16)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='utf-16_enc_file', import_fixtures = True)
    def test_post_inc_enc_transactions(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed', 'result':'file not encoded in utf-8. Please ensure the file is encoded in utf-8 format'}, 415)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 2: not encoded in UTF-8 (e.g.: utf-16)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='utf-16_enc_file', import_fixtures = True)
    def test_get_report_after_failed_post_transactions7(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code





    ######################################################################################################################################################################



    #####################################################methods HTTP POST 422 response##################################################################################

    
    #cases: 1) columns A-D are not filled properly in the csv file, 2)More than 4 column entries in a particular row in the csv file, 
    # 3)Incorrectly formatted date, format as yyyy-mm-dd, 4)Date entries are not all from the same year, 5)Type field is incorrectly formatted type; specify either 'expense' or 'income', 
    # 6)Memo field does not have any English characters (a-z), 7)Amount field is either: an invalid float ($ not accepted), > 32 bits, or > 2 decimal places, scientific notation



    

    ####################################################### ROW CHECK CASES ####################################################################

    #cases: 1) col A-D not filled, but E-Z might be try with a) all missing, and b) some missing , 2) Too many col entries >4

    #test invalid transactions POST, case 1: col A-D not filled, but E-Z might be try with a) all missing, and b) some missing
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='col_A-D_not_filled', import_fixtures = True)
    def test_post_inval_rows_transactions1(self,client,created_file):
        
        # Convert csv file to bytes then send in the format the form expects
        csv,filename,invald_row = created_file[0], created_file[1], created_file[2]
        expected = ({'request':'transactions', 'status': 'failed','result':'columns A-D are not filled properly on row '+ invald_row}, 422)  
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 1: col A-D not filled, but E-Z might be try with a) all missing, and b) some missing
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='col_A-D_not_filled', import_fixtures = True)
    def test_get_report_after_failed_post_transactions8(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename,invald_row = created_file[0], created_file[1], created_file[2]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code



    #test invalid transactions POST, case 2: Too many col entries >4
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='col_overfilled', import_fixtures = True)
    def test_post_inval_rows_transactions2(self,client,created_file):  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename,invald_row = created_file[0], created_file[1], created_file[2]
        expected = ({'request':'transactions', 'status': 'failed','result':'too many column entries on row '+ invald_row}, 422)
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 2: Too many col entries >4
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='col_overfilled', import_fixtures = True)
    def test_get_report_after_failed_post_transactions9(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename,invald_row = created_file[0], created_file[1], created_file[2]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code




    ####################################################### DATE FIELD CASES ####################################################################

    # 3)Incorrectly formatted date, format as yyyy-mm-dd, 4)Date entries are not all from the same year


    #test invalid transactions POST, case 3: Incorrectly formatted date, format as yyyy-mm-dd
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_date_field1', import_fixtures = True)
    def test_post_inval_date_transactions1(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'incorrectly formatted date, format as yyyy-mm-dd'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 3: Incorrectly formatted date, format as yyyy-mm-dd
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_date_field1', import_fixtures = True)
    def test_get_report_after_failed_post_transactions10(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code


    #test invalid transactions POST, case 4: Date entries are not all from the same year
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_date_field2', import_fixtures = True)
    def test_post_inval_date_transactions2(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'Please ensure all entries are from the same year'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 4: Date entries are not all from the same year
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_date_field2', import_fixtures = True)
    def test_get_report_after_failed_post_transactions11(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code
    


    ####################################################### TYPE FIELD CASES ####################################################################

    # 5)Type field is incorrectly formatted type; specify either 'expense' or 'income'

    #test invalid transactions POST, case 5: Type field is incorrectly formatted type; specify either 'expense' or 'income'
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_type_field1', import_fixtures = True)
    def test_post_inval_type_transactions1(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'incorrectly formatted type, please specify either expense or income'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 5: Type field is incorrectly formatted type; specify either 'expense' or 'income'
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_type_field1', import_fixtures = True)
    def test_get_report_after_failed_post_transactions12(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code


    ####################################################### MEMO FIELD CASES ####################################################################

    # 6)Memo field does not have any English characters (a-z)

    #test invalid transactions POST, case 6: Memo field does not have any English characters (a-z)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_memo_field1', import_fixtures = True)
    def test_post_inval_memo_transactions1(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'your memo does not have any english characters (a-z), which does not make sense'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 6: Memo field does not have any English characters (a-z)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_memo_field1', import_fixtures = True)
    def test_get_report_after_failed_post_transactions13(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code


    ####################################################### AMOUNT FIELD CASES ####################################################################

    # 7)Amount field an invalid float ($ not accepted), 8) Amount field is > 32 bits, 9) Amount field is > 2 decimal places, 10) Amount field is in scientific notation

    #test invalid transactions POST, case 7: Amount field an invalid float ($ not accepted)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field1', import_fixtures = True)
    def test_post_inval_amount_transactions1(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'your amount is not formatted properly. please ensure to put just the numerical value (e.g.: 50.2 or 50 or 50.79) with no $ preceeding the value'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 7: Amount field an invalid float ($ not accepted)
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field1', import_fixtures = True)
    def test_get_report_after_failed_post_transactions14(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code


    #test invalid transactions POST, case 8: Amount field is > 32 bits
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field2', import_fixtures = True)
    def test_post_inval_amount_transactions2(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'Please input a realistic value in the amount field (>32 bit number is not realistic for your income or expense)'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 8: Amount field is > 32 bits
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field2', import_fixtures = True)
    def test_get_report_after_failed_post_transactions15(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code

    #test invalid transactions POST, case 9: Amount field is > 2 decimal places
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field3', import_fixtures = True)
    def test_post_inval_amount_transactions3(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'your amount has more than 2 decimal places which is not a real life money value. Please format to 2 decimal places or less (avoid scientific notation)'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 9: Amount field is > 2 decimal places
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field3', import_fixtures = True)
    def test_get_report_after_failed_post_transactions16(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code

    #test invalid transactions POST, case 10: Amount field is in scientific notation
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field4', import_fixtures = True)
    def test_post_inval_amount_transactions4(self,client,created_file):
        expected = ({'request':'transactions', 'status': 'failed','result':'your amount is not formatted properly. Please dont use scientific notation'}, 422)  
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}
        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == (resp.json,resp.status_code)

    #test GET report following an invalid transactions POST, case 10: Amount field is in scientific notation
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='inval_amount_field4', import_fixtures = True)
    def test_get_report_after_failed_post_transactions17(self,client,created_file):
        expected = 204
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        data = {"data": (csv, filename)}

        client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
        resp = client.get("/api/report")
        #if(os.path.isfile(csv)):
            #os.remove(csv)
        assert expected == resp.status_code




    ######################################################################################################################################################################














































##################################################################################################################################################################