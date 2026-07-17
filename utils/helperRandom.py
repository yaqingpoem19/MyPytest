# utils/helperRandom.py
import json
import random
import string
from typing import Dict, Any
from datetime import datetime, timedelta


class DataGenerator:
    """测试数据生成器"""

    @staticmethod
    def random_string(length: int = 8, include_digits: bool = True) -> str:
        """生成随机字符串"""
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def random_number(length: int = 6) -> str:
        """生成随机数字字符串"""
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def random_email(domain: str = "test.com") -> str:
        """生成随机邮箱"""
        return f"{DataGenerator.random_string(8)}@{domain}"

    @staticmethod
    def random_phone() -> str:
        """生成随机手机号"""
        return f"1{DataGenerator.random_number(10)}"

    @staticmethod
    def random_int(min_val: int = 1, max_val: int = 1000) -> int:
        """生成随机整数"""
        return random.randint(min_val, max_val)

    @staticmethod
    def random_float(min_val: float = 0.0, max_val: float = 100.0, precision: int = 2) -> float:
        """生成随机浮点数"""
        value = random.uniform(min_val, max_val)
        return round(value, precision)

    @staticmethod
    def random_bool() -> bool:
        """生成随机布尔值"""
        return random.choice([True, False])

    @staticmethod
    def random_choice(items: List) -> any:
        """从列表中随机选择"""
        return random.choice(items)

    @staticmethod
    def random_date(start_date: str = "2020-01-01", end_date: str = "2025-12-31") -> str:
        """生成随机日期"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end - start
        random_days = random.randint(0, delta.days)
        result = start + timedelta(days=random_days)
        return result.strftime("%Y-%m-%d")

    @staticmethod
    def random_datetime() -> str:
        """生成随机日期时间"""
        now = datetime.now()
        delta = timedelta(days=random.randint(-365, 365))
        result = now + delta
        return result.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_user_data() -> dict:
        """生成用户测试数据"""
        username = DataGenerator.random_string(6)
        return {
            "username": username,
            "email": DataGenerator.random_email(),
            "password": "Test@123",
            "phone": DataGenerator.random_phone(),
            "nickname": f"user_{DataGenerator.random_number(4)}"
        }

    @staticmethod
    def generate_order_data() -> dict:
        """生成订单测试数据"""
        return {
            "order_no": f"ORD{DataGenerator.random_number(12)}",
            "product_name": DataGenerator.random_string(10),
            "quantity": DataGenerator.random_int(1, 10),
            "price": DataGenerator.random_float(10, 1000),
            "status": DataGenerator.random_choice(["pending", "paid", "shipped", "delivered"])
        }

    @staticmethod
    def extract_value(data: Dict, path: str, default=None):
        """
        从嵌套字典中提取值，支持点号路径
        例: extract_value(data, 'user.name')
        """
        keys = path.split('.')
        result = data
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return default
        return result