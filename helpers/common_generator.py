import random
import string

class CommonGenerator:
    
    @staticmethod
    def generate_random_string(length=10):
        """Генерация случайной строки из букв и цифр"""
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def generate_random_phone():
        """Генерация случайного номера телефона"""
        return f"+7{random.randint(900, 999)}{random.randint(100, 999)}{random.randint(10, 99)}{random.randint(10, 99)}"
    
    @staticmethod
    def generate_random_date():
        """Генерация случайной даты в формате YYYY-MM-DD"""
        year = random.randint(2020, 2024)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"