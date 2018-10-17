import uuid

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from datetime import date

# Create your models here.
# ALL UR MODELS BELONG TO HERE!


class SomeTypicalModel(models.Model):
    """this is an example of a typical class that defines a model"""

    # models have fields, as many as you like
    # - each one represents a column of data in your database
    # - each database record contains one of each of your fields

    awesome_field = models.CharField(max_length=200, help_text="Example of what to enter")
    """assigning a field type wraps the input to the field and ensures it is appropriately validated
        - the field name is what is used to create a 'label' for the field
        - this label uppercases the first letter and replaces _ with ' ' it might even pluralize
        - unless that is you use the 'verbose_name' argument"""

    # *COMMON FIELD ARGUMENTS*
    # help_text - this is the text label for the html
    # verbose_name - this replaces the default label for the field
    # default - the default value for the field, it can be an object(which gets called when a new record is made)
    # null - if True, it will store NULL for a blank value, default is False
    # blank - if True, field is allowed to be blank, if False django validation will force you to enter a vaue
    # choices - a group of choices for this field, takes an iterable
    # primary_key - if True this field will be the primary key for the model/group of fields in the database

    # *COMMON FIELD TYPES*
    # CharField() - short to mid sized fixed length strings
    # TextField() - large arbitrary length strings
    # IntegerField() - integers, duh, use when validation is required
    # DateField() - used for date and time information
    # EmailField() - validate and store email addresses
    # FileField() and ImageField() used to upload files and images,
    # - ImageField verifies it's an image, arguments define file path for both
    # AutoField() - is an auto incrementing integer field.
    # - if you don't specify a primary_key, you get one of these as your primary_key
    # ForeignKey() - is used to specify a one-to-many relationship. The one is the one that has this key
    # ManyToManyKey() - "a book can have several genres, and each genre can contain several books"

    class Meta:
        ordering = ['-awesome_field']

        # you can also use verbose_name here to change the default label for the class
        verbose_name = 'EvenMoreAwesomeName'

        # there's lots of stuff you can put in here

    """AT THE MINIMUM YOU NEED TO OVERRIDE __str__() to return a human readable string for each object"""
    def __str__(self):
        return self.awesome_field

    def get_absolute_url(self):
        """returns the url of a particular instance of this model"""
        return reverse('sometypicalmodel-detail', args=[str(self.id)])


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    # a foreign key is used because a book can have only one author(?), but authors can have many books
    # author as a string instead of object because it hasn't been declared in the file yet
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/'
                                                             'content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Enter unique ID for this particular book")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    # user that has this instance borrowed
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        # check if self.due_back is NULL them compare current date to due_back
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'set_as_book_returned'),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (('can_create_author', 'can_create_author'),)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):

    language = models.CharField(
        max_length=100,
        help_text="Pick a language"
    )

    class Meta:
        ordering = ['language']

    def __str__(self):
        return self.language
