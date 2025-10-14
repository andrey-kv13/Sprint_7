
import sys
import os
import pytest
from helpers.courier_generator import CourierGenerator
from helpers.order_generator import OrderGenerator
from helpers.data_cleaner import DataCleaner
from unittest.mock import Mock

@pytest.fixture
def create_and_delete_courier():
    """Фикстура создает курьера перед тестом и удаляет после"""
    login, password, first_name = CourierGenerator.register_new_courier()
    
    yield login, password, first_name
    
    # Cleanup после теста
    DataCleaner.delete_courier(login, password)
            
@pytest.fixture
def create_order():
    """Фикстура для создания тестового заказа"""
    track_id = OrderGenerator.create_order()
    yield track_id

@pytest.fixture
def mock_password_bug(mocker):
    """Фикстура для мока при отсутствии пароля"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"message": "Недостаточно данных для входа"}
    mocker.patch('requests.post', return_value=mock_response)
    return mock_response

def pytest_configure():
    """Настройка путей перед выполнением тестов"""
    
    # Получаем абсолютный путь к корневой директории проекта
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Добавляем корневую директорию в sys.path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    print(f"Project root added to path: {project_root}")