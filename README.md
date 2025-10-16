Overview -
This project allows uploading a CSV file to store user details
It validates each record and provides a summary of valid and rejected rows

Endpoints -
POST /api/upload/ -> to upload csv
GET /api/upload_file/ -> simple html upload form

Setup & Run -
Create database and apply migrations
python manage.py makemigrations
python manage.py migrate

Run code -
python manage.py runserver

Tests -
python manage.py test csvapp