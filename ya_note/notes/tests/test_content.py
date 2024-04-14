from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


class TestNotesList(TestCase):
    NOTE_LIST_URL = reverse("notes:list")

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

    def test_notes_list_for_different_users(self):
        data = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in data:
            with self.subTest(user=user):
                client = Client()
                client.force_login(user)
                response = client.get(self.NOTE_LIST_URL)
                object_list = response.context["object_list"]
                self.assertEqual((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        data = (
            ("notes:add", None),
            ("notes:edit", ("note-slug",)),
        )
        for name, args in data:
            with self.subTest(name=name):
                client = self.author_client
                url = reverse(name, args=args)
                response = client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
