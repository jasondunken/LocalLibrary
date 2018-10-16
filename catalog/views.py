from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.models import Author, Book, BookInstance
from catalog.forms import RenewBookForm




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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request, it is not the first request, so okay to process request
    if request.method == 'POST':
        book_renewal_form = RenewBookForm(request.POST)

        # check that the form is valid
        if book_renewal_form.is_valid():
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/renew_book_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    # the fields attrib defines which fields to show on form
    fields = '__all__'  # this shows all the fields for a given model

    # you can set initial values for fields using a dict syntax
    initial = {'date_of_death': '05/01/2018'}

    # in the CreateView view, upon success, a redirect to the newly created/edited model instance is called


class AuthorUpdate(UpdateView):
    model = Author
    # here the fields to be displayed are being explicitly defined
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    # in the UpdateView view, upon success, a redirect to the newly created/edited model instance is called


class AuthorDelete(DeleteView):
    model = Author
    # in the above views, upon success, a redirect to the previous page is called
    # here a success redirect url is explicitly defined
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book

    success_url = reverse_lazy('books')


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


