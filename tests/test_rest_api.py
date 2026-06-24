# tests/test_rest_api.py
import pytest
from config.config import Config


class TestRESTAPI:
    """RESTful API 测试"""

    def test_get_user(self, rest_client):
        """测试 GET 请求"""
        response = rest_client.get('/api/users/1')
        assert response['id'] == 1
        assert 'name' in response

    def test_create_user(self, rest_client):
        """测试 POST 请求"""
        user_data = {
            'name': '张三',
            'email': 'zhangsan@example.com'
        }
        response = rest_client.post('/api/users', json_data=user_data)
        assert response['status'] == 'success'
        assert response['data']['name'] == '张三'

    def test_update_user(self, rest_client):
        """测试 PUT 请求"""
        update_data = {'name': '李四'}
        response = rest_client.put('/api/users/1', json_data=update_data)
        assert response['status'] == 'success'

    def test_delete_user(self, rest_client):
        """测试 DELETE 请求"""
        response = rest_client.delete('/api/users/1')
        assert response['status'] == 'success'