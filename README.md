# ALTIUS API TEST

## Overview
````
This report provides an evaluation of the system's login functionality and deal-related operations. 
The primary focus is on verifying successful user login, handling various failure scenarios, 
and ensuring proper authorization mechanisms for deal retrieval. 
In addition, the report covers the functionality of posting, updating, and deleting comments on deals,
as well as filtering forms associated with deals.
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