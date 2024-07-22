""""
This is the main flask app api module file.
This file has 2 APIs (POST /api/transactions) and
GET /api/report

"""

import logging
import os
import config
import utils
from flask import Flask, request, jsonify, current_app

# use 'currentApp' to store data between requests
LOCAL_LOG_PATH = '/home/Canonical-flask-app/logs'
CONTAINER_LOG_PATH = '/var/www/Canonical-flask-app/logs'
LOG_FILE = None
if os.path.exists(LOCAL_LOG_PATH):
    LOG_FILE = LOCAL_LOG_PATH + '/error.log'
elif os.path.exists(CONTAINER_LOG_PATH):
    LOG_FILE = CONTAINER_LOG_PATH + '/error.log'
if LOG_FILE:
    # used for debugging
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    logger = logging.getLogger(__name__)

app = Flask(__name__)

# ensure jsonify doesn't auto sort the response
app.config['JSON_SORT_KEYS'] = False

# ensures <= 16mb files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# json response for files >16mb
@app.errorhandler(413)
def large_file(error):
    if not error:
        return error
    return jsonify({'request': 'transactions', 'status': 'failed',
                    'result': 'file is too big, limit is 16mb'}), 413


@app.route('/api/transactions', methods=["POST"])
def store_transactions():
    # logic:
    # check if POST call -> if file exists -> .csv ext ->
    # 0<size<=16mb -> only col A-D filled -> fields correctly filled -> calc
    # confirm http POST call (safety net)
    if request.method == 'POST':
        # reset gross revenue, expenses, net revenue, row entry,
        # and calculated state for every new POST
        utils.reset_sums()
        utils.reset_entries_counter()
        # used for TESTING ONLY
        # return jsonify(str(request.files))
        # check: if file exists -> .csv ext -> 0<size<=16mb
        resp = utils.validate_file(request.files,
                                   config.FILE_STORAGE_KEY, config.FILEPATH)

        # no error codes/legitimate file
        if not resp:

            file_open = utils.open_file(config.FILEPATH, os.O_RDONLY)
            # safety catch for issues opening up the tmp file
            if isinstance(file_open, tuple):
                return file_open

            byte_len = os.stat(config.FILEPATH).st_size
            # catch cases where file is not encoded using utf-8
            try:
                file = os.read(file_open, byte_len).decode('utf-8')
            except UnicodeDecodeError:
                utils.file_cleanup(file_open,
                                   config.FILE_STORAGE_KEY, config.FILEPATH)
                return jsonify({'request': 'transactions', 'status': 'failed',
                                'result': 'file not encoded in utf-8. ' +
                                'Please ensure the file ' +
                                'is encoded in utf-8 format'}), 415

            # process
            year = []
            # split the string up into a list seperated by new line,
            # then get rid of last list entry, as, it will be empty
            file_contents = file.split('\n')[:-1]
            # go through each row in the csv
            for line in file_contents:
                # check only col A-D filled
                list_entry = utils.process_csv_row(line, file_open,
                                                   config.FILE_STORAGE_KEY,
                                                   config.FILEPATH)
                if isinstance(list_entry, list):
                    date = list_entry[0].lower().strip()
                    val_type = list_entry[1].lower().strip()
                    amount = list_entry[2].lower().strip()
                    memo = list_entry[3].lower().strip()

                    # process date; check date field correctly filled
                    resp = utils.verify_date(date, file_open,
                                             year, config.FILE_STORAGE_KEY,
                                             config.FILEPATH)
                    # either incorrectly formatted according to YYYY-mm-dd,
                    # or not of the same yr as the rest of the entries
                    if resp:
                        return resp

                    # process value_type (income or expenses);
                    # check type field correctly filled
                    net = utils.process_type(val_type, file_open,
                                             config.FILE_STORAGE_KEY,
                                             config.FILEPATH)
                    # neither expense nor income
                    if not isinstance(net, int):
                        return net

                    # process memo; check memo field correctly filled
                    resp = utils.process_memo(memo, file_open,
                                              config.FILE_STORAGE_KEY,
                                              config.FILEPATH)
                    # memo is all numbers, not a-z chars in memo
                    if resp:
                        return resp

                    # process amount; check amount field correctly filled
                    amount = utils.process_amount(amount, file_open,
                                                  config.FILE_STORAGE_KEY,
                                                  config.FILEPATH)
                    # invalid float, >32 bits, or > 2 decimal places
                    if not isinstance(amount, float):
                        resp = amount
                        return resp

                    # process expenses/gross revenue
                    utils.update_result(net, amount)

                # too many column entries or columns A-D not filled out
                else:
                    utils.reset_entries_counter()
                    return list_entry

            # calculate net revenue and get 200 OK JSON response; calc
            resp = utils.calculate_net_revenue(file_open,
                                               config.FILE_STORAGE_KEY,
                                               config.FILEPATH)
            return resp

        # not legitimate file: either file does not exists or not
        # .csv ext or size < 0
        else:
            try:
                request.files.get(config.FILE_STORAGE_KEY).close()
            except AttributeError:
                pass
            return resp

    # By default with methods = ["POST"], any other HTTP request
    # is already blocked; this is a safety net
    else:
        request.files.get(config.FILE_STORAGE_KEY).close()
        return jsonify({'request': 'transactions', 'status': 'failed',
                        'result': 'request made was not a POST request'}), 405


@app.route('/api/report', methods=['GET'])
def get_report():
    # confirm http GET call (safety net)
    if request.method == 'GET':
        # by design is single use, once client
        # has recieved their tax calculations,
        # no one else should be able to "GET" it
        if current_app.config.get('calculated', 0):
            net_revenue, gross_revenue, expenses = \
                current_app.config.get('netRevenue', 0), \
                current_app.config.get('grossRevenue', 0), \
                current_app.config.get('expenses', 0)
            # reset expenses, revenues, row counter and calculated
            # state between POST calls
            utils.reset_sums()
            utils.reset_entries_counter()
            return jsonify({'gross-revenue': float(gross_revenue),
                            'expenses': float(expenses),
                            'net-revenue': float(net_revenue)}), 200
        # no content to return
        else:
            return '', 204
    # By default with methods = ["GET"], any other HTTP request
    # is already blocked; this is a safety net
    else:
        return jsonify({'request': 'report', 'status': 'failed',
                        'result': 'request made was not a GET request'}), 405


if __name__ == '__main__':
    CRT_FILE = '/var/www/Canonical-flask-app/ssl_certs/server.crt'
    SERV_KEY = '/var/www/Canonical-flask-app/ssl_certs/server.key'
    app.run(host='0.0.0.0', debug=True, port=443,
            ssl_context=(CRT_FILE, SERV_KEY))
