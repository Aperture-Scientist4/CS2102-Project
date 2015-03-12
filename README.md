CS2102-Project
--
To Do: <br />
1. Finish the database, populate with fake games, reviews, etc <br />
2. Make front end web interface <br />
3. Do back end stuff

Note: There is a tutorial on PHP posted to the CS2102 IVLE website.

Setup
--
```
python manage.py migrate
python manage.py makemigrations store
python manage.py sqlmigrate store 0001
python manage.py createsuperuser
```
