# 文件名必须以 test_ 开头，测试类名必须以 Test 开头，测试方法名必须以 test 开头，这样 pytest 才能识别测试用例
import pytest
from config.config import Config


class TestLogin:
    """测试登录相关接口"""

    def test_get_request(self, api_client):
        """测试GET请求 (使用conftest里的api_client fixture)"""
        url = f"{Config.BASE_URL}/get"
        params = {"key1": "value1", "key2": "value2"}

        # 发送GET请求
        response = api_client.get(url, params=params)

        # 断言
        assert response.status_code == 200
        resp_json = response.json()
        # 验证返回的参数是否与请求一致
        assert resp_json.get("args") == params
        print("GET请求测试通过！")

    def test_post_json(self, api_client):
        """测试POST JSON请求"""
        url = f"{Config.BASE_URL}/post"
        json_data = {"name": "pytest", "age": 5}

        response = api_client.post(url, json_data=json_data)

        assert response.status_code == 200
        resp_json = response.json()
        # 验证返回的json是否与我们发送的一致
        assert resp_json.get("json") == json_data
        print("POST JSON请求测试通过！")

    # 演示参数化测试 (从Excel读取数据)
    @pytest.mark.parametrize("username, password", [
        ("user1", "pass1"),
        ("user2", "pass2"),
    ])
    def test_login_parametrize(self, api_client, username, password):
        """参数化测试示例"""
        url = f"{Config.BASE_URL}/post"
        data = {"username": username, "password": password}

        response = api_client.post(url, data=data)
        assert response.status_code == 200
        # 验证返回的表单数据
        resp_json = response.json()
        assert resp_json.get("form") == data
        print(f"参数化测试通过: {username}")