from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from catalog.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 8

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Billy {author_id}',
                last_name=f'Bob {author_id}',
            )

        test_user = User.objects.create_user(username='test_user', password='password')
        test_user.save()

    def test_view_url_exists_at_desired_location(self):
        self.login_user()
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login_user()
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_uses_correct_template(self):
        self.login_user()
        response = self.client.get(reverse('authors'))
        print("Response | context: "), print(response), print(response.context)
        self.assertTemplateUsed(response, 'catalog/author_list.html')
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        self.login_user()
        response = self.client.get(reverse('authors'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 5)
        self.assertEqual(response.status_code, 200)

    def test_lists_all_authors(self):
        self.login_user()
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)
        self.assertEqual(response.status_code, 200)

    def login_user(self):
        self.client.login(username='test_user', password='password')

