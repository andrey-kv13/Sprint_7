from helpers.api_client import ApiClient
from helpers.common_generator import CommonGenerator

class CourierGenerator:
    
    @staticmethod
    def generate_courier_data(login=None, password=None, first_name=None):
        """Генерация данных для создания курьера"""
        return {
            "login": login or CommonGenerator.generate_random_string(10),
            "password": password or CommonGenerator.generate_random_string(10),
            "firstName": first_name or CommonGenerator.generate_random_string(10)
        }
    
    @staticmethod
    def register_new_courier():
        """Регистрация нового курьера в системе"""
        payload = CourierGenerator.generate_courier_data()
        
        response = ApiClient.post_request_create_courier(payload)
        
        if response.status_code == 201:
            return payload['login'], payload['password'], payload['firstName']
        else:
            return None, None, None
    
    @staticmethod
    def get_courier_id(login, password):
        """Получение ID курьера по логину и паролю"""
        payload = {"login": login, "password": password}
        response = ApiClient.post_request_login_courier(payload)
        
        if response.status_code == 200:
            return response.json().get("id")
        raise Exception(f"Failed to get courier ID. Status: {response.status_code}")
    
    @staticmethod
    def generate_courier_with_missing_field(missing_field):
        """Генерация данных курьера с отсутствующим полем"""
        payload = CourierGenerator.generate_courier_data()
        payload.pop(missing_field, None)
        return payload