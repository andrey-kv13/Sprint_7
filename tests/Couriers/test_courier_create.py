import pytest
import allure
from helpers.courier_generator import CourierGenerator
from helpers.api_client import ApiClient
from helpers.data_cleaner import DataCleaner

@allure.epic("Courier API")
@allure.feature("Создание курьера")
class TestCreateCourier:
    
    @allure.title("Успешное создание нового курьера")
    @allure.description("Тест проверяет успешное создание курьера с валидными данными")
    def test_create_new_courier_success(self):
        with allure.step("Подготовить валидные данные для создания курьера"):
            payload = CourierGenerator.generate_courier_data()
        
        with allure.step("Отправить запрос на создание курьера"):
            response = ApiClient.post_request_create_courier(payload)
        
        with allure.step("Проверить статус код ответа 201"):
            assert response.status_code == 201, (
                f"Ожидался статус код 201, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Проверить что успешный запрос возвращает {'ok': true}'"):
            response_data = response.json()
            assert response_data == {"ok": True}, (
                f"Ожидалось {{'ok': true}}, получено: {response_data}"
            )
        DataCleaner.delete_courier(payload['login'], payload['password'])
        
    @allure.title("Негативные кейсы: cоздание курьера без обязательного поля: {missing_field}")
    @allure.description("Тестирование создания курьера без обязательных полей")
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):
        """Тест проверяет статус код при отсутствии обязательного поля,
        используем MOCK, тк на сервере баг: возвращается 504 код при отсутствии поля password"""
        
        with allure.step("Подготовить данные и удалить обязательное поле"):
            payload = CourierGenerator.generate_courier_with_missing_field(missing_field)
            
        with allure.step("Отправить запрос с неполными данными"):
            response = ApiClient.post_request_create_courier(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 400, (
                f"Ожидался статус код 400, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            error_message = response_data.get("message", "")
            expected_message = "Недостаточно данных для создания учетной записи"
            assert error_message == expected_message, (
                f"Ожидалось сообщение: '{expected_message}', "
                f"получено: '{error_message}'"
            )
              
    @allure.title("Негативные кейсы: cоздание курьера с существующим логином")
    @allure.description("Тест проверяет обработку попытки создания курьера с уже существующим логином")
    def test_create_courier_with_existing_login(self, create_and_delete_courier):
        existing_login, _, _ = create_and_delete_courier
        """Используем созданного фикстурой курьера для проверки дубликата"""
        with allure.step("Попытаться создать курьера с таким же логином"):
            payload = CourierGenerator.generate_courier_data(login=existing_login)
            response = ApiClient.post_request_create_courier(payload)

        with allure.step("Проверить ошибку конфликта - статус 409"):
            assert response.status_code == 409, (
                f"Ожидался статус код 409, получен {response.status_code}"
            )
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            error_message = response_data.get("message", "")
            expected_message = "Этот логин уже используется. Попробуйте другой."
            assert error_message == expected_message, (
                f"Ожидалось сообщение: '{expected_message}', "
                f"получено: '{error_message}'"
            )