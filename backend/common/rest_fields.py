import base64
import hashlib
import hmac
import textwrap

from rest_framework.fields import FileField, get_attribute

from config.settings import IMGPROXY_FULL_PATH, IMGPROXY_KEY, IMGPROXY_SALT, IMGPROXY_SECURE

try:
    from django.contrib.postgres import fields as postgres_fields
    from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange
except ImportError:
    postgres_fields = None
    DateRange = None
    DateTimeTZRange = None
    NumericRange = None


class MultiImageField(FileField):
    def _generate_insecure_url(self, instance, origin_attr, attr_name, img_format):
        """Генерация незащищенного URL"""
        link = getattr(instance, f"{attr_name}_default")
        try:
            return link + getattr(instance, origin_attr).url + f"@{img_format}"
        except ValueError:
            return None

    def _generate_secure_url(self, instance, origin_attr, attr_name, img_format):
        """Генерация защищенного URL"""
        # Получаем hex от ключа и соли
        key = bytes.fromhex(IMGPROXY_KEY)
        salt = bytes.fromhex(IMGPROXY_SALT)

        # Кодируем исходный файл
        origin_attr_bytes = str(getattr(instance, origin_attr).url).encode()
        encoded_url = base64.urlsafe_b64encode(origin_attr_bytes).rstrip(b"=").decode()
        encoded_url = "/".join(textwrap.wrap(encoded_url, 16))

        try:
            # Получаем конфигурацию для изображения
            config = getattr(instance, f"{attr_name}_config")
            # Формируем полный путь
            path = str(config + encoded_url + f".{img_format}").encode()
            # Шифруем с помощью ключа и соли
            digest = hmac.new(key, msg=salt + path, digestmod=hashlib.sha256).digest()
            # Преобразуем в читаемый url
            protection = base64.urlsafe_b64encode(digest).rstrip(b"=")
            url = b"/%s%s" % (
                protection,
                path,
            )

            return IMGPROXY_FULL_PATH + url.decode()
        except ValueError:
            return None

    def get_attribute(self, instance):
        request = self.context["request"]
        if not instance:
            return None
        if self.source:
            instance = get_attribute(instance, self.source_attrs[:-1])
            attr_name = self.source_attrs[-1]
        else:
            attr_name = self.source_attrs[0]

        try:
            origin_attr = instance.__class__.image_map[attr_name].source
            origin_format = getattr(instance, origin_attr).url.split(".")[-1]
        except AttributeError:
            return None

        # Для хрома меняем формат на webp иначе оставляем оригинальный
        if request.user_agent.browser.family in [
            "Safari",
            "Mobile Safari",
            "Chrome Mobile iOS",
            "Internet Explorer",
        ]:
            img_format = origin_format
        elif "Chrome" in request.user_agent.browser.family:
            img_format = "webp"
        else:
            img_format = origin_format

        if IMGPROXY_SECURE:
            return self._generate_secure_url(instance, origin_attr, attr_name, img_format)
        else:
            return self._generate_insecure_url(instance, origin_attr, attr_name, img_format)

    def to_representation(self, value):
        return value
