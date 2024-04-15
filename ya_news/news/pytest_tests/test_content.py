import pytest

from news.forms import CommentForm
from news.pytest_tests.constants import NEWS_HOME_URL
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
class TestContent:
    def test_news_count(self, guest_client, several_news_objects):
        response = guest_client.get(NEWS_HOME_URL)
        object_list = response.context["object_list"]
        news_count = object_list.count()
        assert news_count == NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, guest_client, several_news_objects):
        response = guest_client.get(NEWS_HOME_URL)
        object_list = response.context["object_list"]
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        assert all_dates == sorted_dates


@pytest.mark.django_db
class TestDetailPage:
    def test_comments_order(
            self, several_comments_objects, guest_client, news_url
    ):
        response = guest_client.get(news_url)
        assert "news" in response.context
        news_got = response.context["news"]
        all_comments = news_got.comment_set.all()
        all_timestamps = [comm.created for comm in all_comments]
        sorted_timestamps = sorted(all_timestamps)
        assert all_timestamps == sorted_timestamps

    def test_anonymous_client_has_no_form(self, guest_client, news_url):
        response = guest_client.get(news_url)
        assert "form" not in response.context

    def test_authorized_client_has_form(self, author_client, news_url):
        response = author_client.get(news_url)
        assert "form" in response.context
        assert isinstance(response.context["form"], CommentForm)
