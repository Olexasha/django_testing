from http import HTTPStatus

import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.constants import COMMENT_TEXT, NEW_COMMENT_TEXT


@pytest.mark.django_db
class TestCommentCreation:
    def test_anonymous_user_cant_create_comment(
        self, guest_client, news_url, form_data_comm
    ):
        comments_count_before = Comment.objects.count()
        guest_client.post(news_url, data=form_data_comm)
        assert Comment.objects.count() == comments_count_before

    def test_user_can_create_comment(
        self, not_author_client, news_url, form_data_comm, news, not_author
    ):
        comments_count_before = Comment.objects.count()
        response = not_author_client.post(news_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{news_url}#comments"
        assert Comment.objects.count() == comments_count_before + 1
        comm = Comment.objects.get()
        assert comm.text == COMMENT_TEXT
        assert comm.news == news
        assert comm.author == not_author

    @pytest.mark.parametrize("bad_word", BAD_WORDS)
    def test_user_cant_use_bad_words(
        self, author_client, news_url, form_data_comm, bad_word
    ):
        form_data_comm["text"] = f"Какой-то текст, {bad_word}, еще текст"
        comments_count_before = Comment.objects.count()
        response = author_client.post(news_url, data=form_data_comm)
        assert response.context["form"].errors["text"] == [WARNING]
        assert Comment.objects.count() == comments_count_before


@pytest.mark.django_db
class TestCommentEditDelete:
    def test_author_can_delete_comment(
            self, author_client, news_url, delete_url
    ):
        comments_count_before = Comment.objects.count()
        response = author_client.delete(delete_url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == news_url + "#comments"
        assert Comment.objects.count() == comments_count_before - 1

    def test_user_cant_delete_comment_of_another_user(
        self, not_author_client, delete_url
    ):
        comments_count_before = Comment.objects.count()
        response = not_author_client.delete(delete_url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert Comment.objects.count() == comments_count_before

    def test_author_can_edit_comment(
        self,
        author_client,
        edit_url,
        form_data_comm,
        news_url,
        comment,
        news,
        author,
    ):
        form_data_comm["text"] = NEW_COMMENT_TEXT
        response = author_client.post(edit_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == news_url + "#comments"
        comment.refresh_from_db()
        assert comment.text == NEW_COMMENT_TEXT
        assert comment.news == news
        assert comment.author == author

    def test_user_cant_edit_comment_of_another_user(
        self,
        not_author_client,
        edit_url,
        form_data_comm,
        comment,
        news,
        author,
    ):
        form_data_comm["text"] = NEW_COMMENT_TEXT
        response = not_author_client.post(edit_url, data=form_data_comm)
        assert response.status_code == HTTPStatus.NOT_FOUND
        comment.refresh_from_db()
        assert comment.text == COMMENT_TEXT
        assert comment.news == news
        assert comment.author == author
