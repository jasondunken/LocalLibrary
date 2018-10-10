from django.shortcuts import render

from catalog.models import Author, Book, BookInstance, Genre


def index(request):
    """this is the view function for the index page of the site"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status='a').count()
    # 'a' is the key defined in the BookInstance model's 'LOAN_STATUS' dict for 'status'

    num_authors = Author.objects.count()  # here the .all() is implied, could have done this on the other count calls

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)
