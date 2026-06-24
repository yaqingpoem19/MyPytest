# base/rest_client.py
from typing import Optional, Dict, Any, Union
import json

from .client_base import BaseClient
from common.exceptions import APIRequestError
from config.config import config


class RESTClient(BaseClient):
    """
    RESTful API 客户端
    支持 GET, POST, PUT, DELETE, PATCH 等方法
    """

    def __init__(self, base_url: str = None, **kwargs):
        """
        初始化 REST 客户端
        :param base_url: 如果未指定，使用配置文件中的地址
        """
        if base_url is None:
            base_url = config.REST_BASE_URL

        timeout = kwargs.pop('timeout', config.TIMEOUT)
        max_retries = kwargs.pop('max_retries', config.MAX_RETRIES)

        super().__init__(base_url, timeout=timeout, max_retries=max_retries)

        # 设置默认请求头
        self.set_headers({
            'User-Agent': config.USER_AGENT,
            'Accept': config.ACCEPT,
            'Accept-Language': config.ACCEPT_LANGUAGE,
        })

        # 设置认证
        auth_credentials = config.get_auth_credentials()
        if auth_credentials:
            self.set_auth(config.AUTH_TYPE, auth_credentials)

        self.logger.info(f"REST客户端初始化: {base_url}, 环境: {config.CURRENT_ENV}")

    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发起 REST API 请求
        :param method: HTTP方法 (GET, POST, PUT, DELETE, PATCH)
        :param endpoint: 接口路径
        :param kwargs: 其他参数 (params, data, json, headers)
        :return: 响应JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)

        # 合并请求头
        if 'headers' in kwargs:
            self.session.headers.update(kwargs.pop('headers'))

        try:
            self.logger.info(f"{method} {url}")
            if kwargs:
                self.logger.debug(f"请求参数: {self._mask_sensitive_data(kwargs)}")

            response = self.session.request(method, url, **kwargs)
            self.logger.info(f"响应状态码: {response.status_code}")

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            self.logger.error(f"请求超时: {url}")
            raise APIRequestError(f"请求超时: {url}")
        except requests.exceptions.ConnectionError:
            self.logger.error(f"连接错误: {url}")
            raise APIRequestError(f"连接错误: {url}")
        except Exception as e:
            self.logger.error(f"请求异常: {e}")
            raise APIRequestError(f"请求异常: {e}")

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """GET 请求"""
        return self.request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict] = None,
             json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """POST 请求"""
        return self.request('POST', endpoint, data=data, json=json_data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """PUT 请求"""
        return self.request('PUT', endpoint, data=data, json=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """DELETE 请求"""
        return self.request('DELETE', endpoint, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict] = None,
              json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """PATCH 请求"""
        return self.request('PATCH', endpoint, data=data, json=json_data, **kwargs)

    @staticmethod
    def _mask_sensitive_data(data: Dict) -> Dict:
        """脱敏处理，隐藏密码等敏感信息"""
        if not data:
            return data
        masked = data.copy()
        sensitive_keys = ['password', 'token', 'secret', 'api_key']
        for key in sensitive_keys:
            if key in masked:
                masked[key] = '***'
        return masked