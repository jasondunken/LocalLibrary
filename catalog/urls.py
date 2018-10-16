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
    path('allborrowed/', views.LoanedBooksAllView.as_view(), name='all-borrowed'),
    path('book/create', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
    path('author/create', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name='author-delete'),
    # as with the index path above, things are a bit different when linking to function defined views,
    # notice the lack of .as_view()
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
