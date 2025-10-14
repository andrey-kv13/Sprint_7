import requests
from config.config import Config

class ApiClient:

    @staticmethod
    def get_request_orders():
        return requests.get(Config.ORDER_URL)
    
    @staticmethod
    def get_request_order_by_track_id(track_id):
        return requests.get(Config.ORDER_TRACK_URL, params={'t':track_id})
    
    @staticmethod
    def post_request_create_courier(payload):
        return requests.post(Config.COURIER_CREATE_URL, json = payload)
    
    @staticmethod
    def post_request_login_courier(payload):
        return requests.post(Config.COURIER_LOGIN_URL, json = payload)
    
    @staticmethod
    def post_request_order_create(payload):
        return requests.post(Config.ORDER_URL, json = payload)
    
    @staticmethod
    def put_request_order_accept(order_id, courier_id):
        return requests.put(Config.ORDER_ACCEPT_URL.format(id=order_id), params=courier_id)
    
    @staticmethod
    def delete_request_courier(courier_id):
        return requests.delete(Config.COURIER_DELETE_URL.format(id=courier_id))
