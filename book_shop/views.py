import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Category, Book
from common.mixins import TitleMixin

from .forms import NewBookForm, NewCategoryForm, EditBookForm


class IndexView(TitleMixin, ListView):
    template_name = 'book_shop/index.html'
    context_object_name = 'books'
    paginate_by = 10
    html_title = 'Главная'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            category = get_object_or_404(Category, id=category_id)
            queryset = Book.objects.filter(category=category)
        else:
            queryset = Book.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NewBookView(TitleMixin, CreateView):
    model = Book
    form_class = NewBookForm
    template_name = 'book_shop/new_book.html'
    success_url = reverse_lazy('book_shop:index')
    html_title = 'Добавление книги'

    def form_invalid(self, form):
        error_message = form.errors.as_text()
        logging.error(f"Ошибка при создании книги: {error_message}")
        return redirect('book_shop:error')


class EditBookView(TitleMixin, UpdateView):
    model = Book
    template_name = 'book_shop/edit_book.html'
    form_class = EditBookForm
    success_url = reverse_lazy('book_shop:index')
    html_title = 'Редактирование информации о книге'

    def get_object(self, queryset=None):
        return get_object_or_404(Book, id=self.kwargs['book_id'])

    def form_invalid(self, form):
        error_message = form.errors.as_text()
        logging.error(f"Ошибка при Редактировании книги: {error_message}")
        return redirect('book_shop:error')


class NewCategoryView(TitleMixin, CreateView):
    model = Category
    form_class = NewCategoryForm
    template_name = 'book_shop/new_category.html'
    success_url = reverse_lazy('book_shop:index')
    html_title = 'Добавление категории'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def delete_book(request, book_id):
    product = get_object_or_404(Book, id=book_id)
    product.delete()
    return HttpResponseRedirect(reverse('book_shop:index'))


class BookShopErrorView(TemplateView):
    template_name = 'book_shop/error.html'
