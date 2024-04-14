from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note


class TestNoteActions(TestCase):
    NOTES_ADD_URL = reverse("notes:add")
    NOTES_SUCCESS_URL = reverse("notes:success")
    USERS_LOGIN_URL = reverse("users:login")

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
        cls.form_data = {
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": "new-slug",
        }

    def test_user_can_create_note(self):
        response = self.author_client.post(
            self.NOTES_ADD_URL, data=self.form_data
        )
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.form_data["title"])
        self.assertEqual(new_note.text, self.form_data["text"])
        self.assertEqual(new_note.slug, self.form_data["slug"])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.NOTES_ADD_URL, data=self.form_data)
        expected_url = f"{self.USERS_LOGIN_URL}?next={self.NOTES_ADD_URL}"
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 1)

    def test_not_unique_slug(self):
        self.form_data["slug"] = self.note.slug
        response = self.author_client.post(
            self.NOTES_ADD_URL, data=self.form_data
        )
        self.assertFormError(
            response, "form", "slug", errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.form_data = {"title": "Новый заголовок", "text": "Новый текст"}
        expected_slug = slugify(self.form_data["title"])
        response = self.author_client.post(
            self.NOTES_ADD_URL, data=self.form_data
        )
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.last()
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        self.form_data = {
            "title": "Измененный заголовок",
            "text": "Измененный текст",
            "slug": "edited-slug",
        }
        url = reverse("notes:edit", args=(self.note.slug,))
        response = self.author_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse("notes:success"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data["title"])
        self.assertEqual(self.note.text, self.form_data["text"])
        self.assertEqual(self.note.slug, self.form_data["slug"])

    def test_other_user_cant_edit_note(self):
        self.form_data = {
            "title": "Измененный заголовок",
            "text": "Измененный текст",
            "slug": "edited-slug",
        }
        url = reverse("notes:edit", args=(self.note.slug,))
        response = self.reader_client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        url = reverse("notes:delete", args=(self.note.slug,))
        response = self.author_client.post(url)
        self.assertRedirects(response, reverse("notes:success"))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        url = reverse("notes:delete", args=(self.note.slug,))
        response = self.reader_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
