# tests/test_api.py
import pytest
import json
from config.config import config
from common.logger import get_logger
from utils.helperRandom import DataGenerator

logger = get_logger("test_user_api")


class TestUserAPI:
    """用户API测试"""

    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_user(self, auth_api_client):
        """测试创建用户"""
        user_data = DataGenerator.generate_user_data()

        logger.info(f"创建用户: {user_data['username']}")
        response = auth_api_client.post("/api/users", json_data=user_data)

        assert response.get("code") == 200
        assert response.get("data", {}).get("username") == user_data["username"]
        logger.info(f"✅ 用户创建成功: {user_data['username']}")

    @pytest.mark.api
    def test_get_user_list(self, auth_api_client):
        """测试获取用户列表"""
        params = {"page": 1, "size": 10}
        response = auth_api_client.get("/api/users", params=params)

        assert response.get("code") == 200
        assert "data" in response
        assert "list" in response.get("data", {})
        logger.info(f"✅ 获取用户列表成功，总数: {response.get('data', {}).get('total', 0)}")

    @pytest.mark.api
    def test_get_user_by_id(self, auth_api_client):
        """测试根据ID获取用户"""
        user_id = 1
        response = auth_api_client.get(f"/api/users/{user_id}")

        assert response.get("code") == 200
        assert response.get("data", {}).get("id") == user_id
        logger.info(f"✅ 获取用户成功: ID={user_id}")

    @pytest.mark.api
    def test_update_user(self, auth_api_client):
        """测试更新用户"""
        user_id = 1
        update_data = {"nickname": f"updated_{DataGenerator.random_string(4)}"}

        response = auth_api_client.put(f"/api/users/{user_id}", json_data=update_data)

        assert response.get("code") == 200
        logger.info(f"✅ 用户更新成功: ID={user_id}")

    @pytest.mark.api
    def test_delete_user(self, auth_api_client):
        """测试删除用户"""
        # 先创建一个用户
        user_data = DataGenerator.generate_user_data()
        create_resp = auth_api_client.post("/api/users", json_data=user_data)
        user_id = create_resp.get("data", {}).get("id")

        # 删除用户
        response = auth_api_client.delete(f"/api/users/{user_id}")

        assert response.get("code") == 200
        logger.info(f"✅ 用户删除成功: ID={user_id}")


class TestOrderAPI:
    """订单接口测试"""

    def test_get_order_list(self, client):
        """测试获取订单列表"""
        response = client.get('/orders')
        assert isinstance(response, list)

    def test_create_order(self, client):
        """测试创建订单"""
        order_data = {
            "product": "笔记本电脑",
            "quantity": 2,
            "price": 5999.00
        }
        response = client.post('/orders', json_data=order_data)
        assert response.get('status') == 'success'
        assert response.get('data', {}).get('product') == '笔记本电脑'


class TestAuthAPI:
    """认证接口测试"""

    def test_login(self, client):
        """测试登录"""
        login_data = {
            "username": config.AUTH_USERNAME,
            "password": config.AUTH_PASSWORD
        }
        response = client.post('/auth/login', json_data=login_data)
        assert response.get('status') == 'success'
        assert 'token' in response.get('data', {})

    def test_invalid_login(self, client):
        """测试登录失败"""
        login_data = {
            "username": "wronguser",
            "password": "wrongpass"
        }
        with pytest.raises(Exception):
            client.post('/auth/login', json_data=login_data)


class TestConfigAPI:
    """配置相关测试"""

    def test_switch_env(self, client):
        """测试环境切换"""
        original_env = config.CURRENT_ENV

        # 切换到 staging
        config.switch_env('staging')
        assert config.CURRENT_ENV == 'staging'
        assert config.BASE_URL != client.base_url

        # 更新客户端
        client.base_url = config.BASE_URL

        # 切换回原环境
        config.switch_env(original_env)

    def test_env_info(self, env_info):
        """测试环境信息"""
        assert 'environment' in env_info
        assert 'base_url' in env_info
        assert 'timeout' in env_info
        assert env_info['timeout'] > 0