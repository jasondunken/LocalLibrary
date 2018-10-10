from django.contrib import admin

from catalog.models import Author, Book, Genre, Language, BookInstance


#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)


class AuthorBooksInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'nick_name', 'date_of_birth', 'date_of_death')
    # fields are displayed vertically by default, group in a tupple to display horizontally
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # by default ALL fields are displayed, use the exclude attribute to not display them
    # if you use the fields attribute, fields not included are excluded
    inlines = [AuthorBooksInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # setting this to 0 keeps the page from displaying filler instances to the inline

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language', 'isbn')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'due_back')

    # here we are defining the 'fieldsets' to be displayed
    # you can use 'None' for the title if you want nothing displayed
    fieldsets = (
        ('Title', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )






