import allure
import pytest
from helpers.courier_generator import CourierGenerator
from helpers.api_client import ApiClient

@allure.epic("Courier API")
@allure.feature("Логин курьера")
class TestCourierLogin:
    
    @allure.title("Успешная авторизация курьера")
    @allure.description("Тест проверяет успешный логин курьера с валидными данными")
    def test_successful_login(self, create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        with allure.step("Подготовить данные для логина"):            
            payload =  CourierGenerator.generate_courier_data(login=login, password=password)

        with allure.step("Отправить запрос на авторизацию"):
            response = ApiClient.post_request_login_courier(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
        
        with allure.step("Проверить наличие поля 'id' в ответе"):
            response_json = response.json()
            assert "id" in response_json, f"В ответе отсутствует обязательное поле id. Ответ: {response_json}"
    
        with allure.step("Проверить что поле 'id' не пустое"):
            assert response_json["id"] is not None, f"Поле 'id' имеет значение None. Ответ: {response_json}"
    
    @allure.title("Негативные кейсы: логин курьера без обязательного поля: {missing_field}")
    @allure.description("Ошибка при логине с отсутствием обязательного поля")  
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_courier_login_wo_required_fields(self, missing_field, mock_password_bug):
        with allure.step("Подготовить данные для создания курьера"):
            payload = CourierGenerator.generate_courier_data()
                    
        with allure.step(f"Удалить обязательное поле: {missing_field}"):
            payload.pop(missing_field)
    
        with allure.step('Отправить запрос login без обязательных полей'):
            response = ApiClient.post_request_login_courier(payload)
    
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 400, (
                f"Ожидался статус код 400, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Проверить сообщение об ошибке"):
            error_message = response.json()["message"]
            expected_message = 'Недостаточно данных для входа'
            assert error_message == expected_message, (
                f"Сообщение об ошибке '{error_message}' не соответствует ожидаемому '{expected_message}'"
            )
    
    @allure.title("Негативные кейсы: логин незарегистрированного курьера")
    @allure.description("Проверка получения ошибки при логине незарегистрированным курьером")
    def test_login_unregistered_courier(self):
        with allure.step("Подготовить данные незарегистрированного курьера"):
            payload =  CourierGenerator.generate_courier_data()
            
        with allure.step("Отправить запрос на авторизацию"):
            response = ApiClient.post_request_login_courier(payload)
            
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            error_message = response.json()["message"]
            expected_message = 'Учетная запись не найдена'
            assert error_message == expected_message, (
                f"Сообщение об ошибке '{error_message}' не соответствует ожидаемому '{expected_message}'"
            )
    
    @allure.title("Негативные кейсы: авторизация с неверным паролем")
    @allure.description("Тест проверяет ошибку при вводе неверного пароля")
    def test_login_incorrect_password(self, create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        with allure.step("Создать курьера в системе"):
            payload =  CourierGenerator.generate_courier_data(login = login)
        
        with allure.step("Отправить запрос на авторизацию"):
            response = ApiClient.post_request_login_courier(payload)

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"

        with allure.step("Проверить сообщение об ошибке"):
            error_message = response.json()["message"]
            expected_message = 'Учетная запись не найдена'
            assert error_message == expected_message, (
                f"Сообщение об ошибке '{error_message}' не соответствует ожидаемому '{expected_message}'"
            )