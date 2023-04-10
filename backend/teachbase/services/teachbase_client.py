import json
from typing import Any

import requests
from requests import Response
from django.conf import settings
from requests.auth import HTTPBasicAuth


class RequestMethods:
    """
    HTTP методы

    """

    get = "GET"
    post = "POST"
    patch = "PATCH"


class TechbasePaths:
    """
    paths для клиента

    """

    token_url = "oauth/token"
    check_access_token = "oauth/token/check"
    courses = "courses"
    users_create = "users/create"
    course_sessions = "course_sessions"


class TeachbaseClient:
    """
    Клиент для работы с API Techbase

    """

    base_url = settings.TEACHBASE_API_URL
    client_id = settings.TEACHBASE_CLIENT_ID
    client_secret = settings.TEACHBASE_CLIENT_SECRET

    def __init__(self):
        # self.access_token = self.get_access_token()
        self.headers = None

    def _request(
        self, url: str, method: str, params: dict, data: dict, headers: dict, auth: HTTPBasicAuth
    ) -> Response:
        """
        Метод для звпросов

        :param url:
        :param method:
        :param params:
        :param data:
        :param headers:
        :param auth:
        :return:
        """
        if not data:
            response = requests.request(
                method, url, params=params, data=data, headers=headers, auth=auth
            )
        else:
            response = requests.request(
                method, url, params=params, json=data, headers=headers, auth=auth
            )
        return response

    def api_request(
        self,
        path: str,
        method: str,
        params: Any = None,
        data: Any = None,
        headers: Any = None,
        auth: Any = None,
    ) -> Response:
        """
        Метод для общих API запросов

        :param path:
        :param method:
        :param params:
        :param data:
        :param headers:
        :param auth:
        :return:
        """
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        if auth is None:
            auth = None
        url = self.get_url(path)
        response = self._request(
            url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
        )
        return response

    def get_url(self, path):
        """
        Получение полного URL запроса

        :param path:
        :return:
        """
        return "{}/{}".format(self.base_url, path)

    def get_access_token(self) -> str:
        """
        Получение токена

        :return:
        """
        payload = {
            "grant_type": "client_credentials",
        }
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        response = self.api_request(
            path=TechbasePaths.token_url, method=RequestMethods.post, auth=auth, data=payload
        )

        if response.status_code != 200:
            raise Exception("Failed to get access token from Teachbase")

        response_data = response.json()
        return response_data.get("access_token")

    def _get_headers(self) -> dict:
        """
        Получение заголовка авторизации

        :return:
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def is_access_token_valid(self):
        """
        Проверка валидности токена

        :return:
        """
        response = self.api_request(
            path=TechbasePaths.check_access_token,
            method=RequestMethods.post,
            headers=self._get_headers(),
        )
        return response.status_code == 200

    def get_courses(self) -> list | None:
        """
        Получение курсов

        :return:
        """
        response = self.api_request(
            path=TechbasePaths.courses, method=RequestMethods.get, headers=self._get_headers()
        )
        if response.status_code != 200:
            raise Exception("Failed to get courses from Teachbase")

        return response.json()

    def get_course_detail(self, course_id: int) -> dict | None:
        """
        Получение детального представления курса

        :param course_id:
        :return:
        """
        path = f"{TechbasePaths.courses}/{course_id}"
        response = self.api_request(
            path=path, method=RequestMethods.get, headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception("Failed to get course detail from Teachbase")

        return response.json()

    def create_user(self, user_data: dict) -> dict | None:
        """
        Создание пользователя

        :param user_data:
        :return:
        """
        response = self.api_request(
            path=TechbasePaths.users_create,
            method=RequestMethods.post,
            data=user_data,
            headers=self._get_headers(),
        )
        if response.status_code != 200:
            raise Exception("Failed to create user from Teachbase")

        return response.json()

    def register_user_in_course_session(self, session_id: int, user_data: dict):
        """
        Запись пользователя на сессию

        :param session_id:
        :param user_data:
        :return:
        """
        path = f"{TechbasePaths.course_sessions}/{session_id}/register"
        response = self.api_request(
            path=path, method=RequestMethods.post, data=user_data, headers=self._get_headers()
        )
        if response.status_code != 200:
            raise Exception("Failed to register user in course session  from Teachbase")

        return response.json()

    def get_course_sessions_list(self, course_id) -> dict | None:
        """
        Получение сессии курсов

        :param course_id:
        :return:
        """
        path = f"{TechbasePaths.courses}/{course_id}/course_sessions"
        response = self.api_request(
            path=path, method=RequestMethods.get, headers=self._get_headers()
        )
        if response.status_code != 200:
            raise Exception("Failed to get courses sessions from Teachbase")

        return response.json()
