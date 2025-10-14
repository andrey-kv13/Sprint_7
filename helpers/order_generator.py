from helpers.api_client import ApiClient
from helpers.common_generator import CommonGenerator

class OrderGenerator:
    
    @staticmethod
    def generate_order_data(color=None, **kwargs):
        """Генерация данных для создания заказа"""
        base_payload = {
            "firstName": kwargs.get('firstName', 'Naruto'),
            "lastName": kwargs.get('lastName', 'Uchiha'),
            "address": kwargs.get('address', 'Konoha, 142 apt.'),
            "metroStation": kwargs.get('metroStation', 4),
            "phone": kwargs.get('phone', CommonGenerator.generate_random_phone()),
            "deliveryDate": kwargs.get('deliveryDate', CommonGenerator.generate_random_date()),
            "comment": kwargs.get('comment', 'Saske, come back to Konoha'),
            "color": color or []
        }
        return base_payload
    
    @staticmethod
    def create_order(color=None, **kwargs):
        """Создание заказа и возврат track_id"""
        payload = OrderGenerator.generate_order_data(color, **kwargs)
        response = ApiClient.post_request_order_create(payload)
        
        if response.status_code == 201:
            track = response.json().get("track")
            if track is not None:
                return track
            else:
                raise ValueError("Track ID not found in response")
        else:
            error_msg = response.json().get("message", "Unknown error")
            raise Exception(f"Failed to create order. Status: {response.status_code}, Error: {error_msg}")
    
    @staticmethod
    def get_order_id_by_track(track_id):
        """Получение order_id по track_id"""
        if not track_id:
            raise ValueError("Track ID cannot be empty")
            
        response = ApiClient.get_request_order_by_track_id(track_id)
        if response.status_code == 200:
            order_data = response.json().get("order", {})
            order_id = order_data.get("id")
            if order_id:
                return order_id
            else:
                raise ValueError("Order ID not found in response")
        else:
            error_msg = response.json().get("message", "Unknown error")
            raise Exception(f"Failed to get order ID. Status: {response.status_code}, Error: {error_msg}")
    
    @staticmethod
    def generate_minimal_order_data():
        """Генерация минимального набора данных для заказа"""
        return {
            "firstName": CommonGenerator.generate_random_string(6),
            "lastName": CommonGenerator.generate_random_string(8),
            "phone": CommonGenerator.generate_random_phone(),
            "deliveryDate": CommonGenerator.generate_random_date()
        }