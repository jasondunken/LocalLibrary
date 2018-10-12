from django.urls import path
from catalog import views

# this is where patterns are added specific to this application 'catalog'
# this is accessed by the include in locallibrary/locallibrary/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserView.as_view(), name='my-borrowed'),
    path('staff/allborrowed/', views.LoanedBooksAllView.as_view(), name='all-borrowed'),
    # things a a bit different when linking to forms, notice the lack of .as_view()
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]