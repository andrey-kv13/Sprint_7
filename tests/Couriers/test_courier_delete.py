import pytest
import allure
from helpers.courier_generator import CourierGenerator
from helpers.api_client import ApiClient
from constants.error_messages import CourierErrorMessages, ResponseMessages

@allure.epic("Courier API")
@allure.feature("Удаление курьера")
class TestDeleteCourier:
    
    @allure.title("Успешное удаление курьера")
    @allure.description("Тест проверяет успешное удаление курьера с существующим id")
    def test_delete_courier(self):
        with allure.step("Получить данные курьера для удаления"):
            login, password, _ = CourierGenerator.register_new_courier()
        with allure.step("Получить ID курьера для удаления"):
            courier_id = CourierGenerator.get_courier_id(login, password)
        with allure.step(f"Отправить DELETE запрос для курьера с ID: {courier_id}"):
            response = ApiClient.delete_request_courier(courier_id)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Проверить поле 'ok' в ответе"):
            response_data = response.json()
            assert response_data == {"ok": True}, (
                f"{ResponseMessages.EXPECTED_OK_TRUE}, получено: {response_data}"
            )
    
    
    @allure.title("Негативные кейсы: удаление с невалидным ID")
    @allure.description("Проверка корректной обработки ошибок, при передаче некорректных идентификаторов курьера в запросе")
    @pytest.mark.parametrize('test_case, courier_id, expected_status, expected_error', [
        
        ('несуществующий id', '12345', 404, CourierErrorMessages.COURIER_NOT_FOUND),
        ('пустая строка', "", 404, CourierErrorMessages.NOT_FOUND)
    ])
    def test_delete_courier_invalid_id(self, test_case, courier_id, expected_status, expected_error ):
        with allure.step(f"Отправить запрос на удаление курьера с ID: '{courier_id}'"):
            response = ApiClient.delete_request_courier(courier_id)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404, (
                f"Ожидался статус код 404, получен {response.status_code}"
            )
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            error_message = response_data.get("message", "")
            assert error_message == expected_error, (
                f"Ожидалось сообщение: {expected_error},"
                f"получено: '{error_message}'"
            )
            
    @allure.title("Удаление курьера и проверка целостности данных")
    @allure.description("Тест проверяет, что после удаления курьера его данные действительно удаляются из системы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_courier_data_integrity(self):
        #Создаем нового курьера
        login, password, first_name = CourierGenerator.register_new_courier()
        assert login is not None, "Не удалось создать курьера для теста"
        
        courier_id = CourierGenerator.get_courier_id(login=login, password=password)
        
        #Удаляем курьера
        with allure.step("Удалить курьера"):
            delete_response = ApiClient.delete_request_courier(courier_id)
            assert delete_response.status_code == 200, "Удаление должно быть успешным"
        
        #Проверяем, что данные действительно удалены
        with allure.step("Проверить, что логин больше не работает"):
            login_response = ApiClient.post_request_login_courier({
                "login": login, 
                "password": password
            })
            assert login_response.status_code == 404, (
                "После удаления курьера не должна проходить авторизация"
            )
        
        with allure.step("Проверить, что ID больше не существует"):
            second_delete_response = ApiClient.delete_request_courier(courier_id)
            assert second_delete_response.status_code == 404, (
                "После удаления курьера его ID не должен существовать в системе"
            )        