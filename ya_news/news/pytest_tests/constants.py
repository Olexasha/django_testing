from django.urls import reverse

# данные
AUTHOR_USERNAME = "Автор"
NOT_AUTHOR_USERNAME = "Не автор"

NEWS_TITLE = "Заголовок"
NEWS_TEXT = "Текст заметки"

NEWS_TITLE_NEW = "Новый заголовок"
NEWS_TEXT_NEW = "Новый текст"

COMMENT_TEXT = "Текст комментария"
NEW_COMMENT_TEXT = "Обновлённый комментарий"

# url'ы
NEWS_HOME = "news:home"
NEWS_DETAIL = "news:detail"
NEWS_EDIT = "news:edit"
NEWS_DELETE = "news:delete"
USERS_LOGIN = "users:login"
USERS_LOGOUT = "users:logout"
USERS_SIGNUP = "users:signup"

NEWS_HOME_URL = reverse(NEWS_HOME)
USERS_LOGIN_URL = reverse(USERS_LOGIN)
USERS_LOGOUT_URL = reverse(USERS_LOGOUT)
USERS_SIGNUP_URL = reverse(USERS_SIGNUP)
