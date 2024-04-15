from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from notes.tests.constants import (
    NOTES_ADD,
    NOTES_ADD_URL,
    NOTES_DELETE,
    NOTES_DETAIL,
    NOTES_EDIT,
    NOTES_HOME_URL,
    NOTES_LIST,
    NOTES_LIST_URL,
    NOTES_SUCCESS,
    NOTES_SUCCESS_URL,
    USERS_LOGIN_URL,
    USERS_LOGOUT_URL,
    USERS_SIGNUP_URL,
)
from notes.tests.fixtures import setup_common_fixtures


class TestPagesAvailability(TestCase):
    @classmethod
    def setUpTestData(cls):
        common_fixtures = setup_common_fixtures()
        cls.author = common_fixtures["author"]
        cls.reader = common_fixtures["reader"]
        cls.note = common_fixtures["note"]
        cls.author_client = common_fixtures["author_client"]
        cls.reader_client = common_fixtures["reader_client"]
        cls.notes_detail_url = common_fixtures["notes_detail_url"]
        cls.notes_edit_url = common_fixtures["notes_edit_url"]
        cls.notes_delete_url = common_fixtures["notes_delete_url"]

    def test_pages_availability_for_anonymous_user(self):
        urls = (
            NOTES_HOME_URL, USERS_LOGIN_URL, USERS_LOGOUT_URL, USERS_SIGNUP_URL
        )
        for url in urls:
            with self.subTest(name=url.title()):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (NOTES_LIST_URL, NOTES_ADD_URL, NOTES_SUCCESS_URL)
        for url in urls:
            with self.subTest(name=url.title()):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        urls = (
            self.notes_detail_url, self.notes_edit_url, self.notes_delete_url
        )
        for url in urls:
            with self.subTest(name=url.title()):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = (
            self.notes_detail_url, self.notes_edit_url, self.notes_delete_url
        )
        for url in urls:
            for client in (self.author_client, self.reader_client):
                with self.subTest(name=url.title()):
                    response = client.get(url)
                    expected_status = (
                        HTTPStatus.OK
                        if client == self.author_client
                        else HTTPStatus.NOT_FOUND
                    )
                    self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        urls = (
            (NOTES_DETAIL, (self.note.slug,)),
            (NOTES_EDIT, (self.note.slug,)),
            (NOTES_DELETE, (self.note.slug,)),
            (NOTES_ADD, None),
            (NOTES_SUCCESS, None),
            (NOTES_LIST, None),
        )
        for name, args in urls:
            url = reverse(name, args=args)
            with self.subTest(name=url.title()):
                response = self.client.get(url)
                expected_url = f"{USERS_LOGIN_URL}?next={url}"
                self.assertRedirects(response, expected_url)
