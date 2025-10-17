Task 1

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

Task 2

Overview-
This task implements a custom rate limiting middleware in Django that restricts requests based on the client’s IP address Each IP address can make up to 100 requests every 5 minutes If this limit is exceeded the API responds with HTTP 429 (Too Many Requests)

Logic used
1. Each request’s IP is used as a key in Django’s cache.
2. The middleware stores timestamps of all requests from that IP.
3. If the number of requests in the last 5 minutes exceeds 100, the response is blocked.
4. A custom header X-RateLimit-Remaining shows how many requests are left.

