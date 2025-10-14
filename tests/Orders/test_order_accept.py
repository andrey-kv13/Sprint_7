import allure
import pytest
from helpers.courier_generator import CourierGenerator
from helpers.order_generator import OrderGenerator
from helpers.api_client import ApiClient
from constants.error_messages import OrderErrorMessages, ResponseMessages


@allure.epic("Order API")
@allure.feature("Принятие заказа курьером")
class TestOrderAccept:
    
    @allure.title("Принятие заказа курьером")
    @allure.description("Тест проверяет успешное принятие заказа курьером")
    def test_order_accept(self, create_and_delete_courier, create_order):
        
        login, password, _ = create_and_delete_courier
        track_id = create_order
        
        with allure.step("Получить ID заказа по track номеру"):
            order_id = OrderGenerator.get_order_id_by_track(track_id)

        with allure.step("Получить ID курьера"):
            courier_id = CourierGenerator.get_courier_id(login=login, password=password)
            courier_params = {"courierId": courier_id}
        
        with allure.step("Отправить запрос на принятие заказа"):
            response = ApiClient.put_request_order_accept(order_id, courier_params)
        
        with allure.step("Проверить статус код ответа 200"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Проверить что успешный запрос возвращает {'ok': true}"):
            response_data = response.json()
            assert response_data == {"ok": True}, (
                f"{ResponseMessages.EXPECTED_OK_TRUE}, получено: {response_data}"
            )
    
    @allure.title("Негативные кейсы: попытка принятия заказа с невалидным ID курьера")
    @allure.description("Тест проверяет ошибку при при несуществующем ID курьера")
    @pytest.mark.parametrize(
        "test_case, courier_id, expected_status, expected_error", 
        [
            ("missing_corier_id", None, 400, "Недостаточно данных для поиска"),
            ("empty_courier_id", "", 400, "Недостаточно данных для поиска"),
            ("nonexistent_courier_id", 999999999, 404, "Курьера с таким id не существует")
        ]
    )
    def test_order_accept_invalid_courier_id(self, test_case, courier_id, expected_status, expected_error,
                                             create_order):
        with allure.step("Получить ID заказа"):
            order_id = OrderGenerator.get_order_id_by_track(create_order)
        
        with allure.step("Получить ID курьера"):
            courier_id = {"courierId": courier_id}
        
        with allure.step("Отправить запрос на принятие заказа"):
            response = ApiClient.put_request_order_accept(order_id, courier_id)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == expected_status,(
                f"Ожидался статус код {expected_status}, получен {response.status_code}"
            )
            
        with allure.step("Проверить текст ошибки"):
            actual_error = response.json()["message"]
            assert actual_error == expected_error, f'Ожидали: {expected_error}, получили: {actual_error}'
    
    @allure.title("Негативные кейсы: попытка принятия заказа с невалидным ID курьера")
    @allure.description("Тест проверяет ошибку при несуществующем ID заказа")        
    @pytest.mark.parametrize(
        "test_case, order_id, expected_status, expected_error", 
        [
            ("empty_order", "", 404, OrderErrorMessages.NOT_FOUND),
            ("nonexistent_oder_id", 999999999, 404, OrderErrorMessages.ORDER_NOT_EXIST)
        ]
    )
        
    def test_order_accept_invalid_order_id(self, test_case, order_id, expected_status, 
                                           expected_error,create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        with allure.step("Получить ID заказа"):
            order_id = order_id
        
        with allure.step("Получить ID курьера"):
            courier_id = {"courierId": CourierGenerator.get_courier_id(login = login, password = password)}
        
        with allure.step("Отправить запрос на принятие заказа"):
            response = ApiClient.put_request_order_accept(order_id, courier_id)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == expected_status,(
                f"Ожидался статус код {expected_status}, получен {response.status_code}"
            )
            
        with allure.step("Проверка текста ошибки"):
            actual_error = response.json()["message"]
            assert actual_error == expected_error, f'Ожидали: {expected_error}, получили: {actual_error}'