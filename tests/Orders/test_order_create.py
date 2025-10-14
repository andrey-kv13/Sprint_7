import pytest
import allure
from helpers.order_generator import OrderGenerator
from helpers.api_client import ApiClient


@allure.epic("Order API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с разными цветами: {color}")
    @allure.description("Тест проверяет создание заказа с различными комбинациями цветов самоката")
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"], 
        ["BLACK", "GREY"],
        []
    ])
    def test_order_create_with_different_colors(self, color):
        with allure.step("Подготовить данные заказа"):
            payload = OrderGenerator.generate_order_data(color=color) 
                    
        with allure.step("Отправить запрос на создание заказа"):
            response = ApiClient.post_request_order_create(payload)
        
        with allure.step("Проверить статус код ответа 201"):
            assert response.status_code == 201, (
                f"Ожидался статус код 201, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        
        with allure.step("Проверить наличие параметра track в теле ответа"):
            response_data = response.json()
            assert "track" in response_data, (
                f"В ответе отсутствует поле 'track'. Ответ: {response_data}"
            )
        
        with allure.step("Проверить что параметр track не пустой"):
            track_number = response_data["track"]
            assert track_number is not None, "Поле 'track' не должно быть пустым"
            assert isinstance(track_number, int), f"Track должен быть числом, получен {type(track_number)}"
            assert track_number > 0, f"Track должен быть положительным числом, получен {track_number}"
                
    @allure.title("Создание заказа без дополнительных полей")
    @allure.description("Тест проверяет создание заказа без необязательных полей: comment и color")
    def test_order_create_wo_additional_fields(self):
        with allure.step("Подготовить минимальный набор данных заказа"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06"
            }
            
        with allure.step("Отправить запрос на создание заказа"):
            response = ApiClient.post_request_order_create(payload)

        with allure.step("Проверить статус код ответа 201"):
            assert response.status_code == 201, (
                f"Ожидался статус код 201, получен {response.status_code}"
            )
        
        with allure.step("Проверить наличие параметра track в теле ответа"):
            response_data = response.json()
            assert "track" in response_data, "В ответе отсутствует поле 'track'"
        
        with allure.step("Проверить что параметр track не пустой"):
            track_number = response_data["track"]
            assert track_number is not None, "Поле 'track' не должно быть пустым"