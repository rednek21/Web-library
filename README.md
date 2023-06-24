# Web-library
Web library using Google Books API

This project is for my "Internet-technologies" university course work. It was necessary to create a simple web-application.
Working with an external API was proposed by the university lecture of the law of obtaining the highest score.

The application provides the ability to add new books, delete existing ones, edit information for each one. 
If you change the book title, all data for the object will update according to the new tltle. 
To track changes, a function was written that makes a new request in google books for each available book once every 5 seconds (value was selected for the tests. You can change it in settings.py)
If a new image for the book is received on request, it will be used as a cover and the old image will be deleted.

So, here you can see how to run the app:
1. Create your virtual environment
2. Create your database. If you want to use database different from PostgreSQL, edit the appropriate fields in settings.py
3. Create ".env" file in the project root folder. Then edit it using your own data
4. pip install -r requirements.txt
5. python3 manage.py runserver
6. celery -A shop worker -l info
7. celery -A shop beat -l info

If everything is done correctly, try to use the app :)
