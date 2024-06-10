# Summer break

## Table of Contents

1. [Description](#description)
2. [Prerequisites](#prerequisites)
    - [Apache2 And Miscellaneous](#apache2-and-miscellaneous)
    - [Flask](#flask)
3. [Assumptions](#assumptions)
4. [Instructions For Running My Code](#instructions-for-running-my-code)
5. [Backend APIs](#backend-apis)
    - [Transactions](#transactions)
    - [Report](#report)
        - [Testcase Collection](#testcase-collection)
            - [Test Transactions API Testcases](#test-transactions-api-testcases)
            - [Test Report API Testcases](#test-report-api-testcases)
6. [My Solution's Shortcomings](#my-solution's-shortcomings)
7. [Additions & Refinements](#additions-&-refinements)

## Description

This application is written in Python 3 for the Flask backend, whereby APIs are used to read in a CSV file to
generate a tax-friendly report (in JSON).

## Prerequisites

The assumption is that this is a brand new Ubuntu node with just the packages that come with a fresh installation of Ubuntu.
Please use an editor - I recommend Microsoft Visual Studio Code, then press ctrl + shift + V to view properly. You could also use Atom for a proper view of the file, then press ctrl + shift + M on your keyboard to view properly. Please note that when I used Atom, hyperlinks wouldn't work correctly, hence I why I recommended Visual Studio Code.



### Apache2 And Miscellaneous

1. Ensure Ubuntu is up to date by running the following command:

```
sudo apt update && sudo apt upgrade
```

2. Install apache2 by running the following commands:

```
sudo apt install apache2
```
3. Modify firewall settings to allow access to the server (by default access will be restricted to your sever), to check which apps can be blocked or allowed use the following command:

```
sudo ufw app list
```

Output:

```
Available applications:
  Apache
  Apache Full
  Apache Secure
  CUPS

```

To enable access to Apache through the firewall (note that this is only for port 80):

```
sudo ufw allow 'Apache'
```

Output:

```
Rules updated
Rules updated (v6)
```

Re-enable the firewall with the following command:

```
sudo ufw enable
```
Then confirm that Apache is allowed through the firewall with the following command:

```
sudo ufw status
```

Output:

```
Status: active

To                         Action      From
--                         ------      ----
Apache                     ALLOW       Anywhere
Apache (v6)                ALLOW       Anywhere (v6)
```

4. Check that Apache is running by using the following command:

```
sudo systemctl status apache2
```

Output:

```
apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-05-23 22:04:18 EDT; 28min ago
       Docs: https://httpd.apache.org/docs/2.4/
    Process: 31539 ExecReload=/usr/sbin/apachectl graceful (code=exited, status=0/SUCCESS)
   Main PID: 26347 (apache2)
      Tasks: 55 (limit: 9315)
     Memory: 10.0M
     CGroup: /system.slice/apache2.service
             ├─26347 /usr/sbin/apache2 -k start
             ├─31543 /usr/sbin/apache2 -k start
             └─31544 /usr/sbin/apache2 -k start

May 23 22:04:18 alex-500-098 systemd[1]: Starting The Apache HTTP Server...
May 23 22:04:18 alex-500-098 apachectl[26346]: AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
May 23 22:04:18 alex-500-098 systemd[1]: Started The Apache HTTP Server.
May 23 22:17:40 alex-500-098 systemd[1]: Reloading The Apache HTTP Server.
May 23 22:17:40 alex-500-098 apachectl[31542]: AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
May 23 22:17:40 alex-500-098 systemd[1]: Reloaded The Apache HTTP Server.

```

5. Install curl using the following command:

```
sudo snap install curl
```

6. Visit https://www.postman.com/downloads/ and install POSTMAN (optional, as, you can test with curl instead).



### Flask

1. By default, most Ubuntu/Linux distributions come with Python3 already preinstalled. We can check with the following command:

```
python3 --version
```

If you don't see a Python version in the prompt, install a version of Python 3 using the following command:

```
sudo apt install python3
```

2. Create a file called 'Pipfile' with the following to aid in our installation of Flask (note that the "python_version" field depends on the version of python you have installed as per step 1):

```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"

[dev-packages]

[requires]
python_version = "3.8"

```

3. Install pip and pipenv using the following commands:

```
sudo apt install pip
```

```
sudo apt install pipenv
```

4. Create a new folder in /var/www/ and call it 'Canonical-flask-app' this is where the Flask app/files will reside.

5. Create a new directories in /var/www/Canonical-flask-app called 'logs', 'staic', and 'templates' for testing purposes.

6. Use the following commands to ensure that we have a new group called 'webmasters' (add your current user to this group), that all files placed here will inherit the group ownership of the directory, and correct ownership/permisions to directories will be applied:

```
sudo addgroup webmasters
```

```
sudo adduser $USER webmasters
```

```
sudo chown -R root:webmasters /var/www
```

```
sudo find /var/www -type d -exec chmod 775 {} \;
```

```
sudo find /var/www -type d -exec chmod g+s {} \;
```

7. Move your 'Pipfile' that you created earlier to the directory '/var/www/Canonical-flask-app'. Then, to ensure that only root and group owners can read and write to files, while other users can only read using the following command:

```
sudo find /var/www -type f -exec chmod 664 {} \;
```

8. Go to the directory '/var/www/Canonical-flask-app' and to install Flask and setup the proper virtual environment (dictated by our Pipfile previously created) run the following command:

```
sudo pipenv install
```

Output:

```
Creating a virtualenv for this project…
Using /usr/bin/python3.8 (3.8.10) to create virtualenv…
⠋created virtual environment CPython3.8.10.final.0-64 in 286ms
  creator CPython3Posix(dest=/home/alex/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, pkg_resources=latest, via=copy, app_data_dir=/home/alex/.local/share/virtualenv/seed-app-data/v1.0.1.debian.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

Virtualenv location: /home/alex/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Traceback (most recent call last):
  File "/usr/bin/pipenv", line 11, in <module>
    load_entry_point('pipenv==11.9.0', 'console_scripts', 'pipenv')()
  File "/usr/lib/python3/dist-packages/pipenv/vendor/click/core.py", line 722, in __call__
    return self.main(*args, **kwargs)
  File "/usr/lib/python3/dist-packages/pipenv/vendor/click/core.py", line 697, in main
    rv = self.invoke(ctx)
  File "/usr/lib/python3/dist-packages/pipenv/vendor/click/core.py", line 1066, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/usr/lib/python3/dist-packages/pipenv/vendor/click/core.py", line 895, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/usr/lib/python3/dist-packages/pipenv/vendor/click/core.py", line 535, in invoke
    return callback(*args, **kwargs)
  File "/usr/lib/python3/dist-packages/pipenv/cli.py", line 349, in install
    core.do_install(
  File "/usr/lib/python3/dist-packages/pipenv/core.py", line 1875, in do_install
    do_init(
  File "/usr/lib/python3/dist-packages/pipenv/core.py", line 1356, in do_init
    do_lock(
  File "/usr/lib/python3/dist-packages/pipenv/core.py", line 1174, in do_lock
    with open(project.lockfile_location, 'w') as f:
PermissionError: [Errno 13] Permission denied: '/var/www/Canonical-flask-app/Pipfile.lock'
alex@alex-500-098:/var/www/Canonical-flask-app$ sudo pipenv install
Creating a virtualenv for this project…
Using /usr/bin/python3.8 (3.8.10) to create virtualenv…
⠋created virtual environment CPython3.8.10.final.0-64 in 276ms
  creator CPython3Posix(dest=/root/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, pkg_resources=latest, via=copy, app_data_dir=/root/.local/share/virtualenv/seed-app-data/v1.0.1.debian.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

Virtualenv location: /root/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (ac8e32)!
Installing dependencies from Pipfile.lock (ac8e32)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 9/9 — 00:00:03
To activate this project's virtualenv, run the following:
 $ pipenv shell

```

Make sure to take note of the path to the virtual environment using this command:

```
pipenv --venv
```

Output:

```
/home/alex/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU
```

9. Our goal now is to create a 'wsgi' file so that our Flask app can run, but, before we do that, create a py file called 'app.py', modify it with the following code below (for testing purposes; this won't be our final Flask application):

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
```

Move this file to the directory /var/www/Canonical-flask-app and use the following command to modify permissions:

```
sudo find /var/www -type f -exec chmod 664 {} \;
```

10. In /var/www/Canonical-flask-app create a file called 'app.wsgi', and change its permissions with the following commands:

```
sudo touch app.wsgi;sudo chmod 664 app.wsgi

```

11. Modify the 'app.wsgi' (using either text editor or vi) and populate it as such:

```
import sys
sys.path.insert(0,'/var/www/Canonical-flask-app')

virt_env = '/home/alex/.local/share/virtualenvs/Canonical-flask-app-7q-geZJU'
with open(virt_env) as file_:
	exec(file_.read(),dict(__file__=virt_env))

from app import app as application
```

This allows the application (i.e.: the Flask app) to actually be deployed using the Apache module "wsgi".

12. Move the 'index.html' file from /var/www/html to /var/www/Canonical-flask-app/templates, then delete the /var/www/html/ folder (note: this is only for testing purposes before we build our API to ensure Flask is running, this would allow the html to render via Flask).

13. Install the wsgi module using the following command:

```
sudo apt-get install libapache2-mod-wsgi-py3
```

14. Create a config file in /etc/apache2/sites-available called 'Canonical-flask-app.conf', modify its permissions to 644, and populate it as such:

```
<VirtualHost *:5000>
            ServerName 127.0.0.1

            WSGIDaemonProcess flaskapi user=www-data group=www-data threads=5
            WSGIScriptAlias / /var/www/Canonical-flask-app/app.wsgi

            <Directory /var/www/Canonical-flask-app>
            		WSGIProcessGroup flaskapi
            		WSGIApplicationGroup %{GLOBAL}
                    Order deny,allow
                    Allow from all
            </Directory>

            Alias /static /var/www/Canonical-flask-app/static

            <Directory /var/www/Canonical-flask-app/static/>
                    Order allow,deny
                    Allow from all
            </Directory>
            ErrorLog /var/www/Canonical-flask-app/logs/error.log
            CustomLog /var/www/Canonical-flask-app/logs/access.log combined
</VirtualHost>
```

15. To enable this new site in Apache, use the following command:

```
sudo a2ensite Canonical-flask-app.conf
```

Output:

```
Enabling site Canonical-flask-app.
To activate the new configuration, you need to run:
  systemctl reload apache2

```

16. Reload apache2 with the following command:

```
sudo systemctl reload apache2
```

17. Install supervisord with the following command:

```
sudo apt install supervisor
```

and check that it's running:

```
sudo systemctl status supervisor
```

18. Create a file in /etc/supervisor/conf.d/ and name it 'idle.conf'. Populate it as such:

```
[program:Canonical_Flask_App]
command=python3 app.py
directory = /var/www/Canonical-flask-app/
autostart=true
autorestart=true
stderr_logfile=/var/log/idle.err.log
stdout_logfile=/var/log/idle.out.log
```
What we have done is that we've created a file to automatically start our flask application upon system boot (autostart = true), and, to automatically restart once the program exits (autorestart=true). In other words, our application won't close unless the server has been turned off. Now we need to make the supervisor process manager aware of this.

19. Use the following commands to ensure supervisor processes the idle.conf file:

```
sudo supervisorctl reread
```

Output:

```
Canonical_Flask_App: available
```

```
sudo supervisorctl update
```
Output:

```
Canonical_Flask_App: added process group
```

20. To test if the setup has been done correctly, go to http://127.0.0.1:5000/ on your web browser. You should something identical to the imagine below:

![flask](./screenshots/Flask_is_running.png)


## Assumptions

The following is a list of assumptions I made when designing the 2 APIs:

  - `The user is using a Linux OS (specifically Ubuntu since other distros could have different packaging type - not all our debian compliant), this will not work on Windows/MAC`
  - `That the user has sufficient disc space to install all the packages required in the setup and use the files that I provided`
  - `The application is a Flask application meant to be running on localhost on port 5000 (as per the provided shell script)`
  - `This application is not meant for a large amount of users at a time (i.e.: handles 1 user at a time)`
  - `Once transactions have been processed via the transactions API, you would only be able to GET the tally once via the report API before you would need to POST again (prevents a different user from stealing the 1st users' tally info)`
  - `Consecutive POSTS (i.e.: 2 POSTS in a row - or more) are meant to be 2 different users; this means that we won't sum data from the 1st CSV with data from the 2nd`
  - `That data only needs to be cached as long as the Flask server is up and running; any code changes or restarts to the server will erase data`
  - `That for the time allocated, a database, GUI(frontend), node redundancy, SSO authentication/API keys, SSL certificate (for https/443), and DNS hostname resolution (e.g.:www.google.com) are not required`
  - `That there were no restrictions on the Python3 modules/libraries I could use`
  - `The provided CSV file is always encoded in utf-8 format (application will throw a HTTP 415 error otherwise) or at least utf-8 is backwards compatible with the encoding; files not encoded in this way won't be processed`
  - `The provided CSV file would not be corrupted in any way`
  - `The provided CSV file is not expected to be processed if its >16MB (as this is the FLASK payload limit)`
  - `That the /tmp/ directoy doesn't have a cleaner of sorts to automatically delete files in tmp immediately`
  - `That the user has enough disc space/storage space to store a file up to 16MB in /tmp/ directory`
  - `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`
  - `That entries are all meant to be within the same year (i.e.: YYYY in date field are all the same), else should be unprocessable`
  - `That for any given row, only columns A-D are meant to be filled out in the CSV, else should be unprocessable`
  - `That there are no headers for the provided CSV file`
  - `That for the date field, the format is supposed to be as such: YYYY-mm-dd, and all other format will be unprocessable`
  - `That for a memo field to be valid, it should contain at least 1 alphabetic character (a-z) and not be only numbers`
  - `That a user would not want a partially calculated response (up until the point of failure from for example a missing field)`
  - `That for the amount field the user can input negative numbers, but, scientific notation may not be processable (e.g.: 3E10) and currency notation (e.g.:$30) will be unprocessable`
  - `That for the amount field in the CSV, the cell would be formated as a 'number' with at most 2 decimal places; any more than 2 decimal places and it will be unprocessable (unrealistic money value)`
  - `That for the amount field the upper limit is a 32 bit number (i.e.:4294967295), and, to be honest, even this number is unrealistic`
  - `If leading 0s are used for the amount field, all leading 0s will be ignored until the last 0 or the 1st non-zero number`
  - `That as per the shell script, the file would only ever be assigned to the variable data ("data=@data.csv"), else it will be unprocessable`
  - `That the Flask server won't crash or shutdown/restart mid os local save/delete/open/read of input file (i.e.: POST file) in the /tmp/ directory`
  - `That the application is only meant to process only CSV files, and, that only 1 CSV file can be provided at a time`
  - `That if there's an issue with the users csv file, they would know which row to fix in order to meet the requirements for a processable csv file`

## Instructions For Running My Code

1. Assuming you've followed my prerequesites instructions, unzip the tar.gz I've provided, then replace /var/www/Canonical-flask-app/app.py with my app.py and move the provided utils.py to /var/www/Canonical-flask-app/, then use the following command:

```
sudo chown -R root:webmasters /var/www
```

```
sudo systemctl restart apache2
```

```
sudo systemctl restart supervisor
```
2. Modify the provided test.sh bash script as such:

```
curl -v -X POST http://127.0.0.1:5000/transactions  -F "data=@data.csv"
echo
curl -v http://127.0.0.1:5000/report
```
Note that the -v option is just used to show more information about the HTTP response code

3. Move the shell script and the csv file to where you would like to open terminal, then, open terminal and run using the following command:

```
./test.sh
```

4. If the Flask app is ever in a state of error as per below:

![internal_server_error](./screenshots/Internal_Server_Error.png)

We can check the following logs:
```
less /var/log/idle.err.log
less /var/www/Canonical-flask-app/logs/error.log
less /var/log/supervisor/supervisord.log
```

Output:

![/var/log/idle.err.log log](./screenshots/idle_err_log.png)


Then once the bug is fixed on the server side code we can restart both the apache2 and supervisor processes:

```
sudo systemctl restart apache2
sudo systemctl restart supervisor
```

5. If you would like to use the testcases I've provided on /canonical-test-summer-break/My_files+instructions/testcases/ directory, please ensure they are on your local drive, and not on an external HDD/SSD

## Backend APIs


> [!NOTE]
> All API requests must be made over port 5000.

### Transactions

Take as input the CSV formatted data, parse, and store the data.

Endpoint: POST `/transactions`

Request Syntax:

```
curl -v -X POST http://127.0.0.1:5000/transactions  -F "data=@data.csv"
```

Request Body:

Would be in the CSV file as for example:

```
2020-07-01, Expense, 18.77, Gas
2020-07-04, Income, 40.00, 347 Woodrow
2020-07-06, Income, 35.00, 219 Pleasant
2020-07-12, Expense, 49.50, Repairs
```

HTTP Status Code Summary

| HTTP status | Code Summary | Details |
|---|---|---|
| 200 | OK | Everything worked as expected. |
| 400 | Bad Request | Empty file name, or, incorrect CURL syntax (e.g.:trying to send more than 1 file at a time). |
| 404 | Not Found | Empty input csv file (0 bytes) or error opening tmp file saved on server side. |
| 405 | Method not allowed | Incorrect HTTP REST call (i.e.: used GET, DELETE, PUT when POST is expected). |
| 413 | Payload Too Large | CSV file input is > 16mb. |
| 415 | Unsupported Media Type | Incorrect file extension (not .csv) or not encoded in UTF-8. |
| 422 | Unprocessable Content | Possible issues include: 1) columns A-D are not filled properly in the csv file,  2)More than 4 column entries in a particular row in the csv file,  3)Incorrectly formatted date, format as yyyy-mm-dd,  4)Date entries are not all from the same year,  5)Type field is incorrectly formatted type; specify either 'expense' or 'income', 6)Memo field does not have any English characters (a-z), 7)Amount field is either: an invalid float ($ not accepted),  > 32 bits, or > 2 decimal places |
| 500 | Internal Server Error | Something went wrong on the server end (usually caused by broken code/syntax errors). |

### Report

Return a JSON document with the tally of gross revenue, expenses, and net revenue.

Endpoint: GET `/report`

Response Body:

```json
{
  "gross-revenue": 151.23,
  "expenses": 112.93,
  "net-revenue": 38.30
}
```

HTTP Status Code Summary

| HTTP status | Code Summary | Details |
|---|---|---|
| 200 | OK | Everything worked as expected. |
| 204 | No Content | No data has been processed in the transactions endpoint; ensure you submit a  correct csv formatted file to the transactions endpoint then try the report  endpoint again |
| 405 | Method Not Allowed | Incorrect HTTP REST call (i.e.: used POST, DELETE, PUT when GET is expected). |
| 500 | Internal Server Error | Something went wrong on the server end (usually caused by broken code/syntax errors). |

#### Testcase collection

See testcase collection (csv files used) [here](./testcases/not_a_test_file.txt)
The path is in the same location as the file you just opened (i.e.:/canonical-test-summer-break/My_files+instructions/testcases)

##### Test Transactions API Testcases

1. Case: standard correct data
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv"```

   Expected Response: 200 OK

   Response:

   ![standard_200_OK_POST](./screenshots/standard_200_OK_POST.png)


2. Case: Amount field has leading 0s
   
   File used: leading 0s correct data [here](./testcases/data_leading_0s.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_leading_0s.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_leading_0s.csv"```

   Expected Response: 200 OK

   Assumption: `If leading 0s are used for the amount field, all leading 0s will be ignored until the last 0 or the 1st non-zero number`

   Response:

   ![leading_0s_200_OK_POST](./screenshots/leading_0s_200_OK_POST.png)


3. Case: Incorrect CURL syntax (more than 1 file sent at a time)
   
   Files used: standard correct data [standard](./testcases/data.csv) leading 0s correct data [leading0s](./testcases/data_leading_0s.csv)(if you are unable to click the hyperlink: '/canonical-test-summer-break/My_files+instructions/testcases/data.csv' and '/canonical-test-summer-break/My_files+instructions/testcases/data_leading_0s.csv' respectively)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv" -F "data=@data_leading_0s.csv"```

   Expected Response: 400 Bad Request

   Assumption: `That the application is only meant to process only CSV files, and, that only 1 CSV file can be provided at a time`

   Response:

   ![2_files_400_Bad_Request_POST](./screenshots/2_files_400_Bad_Request_POST.png)


4. Case: Incorrect CURL syntax (assigning a variable that is not 'data' to the csv file)
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "dataa=@data.csv"```

   Expected Response: 400 Bad Request

   Response:

   ![wrong_variable_400_Bad_Request_POST](./screenshots/wrong_variable_400_Bad_Request_POST.png)


5. Case: Empty input CSV file (0 bytes)
   
   File used: Empty csv file [here](./testcases/0_bytes_file.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/0_bytes_file.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@0_bytes_file.csv"```

   Expected Response: 404 Not Found

   Response:

   ![0_Bytes_File_404_Not_Found_POST](./screenshots/0_Bytes_File_404_Not_Found_POST.png)


6. Case: Method not allowed (GET,PUT,DELETE)
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax (GET): ```curl -v http://127.0.0.1:5000/transactions```
   Syntax (DELETE): ```curl -v -X DELETE http://127.0.0.1:5000/transactions```
   Syntax (PUT): ```curl -v -X PUT http://127.0.0.1:5000/transactions -F "data=@data.csv"```

   Expected Responses: 405 Method not allowed

   Response:

   ![transactions_api_test_GET_not_allowed](./screenshots/transactions_api_test_GET_not_allowed.png)

   ![transactions_api_test_DELETE_not_allowed](./screenshots/transactions_api_test_DELETE_not_allowed.png)

   ![transactions_api_test_PUT_not_allowed](./screenshots/transactions_api_test_PUT_not_allowed.png)


7. Case: Payload/file too large (>16MB)
   
   File used: big csv file (>16MB) [here](./testcases/big_csv.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/big_csv.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@big_csv.csv"```

   Expected Response: 413 Payload Too Large

   Assumption: `The provided CSV file is not expected to be processed if its >16MB (as this is the FLASK payload limit)`

   Response:

   ![Big_File_response_413_POST](./screenshots/Big_File_response_413_POST.png)


8. Case: Unsupported Media Type, Incorrect file extension
   
   File used: a txt file [here](./testcases/data_unsupported.txt) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_unsupported.txt)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_unsupported.txt"```

   Expected Response: 415 Unsupported Media Type

   Assumption: `That the application is only meant to process only CSV files`

   Response:

   ![Incorrect_File_ext_response_415_POST](./screenshots/Incorrect_File_ext_response_415_POST.png)


9. Case: Unsupported Media Type, corrupted file/not encoded in utf-8
   
   File used: Corrupted file not encoded in utf-8 [here](./testcases/corrupted_file.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/corrupted_file.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@corrupted_file.csv"```

   Expected Response: 415 Unsupported Media Type

   Assumption: `The provided CSV file is always encoded in utf-8 format (application will throw a HTTP 415 error otherwise) or at least utf-8 is backwards compatible with the encoding; files not encoded in this way won't be processed`

   Response:

   ![Corrupted_File_response_415_POST](./screenshots/Corrupted_File_response_415_POST.png)


10. Case: 422 columns A-D are not filled properly in the csv file
   
   File used: File with columns A-D not filled [here](./testcases/data_A-D_not_filed.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_A-D_not_filed.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_A-D_not_filed.csv"```

   Expected Response: 422 Unprocessable Content

   Assumption: `That for any given row, only columns A-D are meant to be filled out in the CSV, else should be unprocessable`

   Response:

   ![Missing_col_A_D_response_422_POST](./screenshots/Missing_col_A_D_response_422_POST.png)


11. Case: More than 4 column entries in a particular row in the csv file
   
   File used: File with more than 4 column entries in a row [here](./testcases/data_more_than_4.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_more_than_4.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_more_than_4.csv"```

   Expected Response: 422 Unprocessable Content

   Response:

   ![Too_Many_col_entries_response_422_POST](./screenshots/Too_Many_col_entries_response_422_POST.png)


12. Case: Incorrectly formatted date, format as yyyy-mm-dd
   
   File used: File with incorrect date field format [here](./testcases/data_incorrect_date_format.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_incorrect_date_format.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_incorrect_date_format.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`

   `That for the date field, the format is supposed to be as such: YYYY-mm-dd, and all other format will be unprocessable`

   Response:

   ![Incorrect_date_format_response_422_POST](./screenshots/Incorrect_date_format_response_422_POST.png)


13. Case: Date entries are not all from the same year
   
   File used: File with date fields not all from the same year [here](./testcases/data_not_all_of_same_yr.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_not_all_of_same_yr.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_not_all_of_same_yr.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`

   `That entries are all meant to be within the same year (i.e.: YYYY in date field are all the same), else should be unprocessable`

   Response:

   ![Not_Same_Year_response_422_POST](./screenshots/Not_Same_Year_response_422_POST.png)


14. Case: Type field is incorrectly formatted type; specify either 'expense' or 'income'
   
   File used: File with incorrect type field [here](./testcases/data_type_field_wrong.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_type_field_wrong.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_type_field_wrong.csv"```

   Expected Response: 422 Unprocessable Content

   Assumption: `That entries within the CSV will not be entered with commas` 

   Response:

   ![Incorrect_Type_response_422_POST](./screenshots/Incorrect_Type_response_422_POST.png)


15. Case: Memo field does not have any English characters (a-z)
   
   File used: File with incorrect memo field [here](./testcases/data_memo_field_wrong.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_memo_field_wrong.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_memo_field_wrong.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas`

   `That for a memo field to be valid, it should contain at least 1 alphabetic character (a-z) and not be only numbers` 

   Response:

   ![Incorrect_Memo_response_422_POST](./screenshots/Incorrect_Memo_response_422_POST.png)


16. Case: Amount field is an invalid float ($ symbol infront of number)
   
   File used: File with invalid float for the amount field [here](./testcases/data_invalid_float.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_invalid_float.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_invalid_float.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`

   `That for the amount field the user can input negative numbers, but, scientific notation may not be processable (e.g.: 3E10) and currency notation (e.g.:$30) will be unprocessable`

   Response:

   ![Amount_Invalid_Float_response_422_POST](./screenshots/Amount_Invalid_Float_response_422_POST.png)


17. Case: Amount field is greater than 32 bits
   
   File used: File with amount field >32 bits [here](./testcases/data_33_bit_amount.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_33_bit_amount.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_33_bit_amount.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`

   `That for the amount field the upper limit is a 32 bit number (i.e.:4294967295), and, to be honest, even this number is unrealistic`

   Response:

   ![Amount_GT_32_bits_response_422_POST](./screenshots/Amount_GT_32_bits_response_422_POST.png)


18. Case: Amount field has greater than 2 decimal places
   
   File used: File with amount field > 2 decimal places [here](./testcases/data_greater_than_2_decimals.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data_greater_than_2_decimals.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data_greater_than_2_decimals.csv"```

   Expected Response: 422 Unprocessable Content

   Assumptions: `That entries within the CSV will not be entered with commas (e.g.:'18,77' for amount or '2020,07,01' for date or 'Repairs, Gas, and 219 Pleasant' for memo would not be valid)`

   `That for the amount field in the CSV, the cell would be formated as a 'number' with at most 2 decimal places; any more than 2 decimal places and it will be unprocessable (unrealistic money value)`

   Response:

   ![Amount_GT_2_decimal_response_422_POST](./screenshots/Amount_GT_2_decimal_response_422_POST.png)


19. Case: Internal Server Error
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax: ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv"```

   Expected Response: 500 Internal Server Error

   Response:

   ![Internal_Server_Error_500_POST](./screenshots/Internal_Server_Error.png)

   Logs (/var/log/idle.err.log log):

  ![/var/log/idle.err.log log](./screenshots/idle_err_log.png)


##### Test Report API Testcases

1. Case: standard correct data
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax (POST FIRST): ```curl -v -X POST http://127.0.0.1:5000/transactions -F "data=@data.csv"```

   Syntax (GET AFTER): ```curl -v http://127.0.0.1:5000/report```

   Expected Response: 200 OK

   Assumptions: `Once transactions have been processed via the transactions API, you would only be able to GET the tally once via the report API before you would need to POST again (prevents a different user from stealing the 1st users' tally info)`

   Response:

   ![standard_200_OK_POST](./screenshots/standard_200_OK_POST.png)

   ![standard_200_OK_GET](./screenshots/standard_200_OK_GET.png)


2. Case: No content: use GET /report a 2nd time after processing a transaction or use GET /report without processing a transaction
   
   Syntax: ```curl -v http://127.0.0.1:5000/report```

   Expected Response: 204 No Content

   Assumptions: `Once transactions have been processed via the transactions API, you would only be able to GET the tally once via the report API before you would need to POST again (prevents a different user from stealing the 1st users' tally info)`

   Response:

   ![No_Content_204_GET](./screenshots/No_Content_204_GET.png)


3. Case: Method not allowed (POST,PUT,DELETE)
   
   File used: standard correct data [here](./testcases/data.csv) (if you are unable to click the hyperlink: /canonical-test-summer-break/My_files+instructions/testcases/data.csv)

   Syntax (GET): ```curl -v -X POST http://127.0.0.1:5000/report -F "data=@data.csv"```
   Syntax (DELETE): ```curl -v -X DELETE http://127.0.0.1:5000/report```
   Syntax (PUT): ```curl -v -X PUT http://127.0.0.1:5000/report -F "data=@data.csv"```

   Expected Responses: 405 Method not allowed

   Response:

   ![report_api_test_POST_not_allowed](./screenshots/report_api_test_POST_not_allowed.png)

   ![report_api_test_DELETE_not_allowed](./screenshots/report_api_test_DELETE_not_allowed.png)

   ![report_api_test_PUT_not_allowed](./screenshots/report_api_test_PUT_not_allowed.png)


4. Case: Internal Server Error

   Syntax: ```curl -v http://127.0.0.1:5000/report```

   Expected Response: 500 Internal Server Error

   Response:

   ![Internal_Server_Error_500_POST](./screenshots/Internal_Server_Error.png)

   Logs (/var/log/idle.err.log log):

  ![/var/log/idle.err.log log](./screenshots/idle_err_log.png)


## My Solution's Shortcomings

Based off the assumptions I made I can conclude that the shortcomings to my solution (as far as I'm aware of) is as follows:

   - `The setup to my solution is only Linux/Debian compliant`
   - `The application runs on port 5000, and, hence isn't very secure (it should run on port 443/https with SSL certificate)`
   - `The application can only handle 1 user at a time, and, therefore is not very scalable if many users were required to be using this concurently`
   - `Lack of a database and redundancy on the node/Flask server itself means that if the server shuts down/reboots, data is lost (i.e.: no external caching/session storage)`
   - `Lack of login security or API Keys/SSO authentication means that theoretically, any user could obtain another users' transaction data if they are quick enough with calling the report api`
   - `No DNS hostname resolution means that the application could be hard to find, and, only runs on 1 localhosts' machine`
   - `No GUI means that, unless you know how to work with APIs (i.e.: you're a software dev), you wouldn't know how to use the application; not non-tech user friendly`
   - `Due to the method in which I saved data, the user is unable to add data to transacations (same year) that they may have forgotten about, but, was supposed to be added to the sheet (as a sperate csv)`
   - `My solution doesn't support any encoding that is not backwards compatible with utf-8; this means LATIN-1 encoding that Western Europe uses is not included and this excludes a substantial client base`
   - `My solution can't process files that are greater than 16MB`
   - `Saving the input data locally to a /tmp/ folder isn't ideal (for security reasons)`
   - `My solution can't handle CSV files that could possibly have headers`
   - `My solution can't handle any files other than CSV files (maybe Excel is preferred for some users)`
   - `My solution can't always handle scientific notation amounts, and, can't ever handle amounts in which a '$' precedes the value`
   - `My solution is useless to the extremely wealthy, as, it can't handle amounts greater than 32 bits`

## Additions & Refinements

Based off what I wrote for my solution's shortcomings, I can conclude that the following is what I would like to add or refine (if I had time - albeit, some of these are lengthy solutions):

   - `I would want to add instructions for a setup in Windows, Mac, and other Linux distributions`
   - `I would setup an SSL certificate and run the application on port 443 (HTTPS) so that the connection is more secure`
   - `To handle concurency, I would need to utilize a database, and setup API keys/authentication such that each user can retrieve their own unique data, and only if they are permitted to`
   - `Adding a database (e.g.: sqlite) I could ensure that data is not lost, provided I also ensure there's redundancy to the database`
   - `Along with a GUI/frontend, I would like to add a login screen as well to identify each unique user easily and for security purposes; the frontend/GUI would also make it non-tech user friendly`
   - `Setup DNS hostname resolution so that the applicaiton is easier to find`
   - `I would add a method to ensure I could deal with files of any encoding type (provided that the file is not corrupted)`
   - `I would add a method to handle files greater than 16 MB`
   - `Files wouldn't need to be saved locally if I had a database/session storage`
   - `This solution could prove to be expensive, but, I would add site and geo redundancy to my Flask server`
   - `I would find a way to handle all types of files (Excel, CSV, etc), and handle potential file headers`
   - `I would find a way to handle scientific notation and currency notation for amount fields`




























