CS2102-Project
--

If you want to get the database up and running on your own computer, here's what you do:

1. Download the SQLCode file, move everything in it (not the folder itself, all the files in it) to the folder where SQLite3.exe is on your computer (or whatever your preferred SQL program is).
2. Run the SQL command ".read createDatabase.txt"


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



