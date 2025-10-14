class Config:
    
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    
    """Ручки для взаимодействия с курьером"""
    COURIER_CREATE_URL = f'{BASE_URL}/courier'
    # Создание нового курьера (регистрация в системе)
    # POST запрос с телом {login, password, firstName}
    
    COURIER_LOGIN_URL = f'{BASE_URL}/courier/login'
    # Авторизация курьера в системе (получение ID курьера для последующих операций)
    # POST запрос с телом {login, password}, возвращает courier id
    
    COURIER_DELETE_URL = f'{BASE_URL}/courier/{{id}}'
    # Удаление курьера из системы (:id заменяется на actual courier ID)
    # DELETE запрос, требуется courier id
    
    """Ручки для взаимодействия с заказом"""
    ORDER_URL = f'{BASE_URL}/orders'
    # Создание нового заказа и получение списка заказов
    # POST запрос с телом заказа
    
    ORDER_ACCEPT_URL = f'{ORDER_URL}/accept/{{id}}'
    # Принятие заказа курьером (:id заменяется на actual order ID)
    # PUT запрос, требуется order id и courier id
    
    ORDER_TRACK_URL = f'{ORDER_URL}/track'
    # Получение информации о конкретном заказе по его track number
    # GET запрос с параметром t (track number)