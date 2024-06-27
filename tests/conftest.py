import pytest, sys, os, csv
from api import utils as util
from api import config as configs
from pytest_cases import parametrize_with_cases, fixture, parametrize
from typing import List, Union

# getting the name of the directory where the this file is present.
current_dir = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name where the current directory is present.
parent_dir = os.path.dirname(current_dir)
api_dir = parent_dir + '/api/'

# adding the api directory to the sys.path.
sys.path.append(api_dir)

from app import app as flask_app
from flask import current_app as cur


from werkzeug.datastructures import FileStorage as RequestFiles
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

class Helpers:

    @staticmethod
    def get_file_storage_key():
        return configs.file_storage_key

    @staticmethod
    def get_filepath():
        return configs.filepath
    
    @staticmethod
    def gen_file(file_type: str,abs_path: str,filename: str,input_data: List[List[Union[str,float]]] = None):
        #default data
        if(not input_data):
            input_data = [['    2020-07-01   ','expense', 18.77, 'Fuel'],
            ['2020-07-04',' Income',40, ' 347 Woodrow']]
        elif(type(input_data) == bool):
            input_data = []
        file_loc = abs_path + filename  if abs_path[-1] == '/' else  abs_path + "/" + filename
        #create new directory if it doesnt exist to avoid errors in writing to file later
        if(not os.path.exists(abs_path)):
             os.makedirs(abs_path)
        if(file_type == 'csv' or file_type == 'txt'):
            with open(file_loc,"w",newline='') as file:
                writer = csv.writer(file)
                for data in input_data:
                    writer.writerow(data)
            file.close()
            return file_loc
        #this would be for other file types in the future
        else:
            return


    #gen immutableMultiDict FileStorage object
    @staticmethod
    def gen_mock_request_file(file_locs: list,filenames: list,types_of_content: list, num_of_files: int, key: str = None):
        if(not len(file_locs) == len(filenames) == len(types_of_content) == num_of_files):
            return "ensure fields are consistent in length"
        i = 0
        #assume list input for scalability in the future
        mock_request_file = MultiDict()
        while(i<num_of_files):
            #create File Storage object
            mock_file = RequestFiles(
            stream=open(file_locs[i], "rb"),
            filename=filenames[i],
            content_type=types_of_content[i]
            )
            
            mock_request_file.add(Helpers.get_file_storage_key(),mock_file)
            i+=1
        mock_request_file = ImmutableMultiDict(mock_request_file)
        return mock_request_file

    #process opening and decoding file
    @staticmethod
    def open_and_decode_file(filename: list, abs_path: str, file_data: list, expected: tuple, num_of_files: int,key:str):
        i = 0
        types_of_content, file_loc, file_open, byte_len, file, file_contents = [], [], [], [], [], []
        for content in filename:
            content_list = content.split(".")
            types_of_content.append(content_list[-1].lower())
            file_loc.append(Helpers.gen_file(types_of_content[i],abs_path,content,file_data[i]))
            mock_request_file = Helpers.gen_mock_request_file(file_loc,filename,types_of_content, num_of_files,key)
            file_open.append(util.open_file(file_loc[i], os.O_RDONLY))
            byte_len.append(os.stat(file_loc[i]).st_size)
            file.append(os.read(file_open[i],byte_len[i]).decode('utf-8'))
            file_contents.append(file[i].split('\n')[:-1])
            i+=1
        return [file_open,file_loc,file_contents,expected]




#all these methods can be inferred by other test files to access the capabilities modules

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def utils():
    return util

@pytest.fixture
def current_app():
    return cur

@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture
def client(app):
    return app.test_client()