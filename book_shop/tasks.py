import os
import hashlib
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile

from book_shop.api import get_book_data
from book_shop.models import Book, Category


@shared_task
def update_book_data():
    books = Book.objects.all()

    for book in books:
        book_data = get_book_data(book.title)
        if book_data:
            if book.author != book_data['author']:
                book.author = book_data['author']
            if book.publisher != book_data['publisher']:
                book.publisher = book_data['publisher']
            if book.published_date != book_data['published_date']:
                book.published_date = book_data['published_date']
            if book.category.name != book_data['category']:
                category, _ = Category.objects.get_or_create(name=book_data['category'])
                book.category = category

            new_image_hash = hashlib.md5(book_data['image_data']).hexdigest()
            old_image_hash = hashlib.md5(book.image.read()).hexdigest()
            if old_image_hash != new_image_hash:
                if book.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(book.image))
                    if os.path.exists(image_path):
                        os.remove(image_path)

                book.image.save(f'{book.title}.jpg', ContentFile(book_data['image_data']), save=True)
                book.image_hash = new_image_hash

            book.save()