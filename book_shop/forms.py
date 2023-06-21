from django import forms
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse

from .api import get_book_data

from .models import Category, Book


class NewBookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'label': 'Название книги'
    }))

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if not title:
            raise forms.ValidationError('Некорректное название книги')

        book_data = get_book_data(title)
        if book_data is None:
            raise forms.ValidationError('Книга не найдена')

        return cleaned_data

    def save(self, commit=True):
        title = self.cleaned_data['title']
        book_data = get_book_data(title)

        if book_data:
            category_name = book_data['category']
            category, _ = Category.objects.get_or_create(name=category_name)

            book = Book(
                title=title,
                author=book_data['author'],
                publisher=book_data['publisher'],
                published_date=book_data['published_date'],
                category=category,
            )
            book.image.save(f'{title}.jpg', ContentFile(book_data['image_data']), save=True)
            if commit:
                book.save()
            return book
        else:
            return HttpResponseRedirect(reverse('book_shop:error'))

    class Meta:
        model = Book
        fields = ('title',)


class EditBookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    author = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    publisher = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control-file', 'accept': 'image/*'
    }), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if not title:
            raise forms.ValidationError('Некорректное название книги')

        book_data = get_book_data(title)
        if book_data is None:
            raise forms.ValidationError('Книга не найдена')

        return cleaned_data

    def save(self, commit=True):
        book = super().save(commit=False)
        old_title = book.title
        new_title = self.cleaned_data['title']

        if old_title != new_title:
            book_data = get_book_data(new_title)
            if book_data:
                category_name = book_data['category']
                category, _ = Category.objects.get_or_create(name=category_name)

                book.title = new_title
                book.author = book_data['author']
                book.publisher = book_data['publisher']
                book.published_date = book_data['published_date']
                book.category = category
                #book.image.save(f'{new_title}.jpg', ContentFile(book_data['image_data']), save=True)
                book.image = book_data['image_data']
        if commit:
            book.save()
        return book

    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher',
                  'image', 'category')


class NewCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Category
        fields = ('name',)
