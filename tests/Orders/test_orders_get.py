import allure
import pytest
from helpers.api_client import ApiClient

@allure.epic("Order API")
@allure.feature("Получение днных о заказах")
class TestGetOrder:
    
    @allure.title("Получение списка заказов")
    @allure.description("Тест проверяет успешное получение списка заказов через API")
    def test_get_orders_list(self):
        with allure.step("Отправить GET запрос для получения списка заказов"):
            response = ApiClient.get_request_orders()

        with allure.step("Проверить статус код ответа 200"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Получить и проверить JSON ответ"):
            data = response.json()

        with allure.step("Проверить наличие поля 'orders' в ответе"):
            assert "orders" in data, (
                f"В ответе отсутствует обязательное поле 'orders'. Ответ: {data}"
            )
        
        with allure.step("Проверить что 'orders' является списком"):
            orders_list = data["orders"]
            assert isinstance(orders_list, list), (
                f"Поле 'orders' должно быть списком, получен {type(orders_list)}"
            )


    @allure.title("Получение заказа по валидному track_id")
    @allure.description("Тест проверяет успешное получение заказа по существующему track_id")
    def test_get_order_by_track_id(self,  create_order):
        with allure.step("Получить существующий track_id заказа"):
            track_id = create_order
        
        with allure.step(f"Выполнить запрос на получение заказа по track_id: {track_id}"):
            response = ApiClient.get_request_order_by_track_id(track_id)
        
        with allure.step("Проверить статус код ответа 200"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Получить данные из ответа"):
            data = response.json()
        
        with allure.step("Проверить наличие объекта 'order' в ответе"):
            assert 'order' in data, (
                f"В ответе отсутствует объект 'order'. Ответ: {data}"
            )
        
        with allure.step("Проверить, что track_id в ответе совпадает с запрошенным"):
            order_data = data['order']
            assert order_data['track'] == track_id, (
                f"Track ID в ответе ({order_data['track']}) не совпадает с запрошенным ({track_id})"
            )

    @allure.title("Негативные кейсы: получение заказа с невалидным track_id")
    @allure.description("Тест проверяет обработку ошибок при невалидных track_id")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "test_case, track_id, expected_status, expected_error", 
        [
            ("missing_track_id", None, 400, "Недостаточно данных для поиска"),
            ("empty_track_id", "", 400, "Недостаточно данных для поиска"),
            ("nonexistent_track_id", 999999999, 404, "Заказ не найден"),
        ]
    )
    def test_get_order_with_invalid_track_id_returns_error(self, test_case, track_id, expected_status, expected_error):
        with allure.step(f"Выполнить запрос с невалидным track_id: {track_id}"):
                response = ApiClient.get_request_order_by_track_id(track_id)
            

        with allure.step(f"Проверить статус код {expected_status}"):
                assert response.status_code == expected_status, (
                    f"Ожидался статус код {expected_status}, получен {response.status_code}. "
                    f"Response: {response.text}"
                )
            
        with allure.step(f"Проверить текст ошибки: '{expected_error}'"):
                response_data = response.json()
                assert response_data["message"] == expected_error, (
                    f"Ожидалось сообщение: '{expected_error}', "
                    f"получено: '{response_data['message']}'"
                )