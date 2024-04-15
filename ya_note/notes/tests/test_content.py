from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.tests.constants import NOTES_ADD, NOTES_EDIT, NOTES_LIST_URL
from notes.tests.fixtures import setup_common_fixtures


class TestNotesList(TestCase):
    @classmethod
    def setUpTestData(cls):
        common_fixtures = setup_common_fixtures()
        cls.author = common_fixtures["author"]
        cls.reader = common_fixtures["reader"]
        cls.note = common_fixtures["note"]
        cls.author_client = common_fixtures["author_client"]
        cls.reader_client = common_fixtures["reader_client"]

    def test_notes_list_for_different_users(self):
        data = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in data:
            with self.subTest(user=user):
                client = Client()
                client.force_login(user)
                response = client.get(NOTES_LIST_URL)
                object_list = response.context["object_list"]
                self.assertEqual((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        data = (
            (NOTES_ADD, None),
            (NOTES_EDIT, (self.note.slug,)),
        )
        for name, args in data:
            with self.subTest(name=name):
                client = self.author_client
                url = reverse(name, args=args)
                response = client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
