from dataclasses import dataclass

from django.db import models, connection
from django.db.models.signals import pre_migrate


from config.settings import IMGPROXY_FULL_PATH, IMGPROXY_SECURE


@dataclass
class Spec:
    source: str
    width: int = 0
    height: int = 0
    blur: int = False
    default: str = "jpeg"
    crop: bool = False


class MultiImageMeta(models.base.ModelBase):
    def __new__(mcs, name, bases, dct):
        # нет карты нет обработки
        if "image_map" not in dct:
            return super().__new__(mcs, name, bases, dct)

        # инициализауия параметров
        for spec_name, spec in dct["image_map"].items():
            link = IMGPROXY_FULL_PATH
            if not IMGPROXY_SECURE:
                link += "/insecure"

            config = ""

            if spec.width and spec.height:
                config += f"/rs:auto:{spec.height}:{spec.width}/"

            if spec.blur:
                config += "blur:10/q:70/"

            dct[f"{spec_name}_config"] = config
            dct[f"{spec_name}_default"] = link + config + "plain/"

        return super().__new__(mcs, name, bases, dct)


def app_pre_migration(sender, app_config, **kwargs):

    cur = connection.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


pre_migrate.connect(app_pre_migration)
