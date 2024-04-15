from http import HTTPStatus

from django.test import TestCase
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants import (
    NOTE_SLUG_NEW,
    NOTE_TEXT_NEW,
    NOTE_TITLE_NEW,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    USERS_LOGIN_URL,
)
from notes.tests.fixtures import setup_common_fixtures


class TestNoteActions(TestCase):
    @classmethod
    def setUpTestData(cls):
        common_fixtures = setup_common_fixtures()
        cls.author = common_fixtures["author"]
        cls.reader = common_fixtures["reader"]
        cls.note = common_fixtures["note"]
        cls.author_client = common_fixtures["author_client"]
        cls.reader_client = common_fixtures["reader_client"]
        cls.notes_edit_url = common_fixtures["notes_edit_url"]
        cls.notes_delete_url = common_fixtures["notes_delete_url"]
        cls.new_form_data = {
            "title": NOTE_TITLE_NEW,
            "text": NOTE_TEXT_NEW,
            "slug": NOTE_SLUG_NEW,
        }

    def test_user_can_create_note(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.post(
            NOTES_ADD_URL, data=self.new_form_data
        )
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(notes_count_before + 1, Note.objects.count())
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.new_form_data["title"])
        self.assertEqual(new_note.text, self.new_form_data["text"])
        self.assertEqual(new_note.slug, self.new_form_data["slug"])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        response = self.client.post(NOTES_ADD_URL, data=self.new_form_data)
        expected_url = f"{USERS_LOGIN_URL}?next={NOTES_ADD_URL}"
        self.assertRedirects(response, expected_url)
        self.assertEqual(notes_count_before, Note.objects.count())

    def test_not_unique_slug(self):
        self.new_form_data["slug"] = self.note.slug
        response = self.author_client.post(
            NOTES_ADD_URL, data=self.new_form_data
        )
        self.assertFormError(
            response, "form", "slug", errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.new_form_data.pop("slug")
        expected_slug = slugify(self.new_form_data["title"])
        response = self.author_client.post(
            NOTES_ADD_URL, data=self.new_form_data
        )
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.last()
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.notes_edit_url, data=self.new_form_data
        )
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.new_form_data["title"])
        self.assertEqual(self.note.text, self.new_form_data["text"])
        self.assertEqual(self.note.slug, self.new_form_data["slug"])

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(
            self.notes_edit_url, data=self.new_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.notes_delete_url)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.reader_client.post(self.notes_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
