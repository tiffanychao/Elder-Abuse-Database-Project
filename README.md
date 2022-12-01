# Description of Project Files
This section is going to describe the different folders and files within this project:

files: example files used to test functionalities
static: the folder that holds the css files used to styize the pages
templates: the folder that holds the html files
uploads: the uploads folder is used to store the attachments that are associated with the cases
app.py: the main file that has the main logic and routes
docToSql.py: file used to handle logic from turning microsoft word form to sql database
worddocparser.py: file that was developed by last year's team to parse the Microsoft word form. 



# Elder-Abuse-Database-Project
How to run if version of flask is less than version 2.2:

1.) Go to the project directory 

2.) run the following command `export FLASK_APP=app.py`

3.) run `export FLASK_ENV=development`

4.) then run `flask run`


if version of flask is 2.2:

1.) run `flask --app app --debug run` instead
