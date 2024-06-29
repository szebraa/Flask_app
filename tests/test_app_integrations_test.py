"""
This file is used to perform both happy cases and exception cases integration testing
of the apis of the app.py file

"""
import os
from pytest_cases import parametrize, parametrize_with_cases
from test_app_cases import app_cases

ENDPOINT = "https://127.0.0.1"

class Test_app:

    #######################################################methods for happy cases (without failure)######################################################

    #test GET without posting a file first
    def test_empty_get(self,client):
        expected = 204
        resp = client.get("/api/report")
        assert expected == resp.status_code

    #test POST for valid files
    @parametrize_with_cases("created_file", cases=app_cases, has_tag='val_post_files', import_fixtures = True)
    def test_post_valid_csv_file(self,client,created_file):
        expected = ({'request': 'transactions','result': 'data has been processed, send a GET request to the /report endpoint to retrieve the results','status': 'success'}, 200)
        # Convert csv file to bytes then send in the format the form expects
        csv,filename = created_file[0], created_file[1]
        csv_data = open(csv, "rb")
        data = {"data": (csv_data, filename)}

        resp = client.post(
            "/api/transactions",
            content_type='multipart/form-data',
            data=data,
            )
            
        csv_data.close()
        assert expected == (resp.json,resp.status_code)































































    #test remove file for a valid path
    def test_invalid_method(self,client):
        expected = 405
        resp = client.post("/api/report")
        assert expected == resp.status_code