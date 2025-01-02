# ALTIUS API TEST

## Overview
````
This test suite evaluates the login functionality and deal retrieval endpoints of the system. 
The tests are designed to verify successful login, various failure scenarios, 
lockout mechanisms, and proper authorization for retrieving deals.
````
## Pip Install
````
Execute the following command in the terminal to install the required packages: 
"pip install -r requirements.txt"

This will install the following dependencies:

certifi==2024.12.14
charset-normalizer==3.4.1
colorama==0.4.6
idna==3.10
iniconfig==2.0.0
packaging==24.2
pluggy==1.5.0
pytest==8.3.4
requests==2.32.3
urllib3==2.3.0
````
## Run:
````
To test the API endpoints, execute the following command in the terminal:
"pytest app/tests/altius_api_tests.py"
````