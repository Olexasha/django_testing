from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from notes.models import Note
from notes.tests.constants import (
    AUTHOR_USERNAME,
    NOTE_SLUG,
    NOTE_TEXT,
    NOTE_TITLE,
    NOTES_DELETE,
    NOTES_DETAIL,
    NOTES_EDIT,
    READER_USERNAME,
)

User = get_user_model()


def setup_common_fixtures():
    author = User.objects.create(username=AUTHOR_USERNAME)
    reader = User.objects.create(username=READER_USERNAME)
    note = Note.objects.create(
        title=NOTE_TITLE,
        text=NOTE_TEXT,
        slug=NOTE_SLUG,
        author=author,
    )
    author_client = Client()
    author_client.force_login(author)
    reader_client = Client()
    reader_client.force_login(reader)
    notes_detail_url = reverse(NOTES_DETAIL, args=(note.slug,))
    notes_edit_url = reverse(NOTES_EDIT, args=(note.slug,))
    notes_delete_url = reverse(NOTES_DELETE, args=(note.slug,))

    return {
        "author": author,
        "reader": reader,
        "note": note,
        "author_client": author_client,
        "reader_client": reader_client,
        "notes_detail_url": notes_detail_url,
        "notes_edit_url": notes_edit_url,
        "notes_delete_url": notes_delete_url,
    }
