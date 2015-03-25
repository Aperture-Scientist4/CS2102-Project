CS2102-Project
--
How to make the website work:
1. download python and django
2. pull all the changes in github and make sure your local version is the newest.
3. For Windows, open cmd in the folder contained manage.py and run command "python manage.py startserver"
4. Use browser go to http://127.0.0.1:8000/store/

If you want to get the database up and running on your own computer, here's what you do:

1. Download the SQLCode file, move everything in it (not the folder itself, all the files in it) to the folder where SQLite3.exe is on your computer (or whatever your preferred SQL program is).
2. Run the SQL command ".read createDatabase.txt"    (Note the lack of semicolon. It doesn't work if you put a semicolon.)


If you want to get the database off your computer, run the command: ".read cleanSlate.txt"

If you royally screw up and want to start the database over from the create and fill tables, run the command: ".read resetEverything.txt"


To Do: 
1. Finish the database, populate with fake games, reviews, etc 
2. Make front end web interface 
3. Do back end stuff

Note: There is a tutorial on PHP posted to the CS2102 IVLE website.

Setup
--
```
python manage.py migrate
python manage.py makemigrations store
python manage.py sqlmigrate store 0001
python manage.py syncdb
```



