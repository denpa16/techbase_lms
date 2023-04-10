import json
import os.path
from typing import Any


class TeachbaseClientMock:
    """
    Mock-клиент для запросов к Teachbase
    """

    FIXTUTES_PATH = "teachbase/tests/fixtures"

    def get_course(self) -> list[dict]:
        """
        Фикстура курса
        """

        file_path = self.get_fixture_file_path("course")
        return self.get_json_file_data(file_path)

    def get_json_file_data(self, file_path: str) -> list[dict[str, Any]]:
        """
        Загрузка содержимого json файла
        """

        with open(os.path.join(self.FIXTUTES_PATH, file_path), "r") as fp:
            return json.load(fp)

    @staticmethod
    def get_fixture_file_path(entity_name: str) -> str:
        """
        Метод, формирующий путь до фикстуры
        """

        return f"{entity_name}.json"
