# data-team-rich
Rich Haussmann Interview

# Technical Exercise
Fork this repo\
Add functionality to the application as outlined below\
Submit a PR back to the repo with your work\
# Notes
Feel free to use any anything in the Python standard library or any 3rd party packages in order to complete the exercise.\ 
Freeze any packages you use in requirements.txt.\
Feel free to use Python 2 or 3.\
Add new files, custom classes, additional functions or anything else as you see fit.\ 
Do your best to conform to PEP 8 coding standards.\
Document your code as best you can.\
# Tasks
You should add functionality to the application in order to:\
Parse the included delimited file.\
Insert the results into a database.\
Display the results.\
Parse the included delimited file\
Use any method you choose to parse the delimited file as long as you:\
Clean the data so that it may be inserted into the database using the data types you select in the next step.\
Try to use SQL to do this and not Python. \
In addition, save the results to a new gzipped CSV file.\
Insert the results into a database\
Insert the results into a PostgreSQL table.\
Select proper data types for each column and create a table using these data types.\
Add new columns if necessary\
In your pull request back to the DFM repository, include the DDL you used to create the results table.\
Make any comments if necessary on your choices.\
Also include a dump of the results table in your PR back to the repo.\
Display the results\
A single button at the / route should parse, write the file, insert into the database and then redirect to /results that shows the parsed results in an HTML table\.
Don’t worry about styling here. We’re not front-end developers.\
The primary purpose is just to show retrieving and iterating over results from a database. If you’d like to show that in some fashion other than displaying a page in a Flask app, feel free to do that instead.

