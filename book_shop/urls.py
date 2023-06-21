from django.urls import path
from .views import IndexView, NewCategoryView, NewBookView, delete_book, EditBookView, BookShopErrorView

app_name = 'book_shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:category_id>/', IndexView.as_view(), name='index_list_by_category'),
    path('new_book/', NewBookView.as_view(), name='new_book'),
    path('edit_book/<int:book_id>/', EditBookView.as_view(), name='edit_book'),
    path('new_category/', NewCategoryView.as_view(), name='new_category'),
    path('<int:book_id>/delete/', delete_book, name='delete_book'),
    #path('<int:category_id>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    path('error/', BookShopErrorView.as_view(), name='error'),

]

