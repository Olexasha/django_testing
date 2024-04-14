from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username="Автор")


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username="Не автор")


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title="Заголовок",
        text="Текст заметки",
        date=timezone.now(),
    )
    return news


@pytest.fixture
def comment(author, news):
    comm = Comment.objects.create(
        news=news,
        author=author,
        text="Текст комментария",
    )
    return comm


@pytest.fixture
def news_url(news):
    return reverse("news:detail", args=(news.id,))


@pytest.fixture
def edit_url(comment):
    return reverse("news:edit", args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse("news:delete", args=(comment.id,))


@pytest.fixture
def form_data_comm():
    return {"text": "Текст комментария"}


@pytest.fixture
def several_news_objects():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f"Новость {index}",
            text="Просто текст.",
            date=today - timedelta(days=index),
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    yield


@pytest.fixture
def several_comments_objects(news, author):
    now = timezone.now()
    for index in range(NEWS_COUNT_ON_HOME_PAGE):
        comm = Comment.objects.create(
            news=news,
            author=author,
            text=f"Tекст {index}",
        )
        comm.created = now + timedelta(days=index)
        comm.save()
    yield
