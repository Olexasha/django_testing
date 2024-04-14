from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


class TestPagesAvailability(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.author = User.objects.create(username="Автор")
        cls.note = Note.objects.create(
            title="Заголовок",
            text="Текст заметки",
            slug="note-slug",
            author=cls.author,
        )
        cls.reader = User.objects.create(username="Не автор")
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_pages_availability_for_anonymous_user(self):
        urls = ("notes:home", "users:login", "users:logout", "users:signup")
        for name in urls:
            url = reverse(name)
            with self.subTest(name=name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = ("notes:list", "notes:add", "notes:success")
        self.client.force_login(self.author)
        for name in urls:
            url = reverse(name)
            with self.subTest(name=name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        urls = ("notes:detail", "notes:edit", "notes:delete")
        self.client.force_login(self.author)
        for name in urls:
            url = reverse(name, args=(self.note.slug,))
            with self.subTest(name=name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = ("notes:detail", "notes:edit", "notes:delete")
        for name in urls:
            url = reverse(name, args=(self.note.slug,))
            for client in (self.author_client, self.reader_client):
                with self.subTest(name=name):
                    response = client.get(url)
                    expected_status = (
                        HTTPStatus.OK
                        if client == self.author_client
                        else HTTPStatus.NOT_FOUND
                    )
                    self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        urls = (
            ("notes:detail", ("note-slug",)),
            ("notes:edit", ("note-slug",)),
            ("notes:delete", ("note-slug",)),
            ("notes:add", None),
            ("notes:success", None),
            ("notes:list", None),
        )
        login_url = reverse("users:login")
        for name, args in urls:
            url = reverse(name, args=args)
            with self.subTest(name=name):
                response = self.client.get(url)
                expected_url = f"{login_url}?next={url}"
                self.assertRedirects(response, expected_url)
