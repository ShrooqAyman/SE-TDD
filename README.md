# SE-TDD

## Installation
To run tests follow this steps
1. Download project files and open with vcode 
2. run the follwing commamds in terminal
 ```bash
 .\venv\Scripts\activate
```
 ```bash
 python manage.py test
```
 
   or 
 ```bash
 coverage run --source='account' manage.py test &&  coverage report && coverage html
```
 to see coverage report
