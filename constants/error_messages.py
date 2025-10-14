"""Константы с сообщениями об ошибках для тестов"""

class CourierErrorMessages:
    """Сообщения об ошибках для API курьеров"""
    NOT_ENOUGH_DATA_FOR_LOGIN = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    NOT_ENOUGH_DATA_FOR_CREATE = "Недостаточно данных для создания учетной записи"
    LOGIN_ALREADY_EXISTS = "Этот логин уже используется. Попробуйте другой."
    COURIER_NOT_FOUND = "Курьера с таким id нет."
    NOT_FOUND = "Not Found."

class OrderErrorMessages:
    """Сообщения об ошибках для API заказов"""
    NOT_ENOUGH_DATA_FOR_SEARCH = "Недостаточно данных для поиска"
    ORDER_NOT_FOUND = "Заказ не найден"
    COURIER_NOT_EXIST = "Курьера с таким id не существует"
    ORDER_NOT_EXIST = "Заказа с таким id не существует"
    NOT_FOUND = "Not Found."

class ResponseMessages:
    """Сообщения для проверки ответов"""
    EXPECTED_OK_TRUE = "Ожидалось 'ok': true"
    EXPECTED_TRACK_FIELD = "В ответе должно быть поле 'track'"
    EXPECTED_ID_FIELD = "В ответе должно быть поле 'id'"
    EXPECTED_ORDERS_FIELD = "В ответе должно быть поле 'orders'"