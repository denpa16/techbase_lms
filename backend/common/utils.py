import functools
import math
from random import sample


def floor(number, digits=0):
    if number is None:
        return None
    n = 10**-digits
    return round(math.floor(number / n) * n, digits)


def ceil(number, digits=0):
    if number is None:
        return None
    n = 10**-digits
    return round(math.ceil(number / n) * n, digits)


def rgetattr(obj, attr, *args):
    # noinspection PyShadowingNames
    def _getattr(obj, attr):
        if obj:
            return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def generate_code(length: int = 4) -> str:
    """Возвращает строку из n случайных чисел"""
    return "".join([str(x) for x in sample(range(10), length)])


@functools.lru_cache
def get_russian_month(
    month: int, slice_stop: int = None, title: bool = False, case: bool = False
) -> str:
    month_dict = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    }
    month = month_dict.get(month)[:slice_stop]
    if title:
        month = month.title()
    if case:
        if month[-1] in ["ь", "й"]:
            month = month.replace(month[-1], "я")
        else:
            month = month + "a"

    return month
