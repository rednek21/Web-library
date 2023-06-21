import requests
from django.conf import settings


def get_book_data(title):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f'intitle:{title}',
        'maxResults': 5,
        'key': settings.API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'items' in data:
        for item in data['items']:
            book_data = item['volumeInfo']
            image_links = book_data.get('imageLinks')
            thumbnail_url = image_links.get('thumbnail') if image_links and 'thumbnail' in image_links else None

            if thumbnail_url:
                response = requests.get(thumbnail_url)
                if response.status_code == 200:
                    image_data = response.content
                    author = book_data.get('authors', ['Unknown'])[0]
                    category = book_data.get('categories', ['Unknown'])[0]
                    published_date = book_data.get('publishedDate', 'Unknown')
                    publisher = book_data.get('publisher', 'Unknown')

                    return {
                        'author': author,
                        'category': category,
                        'published_date': published_date,
                        'publisher': publisher,
                        'image_data': image_data
                    }

        first_item = data['items'][0]
        book_data = first_item['volumeInfo']
        author = book_data.get('authors', ['Unknown'])[0]
        category = book_data.get('categories', ['Unknown'])[0]
        published_date = book_data.get('publishedDate', 'Unknown')
        publisher = book_data.get('publisher', 'Unknown')

        return {
            'author': author,
            'category': category,
            'published_date': published_date,
            'publisher': publisher,
            'image_data': None
        }

    return None
