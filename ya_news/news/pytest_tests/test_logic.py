from http import HTTPStatus

import pytest
from django.test import Client

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
class TestCommentCreation:
    COMMENT_TEXT = "Текст комментария"

    def test_anonymous_user_cant_create_comment(
            self, news_url, form_data_comm
    ):
        Client().post(news_url, data=form_data_comm)
        comments_count = Comment.objects.count()
        assert comments_count == 0

    def test_user_can_create_comment(
        self, not_author_client, news_url, form_data_comm, news, not_author
    ):
        response = not_author_client.post(news_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{news_url}#comments"
        comments_count = Comment.objects.count()
        assert comments_count == 1
        comm = Comment.objects.get()
        assert comm.text == self.COMMENT_TEXT
        assert comm.news == news
        assert comm.author == not_author

    def test_user_cant_use_bad_words(self, not_author_client, news_url):
        bad_words_data = {"text": f"Какой-то текст, {BAD_WORDS[0]}, еще текст"}
        response = not_author_client.post(news_url, data=bad_words_data)
        assert response.context["form"].errors["text"] == [WARNING]
        comments_count = Comment.objects.count()
        assert comments_count == 0


@pytest.mark.django_db
class TestCommentEditDelete:
    COMMENT_TEXT = "Текст комментария"
    NEW_COMMENT_TEXT = "Обновлённый комментарий"

    def test_author_can_delete_comment(
            self, author_client, news_url, delete_url
    ):
        response = author_client.delete(delete_url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == news_url + "#comments"
        comments_count = Comment.objects.count()
        assert comments_count == 0

    def test_user_cant_delete_comment_of_another_user(
        self, not_author_client, delete_url
    ):
        response = not_author_client.delete(delete_url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        comments_count = Comment.objects.count()
        assert comments_count == 1

    def test_author_can_edit_comment(
        self, author_client, edit_url, form_data_comm, news_url, comment
    ):
        form_data_comm["text"] = self.NEW_COMMENT_TEXT
        response = author_client.post(edit_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == news_url + "#comments"
        comment.refresh_from_db()
        assert comment.text == self.NEW_COMMENT_TEXT

    def test_user_cant_edit_comment_of_another_user(
        self, not_author_client, edit_url, form_data_comm, comment
    ):
        form_data_comm["text"] = self.NEW_COMMENT_TEXT
        response = not_author_client.post(edit_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.NOT_FOUND
        comment.refresh_from_db()
        assert comment.text == self.COMMENT_TEXT
