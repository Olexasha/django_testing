from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

from news.pytest_tests.constants import (
    NEWS_HOME_URL,
    USERS_LOGIN_URL,
    USERS_LOGOUT_URL,
    USERS_SIGNUP_URL,
)


@pytest.mark.django_db
class TestRoutes:
    User = get_user_model()

    @pytest.mark.parametrize(
        "url",
        (
            NEWS_HOME_URL,
            lazy_fixture("news_url"),
            USERS_LOGIN_URL,
            USERS_LOGOUT_URL,
            USERS_SIGNUP_URL,
        ),
    )
    def test_pages_availability(self, guest_client, url):
        response = guest_client.get(url)
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize(
        "url", (lazy_fixture("edit_url"), lazy_fixture("delete_url"))
    )
    @pytest.mark.parametrize(
        "user_client, expected_status",
        (
            (lazy_fixture("author_client"), HTTPStatus.OK),
            (lazy_fixture("not_author_client"), HTTPStatus.NOT_FOUND),
        ),
    )
    def test_availability_for_comment_edit_and_delete(
        self, url, user_client, expected_status
    ):
        response = user_client.get(url)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "url", (lazy_fixture("edit_url"), lazy_fixture("delete_url"))
    )
    def test_redirect_for_anonymous_client(self, guest_client, url):
        redirect_url = f"{USERS_LOGIN_URL}?next={url}"
        response = guest_client.get(url)
        assertRedirects(response, redirect_url)
