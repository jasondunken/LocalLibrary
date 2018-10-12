from django.shortcuts import render
from django.views import generic

from catalog.models import Author, Book, BookInstance, Genre
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



def index(request):
    """this is the view function for the index page of the site"""
    session_id = request.session.session_key
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status='a').count()
    # 'a' is the key defined in the BookInstance model's 'LOAN_STATUS' dict for 'status'

    num_authors = Author.objects.count()  # here the .all() is implied, could have done this on the other count calls

    context = {
        'session_id': session_id,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'

    paginate_by = 5

    def get_queryset(self):
        return Book.objects.all()[:10]  # gets first 10 results

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        # add things to the context here!
        return context


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'author_list.html'

    paginate_by = 5

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# class CreateNewUserView(generic.FormView):
    # model = User
    # template_name = 'registration/create_new_user.html'
    # first_name = 'none'
    # last_name = 'none'
    # username = 'none'
    # email = 'none@none'
    # password = 'password'
    #
    # user = User.objects.create_user(username, email, password)
    # user.first_name = first_name
    # user.last_name = last_name
    #
    # user.save()


