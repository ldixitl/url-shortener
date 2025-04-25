import random
import string


def generate_short_id(length: int = 6) -> str:
    """
    Функция для генерации случайного короткого идентификатора.

    :param length: Длина генерируемой строки.
    :return: Строка с коротким идентификатором.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
