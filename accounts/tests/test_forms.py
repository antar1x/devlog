from django.test import TestCase

from accounts.forms import ProfileUpdateForm, RegisterForm, SearchForm


class RegisterFormTests(TestCase):
    def test_register_form_is_valid_with_correct_data(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertTrue(form.is_valid())

    def test_register_form_is_invalid_when_passwords_do_not_match(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'OtherPass123',
        })

        self.assertFalse(form.is_valid())


class SearchFormTests(TestCase):
    def test_search_form_is_valid_with_username(self):
        form = SearchForm(data={
            'username': 'testuser',
        })

        self.assertTrue(form.is_valid())

    def test_search_form_is_invalid_without_username(self):
        form = SearchForm(data={})

        self.assertFalse(form.is_valid())


class ProfileUpdateFormTests(TestCase):
    def test_profile_update_form_is_valid(self):
        form = ProfileUpdateForm(data={
            'bio': 'Python and Django learner',
            'is_public': True,
        })

        self.assertTrue(form.is_valid())
