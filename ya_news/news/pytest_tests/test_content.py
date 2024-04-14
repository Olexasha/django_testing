import pytest
from django.test import Client
from django.urls import reverse

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


class TestContent:
    HOME_URL = reverse("news:home")

    def test_news_count(self, not_author_client, several_news_objects):
        response = not_author_client.get(self.HOME_URL)
        object_list = response.context["object_list"]
        news_count = object_list.count()
        assert news_count == NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, not_author_client, several_news_objects):
        response = not_author_client.get(self.HOME_URL)
        object_list = response.context["object_list"]
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        assert all_dates == sorted_dates


class TestDetailPage:
    @pytest.mark.django_db(transaction=True)
    def test_comments_order(
            self, several_comments_objects, not_author_client, news_url
    ):
        response = not_author_client.get(news_url)
        assert "news" in response.context
        news_got = response.context["news"]
        all_comments = news_got.comment_set.all()
        all_timestamps = [comm.created for comm in all_comments]
        sorted_timestamps = sorted(all_timestamps)
        assert all_timestamps == sorted_timestamps

    def test_anonymous_client_has_no_form(self, not_author_client, news_url):
        response = Client().get(news_url)
        assert "form" not in response.context

    def test_authorized_client_has_form(self, author_client, news_url):
        response = author_client.get(news_url)
        assert "form" in response.context
        assert isinstance(response.context["form"], CommentForm)
