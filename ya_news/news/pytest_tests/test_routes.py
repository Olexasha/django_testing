from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


class TestRoutes:
    User = get_user_model()

    @pytest.mark.parametrize(
        "name",
        ("news:home", "news:detail", "users:login",
         "users:logout", "users:signup"),
    )
    def test_pages_availability(self, not_author_client, name, news):
        args = None
        if name == "news:detail":
            args = (news.id,)
        url = reverse(name, args=args)
        response = not_author_client.get(url)
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("url_name", ("news:edit", "news:delete"))
    @pytest.mark.parametrize(
        "user_client, expected_status",
        (
            (lazy_fixture("author_client"), HTTPStatus.OK),
            (lazy_fixture("not_author_client"), HTTPStatus.NOT_FOUND),
        ),
    )
    def test_availability_for_comment_edit_and_delete(
        self, url_name, user_client, expected_status, comment
    ):
        url = reverse(url_name, args=(comment.id,))
        response = user_client.get(url)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("url_name", ("news:edit", "news:delete"))
    def test_redirect_for_anonymous_client(self, client, url_name, comment):
        login_url = reverse("users:login")
        url = reverse(url_name, args=(comment.id,))
        redirect_url = f"{login_url}?next={url}"
        response = client.get(url)
        assertRedirects(response, redirect_url)
