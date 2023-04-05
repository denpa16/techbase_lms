import ast
import ipaddress
import logging
import traceback

from django.db import connection
from django.utils.timezone import now

from .models import APIRequestLog

logger = logging.getLogger(__name__)


class BaseLoggingMixin(object):
    """
    Миксин для логирования запросов
    """

    CLEANED_SUBSTITUTE = "********************"

    logging_methods = "__all__"
    sensitive_fields = {}

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), "CLEANED_SUBSTITUTE должен быть строкой."
        super(BaseLoggingMixin, self).__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self.log = {"requested_at": now(), "data": self._clean_data(request.body)}

        super(BaseLoggingMixin, self).initial(request, *args, **kwargs)

        try:
            # Accessing request.data *for the first time* parses the request body, which may raise
            # ParseError and UnsupportedMediaType exceptions. It's important not to swallow these,
            # as (depending on implementation details) they may only get raised this once, and
            # DRF logic needs them to be raised by the view for error handling to work correctly.
            data = self.request.data.dict()
        except AttributeError:
            data = self.request.data
        self.log["data"] = self._clean_data(data)

    def handle_exception(self, exc):
        response = super(BaseLoggingMixin, self).handle_exception(exc)
        self.log["errors"] = traceback.format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(BaseLoggingMixin, self).finalize_response(
            request, response, *args, **kwargs
        )

        if self.should_log(request, response):
            if (
                connection.settings_dict.get("ATOMIC_REQUESTS")
                and getattr(response, "exception", None)
                and connection.in_atomic_block
            ):
                # response with exception (HTTP status like: 401, 404, etc)
                # pointwise disable atomic block for handle log (TransactionManagementError)
                connection.set_rollback(True)
                connection.set_rollback(False)
            if response.streaming:
                rendered_content = None
            elif hasattr(response, "rendered_content"):
                rendered_content = response.rendered_content
            else:
                rendered_content = response.getvalue()

            user = self._get_user(request)

            self.log.update(
                {
                    "remote_addr": self._get_ip_address(request),
                    "view": self._get_view_name(request),
                    "view_method": self._get_view_method(request),
                    "path": self._get_path(request),
                    "host": request.get_host(),
                    "method": request.method,
                    "query_params": self._clean_data(request.query_params.dict()),
                    "user": user,
                    "username_persistent": user.get_username() if user else "Anonymous",
                    "response_ms": self._get_response_ms(),
                    "response": self._clean_data(rendered_content),
                    "status_code": response.status_code,
                }
            )
            if self._clean_data(request.query_params.dict()) == {}:
                self.log.update({"query_params": self.log["data"]})
            try:
                self.handle_log()
            except Exception:
                # ensure that all exceptions raised by handle_log
                # doesn't prevent API call to continue as expected
                logger.exception("Ошибка DRF logging API!")
        return response

    def handle_log(self):
        """
        Хук для действия с логируемыми данными.
        """
        raise NotImplementedError

    def _get_path(self, request):
        """Возвращает path запроса"""
        return request.path

    def _get_ip_address(self, request):
        """Возвращает IP адрес источника запроса из хедера HTTP_X_FORWARDED_FOR."""
        ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddr:
            ipaddr = ipaddr.split(",")[0]
        else:
            ipaddr = request.META.get("REMOTE_ADDR", "").split(",")[0]

        # Account for IPv4 and IPv6 addresses, each possibly with port appended. Possibilities are:
        # <ipv4 address>
        # <ipv6 address>
        # <ipv4 address>:port
        # [<ipv6 address>]:port
        # Note that ipv6 addresses are colon separated hex numbers
        possibles = (ipaddr.lstrip("[").split("]")[0], ipaddr.split(":")[0])

        for addr in possibles:
            try:
                return str(ipaddress.ip_address(addr))
            except ValueError:
                pass

        return ipaddr

    def _get_view_name(self, request):
        """Возвращает имя view."""
        method = request.method.lower()
        try:
            attributes = getattr(self, method)
            return type(attributes.__self__).__module__ + "." + type(attributes.__self__).__name__

        except AttributeError:
            return None

    def _get_view_method(self, request):
        """Возвращает метод view."""
        if hasattr(self, "action"):
            return self.action or None
        return request.method.lower()

    def _get_user(self, request):
        """Возвращает пользователя."""
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def _get_response_ms(self):
        """
        Возвращает длительность обработки запроса в миллисекундах.
        В случае отрицательного значения возвращает 0.
        """
        response_timedelta = now() - self.log["requested_at"]
        response_ms = int(response_timedelta.total_seconds() * 1000)
        return max(response_ms, 0)

    def should_log(self, request, response):
        """
        Метод возвращает True если запрос должен быть залогирован.

        По умолчанию логирует все методы запроса в logging_methods.
        """
        return self.logging_methods == "__all__" or request.method in self.logging_methods

    def _clean_data(self, data):
        """
        Чистит словарь данных от потенциально конфиденциальной информации до отправки в базу.
        Функция основывается на "_clean_credentials"
        (https://github.com/django/django/blob/stable/1.11.x/django/contrib/auth/__init__.py#L50)
        Поля, определенные django, по умолчанию очищаются с помощью этой функции.
        Вы можете определить свои собственные чувствительные поля в своем view, определив set.
        например: sensitive_fields = {'field1', 'field2'}
        """
        if isinstance(data, bytes):
            data = data.decode(errors="replace")

        if isinstance(data, list):
            return [self._clean_data(d) for d in data]

        if isinstance(data, dict):
            SENSITIVE_FIELDS = {"api", "token", "key", "secret", "password", "signature"}

            data = dict(data)
            if self.sensitive_fields:
                SENSITIVE_FIELDS = SENSITIVE_FIELDS | {
                    field.lower() for field in self.sensitive_fields
                }

            for key, value in data.items():
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
                if isinstance(value, (list, dict)):
                    data[key] = self._clean_data(value)
                if key.lower() in SENSITIVE_FIELDS:
                    data[key] = self.CLEANED_SUBSTITUTE
        return data


class LoggingMixin(BaseLoggingMixin):
    def handle_log(self):
        """
        Хук для действия с логируемыми данными.
        По умолчанию сохраняет объект лога в базу данных.
        """
        APIRequestLog(**self.log).save()


class LoggingErrorsMixin(LoggingMixin):
    """
    Метод возвращает True если запрос должен быть залогирован.

    Логирует только ошибки.
    """

    def should_log(self, request, response):
        return response.status_code >= 400
