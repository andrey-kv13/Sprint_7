from helpers.api_client import ApiClient
from helpers.courier_generator import CourierGenerator

class DataCleaner:
    
    @staticmethod
    def delete_courier(login, password):
        """Удаление курьера по логину и паролю"""
        try:
            courier_id = CourierGenerator.get_courier_id(login, password)
            ApiClient.delete_request_courier(courier_id)
        except Exception as e:
           raise Exception(f"Error deleting courier {login}: {e}")