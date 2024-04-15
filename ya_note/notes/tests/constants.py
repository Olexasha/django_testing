from django.urls import reverse

# данные
AUTHOR_USERNAME = "Автор"
READER_USERNAME = "Не автор"

NOTE_TITLE = "Заголовок"
NOTE_TEXT = "Текст заметки"
NOTE_SLUG = "note-slug"

NOTE_TITLE_NEW = "Новый заголовок"
NOTE_TEXT_NEW = "Новый текст"
NOTE_SLUG_NEW = "new-slug"

# url'ы
NOTES_HOME = "notes:home"
NOTES_LIST = "notes:list"
NOTES_ADD = "notes:add"
NOTES_DETAIL = "notes:detail"
NOTES_EDIT = "notes:edit"
NOTES_DELETE = "notes:delete"
NOTES_SUCCESS = "notes:success"
USERS_LOGIN = "users:login"
USERS_LOGOUT = "users:logout"
USERS_SIGNUP = "users:signup"

NOTES_HOME_URL = reverse(NOTES_HOME)
NOTES_LIST_URL = reverse(NOTES_LIST)
NOTES_ADD_URL = reverse(NOTES_ADD)
NOTES_DETAIL_URL = reverse(NOTES_DETAIL, args=(NOTE_SLUG,))
NOTES_EDIT_URL = reverse(NOTES_EDIT, args=(NOTE_SLUG,))
NOTES_DELETE_URL = reverse(NOTES_DELETE, args=(NOTE_SLUG,))
NOTES_SUCCESS_URL = reverse(NOTES_SUCCESS)
USERS_LOGIN_URL = reverse(USERS_LOGIN)
USERS_LOGOUT_URL = reverse(USERS_LOGOUT)
USERS_SIGNUP_URL = reverse(USERS_SIGNUP)
