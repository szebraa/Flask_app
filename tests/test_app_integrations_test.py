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
        assert expected == resp.status_code




    ######################################################################################################################################################################


    #####################################################methods HTTP POST 415 response###############################################################################

    #cases: 1) Incorrect file extension (not .csv) , 2) not encoded in UTF-8.











    ######################################################################################################################################################################


















































##################################################################################################################################################################