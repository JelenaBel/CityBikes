## Project - City Bikes​
#### Link to the project web-site - http://rabbid.ddns.net:8000/

#### This is the pre-assignment for the Solita Dev Academy Finland 2023. 
Project includes UI and a backend service for displaying data from journeys made with city bikes in the Helsinki Capital area.
The data used in the project is owned by City Bike Finland.  Dataset includes information about Helsinki Region Transport’s (HSL) city bicycle stations

#### Main goals: ​

```
To provide customers with highly developed versatile servise to work with the 
statistic information about CityBikes usage in Helsinki and Espoo area. This 
statistic and analytical information might be used to imporove CityBikes service, 
to better understanding of customers needs and habits,  as well as information 
about trouble or misusage of CityBikes service. ​
​
 
```

#### Technical description: 
- Project scope: Python web-application. ​
- Framework: Django ​
- Database: SQLite. ​
- Languages: Python, JavaScript, HTML, CSS,  SQL. ​
- Design-framework: Bootstrap ​
- Publishing:  GitHub.​
- IDE: PyCharm​
- Additions: Pillow, pip.​


#### Prerequisites: ​
Python 3.10 ​

To run the project please install:_​_
Python 3.10 . ​You can find instructions for Python installation here - www.python.org​

Django 4.1.5 ​

This is the recommended way to install Django.​
Install pip. ​
The easiest is to use the standalone pip installer. ​
If your distribution already has pip installed, you might need to update it if it’s outdated. ​
If it’s outdated, you’ll know because installation won’t work.
Take a look at venv. ​
This tool provides isolated Python environments, which are more practical than installing packages systemwide. It also allows installing packages without administrator privileges. The contributing tutorial walks through how to create a virtual environment.

After you’ve created and activated a virtual environment, enter the command:​

For Windows:   ...\> py -m pip install Django​

For Linux/Mac:   $ python -m pip install Django​


Pillow 9.4.0 ​

For Windows:    pip install Pillow ​

For Linux/Mac: ​

Check  first if pip3 and python3 are correctly installed.​

python3 --version​

pip3 --version​

pip3 install --upgrade pip (if needed)​

pip3 install Pillow​


### Guide to run this project:

#### Configuration: ​
#### Database. ​

In project is used SQLite database, provided with Django. Additional installation is not needed. 
Before running the project database tables should be created by running commands:​
python manage.py makemigrations​
python manage.py migrate​

#### Launch class. ​

In order to fill the database with information provided by CityBikes and HLS please 
open main/views.py and carefully uncomment code from lines 15 until line 31. Leave the comment signs only on the rows with the text explanations. 

Launching will take form 16 to 24 hours. So long time needed to fill in the database wil 3 mln rows of the information. 
Because of the size of database, file with already created database can not be added to GitHub. 

With your request I can send ready database (size - 400 mb) in zip file. Please contact - elena.belousova@gmail.com

Or see this project published http://rabbid.ddns.net:8000/ with whole database information. ​

After filling up the database please open main/views.py and carefully comment back all lines from line 15 until line 33 (included). ​

#### Run ready project
To run project on your computer, use terminal in your IDE (VSCode, PyCharm) or any other which supports Python with command:​

python manage.py runserver​

#### Admin or User Mode

To switch from Admin to User view and back please use button User Mode on top navigation menu. 


#### Tests
Project now includes 25 tests. 
To run tests in this project, please use terminal in your IDE with command: 

python manage.py test main

#### Project main features:

- Responsive design​
- fixed top menu​
- dynamic pages​
- search functionality
- pagination
- filtering
- ordering by tables columns,
- information about stations with map
- total and monthly statistic for each station
- information about routes with map
- multi/table database with primary and foreign keys​
- admin mode (created without logins only for the demonstration purposes)
- CMS features> adding, updating, deleting information. 
- database includes 3 200 000 rows of information. (457 stations and 3 200 000 routes)



#### Project structure:
- Main page with main statistic   ​
- Stations list page with search, sorting and pagination​
- Own station page with address, capacity info and total and monthly statistic of station usage​

- Routes list pages with search, sorting, filtering and pagination​
- Own route page with map and route information ​
- Special admin mode for wider functionality - adding, deleting and updating the information about stations and routes ​

- To keep consistency and fullness of the database information from HSL and CityBikes, admin functionality available only for new stations. In order to test this functionality create new station or new route first. 

