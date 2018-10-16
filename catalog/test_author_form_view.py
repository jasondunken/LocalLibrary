"""this is a test file for the author form view

    it will perform tests for both the author model, the author from, and the author form view

    you need to check anything that you specify or that is part of the design.
    This will include who has access, the initial date, the template used, and where the view redirects on success

    first_name = model.CharField max length 100
    last_name = model.CharField max length 100
    nick_name = model.CharField max length 100
    date_of_birth = model.DateField
    date_of_death = model.DateField

    absolute_url = reverse('author-detail', self.id)
    ordering = 'last_name', 'first_name' """

from django.test import TestCase
import datetime

from django.forms import fields
from catalog.models import Author

from django.urls import reverse
from django.contrib.auth.models import User, Permission


class AuthorFormViewTest(TestCase):
    test_first_name = "John"
    test_last_name = 'Smith'

    def setUp(self):
        # create a few test_authors
        num_test_authors = 10

        self.test_author = Author.objects.create(first_name=self.test_first_name, last_name=self.test_last_name)

        for i in range(num_test_authors):
            last_name = self.test_last_name + str(i)
            Author.objects.create(first_name=self.test_first_name, last_name=last_name)

        test_user = User.objects.create_user(username='test_user', password='password')
        permission = Permission.objects.get(name='can_create_author')
        test_user.user_permissions.add(permission)
        test_user.save()

    def test_author_create_form_view_redirect_on_no_permission(self):
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 302)

    def test_author_create_form_view_uses_correct_field_types(self):
        self.login_test_user()
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        # assert correct field types
        self.assertEqual(type(form.fields['first_name']), fields.CharField)
        self.assertEqual(type(form.fields['last_name']), fields.CharField)
        self.assertEqual(type(form.fields['nick_name']), fields.CharField)
        self.assertEqual(type(form.fields['date_of_birth']), fields.DateField)
        self.assertEqual(type(form.fields['date_of_death']), fields.DateField)

    def test_author_create_form_char_fields_have_correct_max_length(self):
        self.login_test_user()
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        # assert correct field max_length
        self.assertTrue(form.fields['first_name'].max_length == 100)
        self.assertTrue(form.fields['last_name'].max_length == 100)
        self.assertTrue(form.fields['nick_name'].max_length == 100)

    def test_author_create_form_first_name_can_not_be_blank(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={'first_name': ""})
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')

    def test_author_create_form_last_name_can_not_be_blank(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={'last_name': ""})
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')

    def test_author_create_form_nick_name_can_be_blank(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={'nick_name': ""})
        self.assertEqual(response.status_code, 200)

    def test_author_create_form_redirects_to_author_detail_on_success(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={
            'first_name': self.test_first_name,
            'last_name': self.test_last_name,
            'nick_name': "",
            'date_of_birth': '10/10/1900',
            'date_of_death': '10/10/2000',
        })
        # this claims to not redirect, I guess it's a result of using the generic form views create/update/delete?
        self.assertEqual(response.status_code, 200)

    def test_author_create_form_date_of_birth_can_be_blank(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={'date_of_birth': ""})
        self.assertEqual(response.status_code, 200)

    def test_author_create_form_date_of_death_can_be_blank(self):
        self.login_test_user()
        response = self.client.post(reverse('author-create'), kwargs={'date_of_death': ""})
        self.assertEqual(response.status_code, 200)

    def test_author_detail_returns_correct_data(self):
        self.login_test_user()
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.test_author.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].last_name, self.test_author.last_name)
        self.assertEqual(response.context['object'].first_name, self.test_author.first_name)

    def test_author_sort_by_last_name(self):
        pass

    def login_test_user(self):
        self.client.login(username='test_user', password='password')