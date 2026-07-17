
import json
from typing import Optional, Dict, Any, Union
from urllib3.util.retry import Retry

import requests
from requests.adapters import HTTPAdapter

from config.config import config
from common.logger import get_logger
from common.exceptions import APIRequestError, APIResponseError


class RESTClient:
    """
    RESTful API 客户端基类
    支持多服务调用
    """

    def __init__(self, service_name: str = None, base_url: str = None,
                 timeout: int = None, max_retries: int = None):
        """
        初始化 REST 客户端
        :param service_name: 服务名称 (model, order, user, product, payment)
        :param base_url: 基础URL（优先级高于 service_name）
        :param timeout: 超时时间
        :param max_retries: 最大重试次数
        """
        self.service_name = service_name

        if base_url:
            self.base_url = base_url.rstrip('/')
        elif service_name:
            self.base_url = config.get_service_url(service_name)
        else:
            # 默认使用模型服务
            self.base_url = config.MODEL_SERVICE_URL

        self.timeout = timeout or config.TIMEOUT
        self.max_retries = max_retries or config.MAX_RETRIES

        self.session = requests.Session()
        self.logger = get_logger(f"RESTClient({service_name or 'default'})")

        # 配置重试策略
        self._setup_retry()
        # 配置默认请求头
        self._setup_default_headers()
        # 配置认证信息
        self._setup_auth()

        self.logger.info(f"客户端初始化完成，服务: {service_name}, URL: {self.base_url}")

    def _setup_retry(self):
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _setup_default_headers(self):
        self.session.headers.update({
            'User-Agent': 'Pytest-AutoTest/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

    def _setup_auth(self):
        auth_type = config.AUTH_TYPE
        credentials = config.get_auth_credentials()

        if auth_type == 'basic' and credentials:
            self.session.auth = (credentials.get('username'), credentials.get('password'))
        elif auth_type == 'bearer' and credentials.get('token'):
            self.session.headers.update({'Authorization': f"Bearer {credentials['token']}"})

    def set_headers(self, headers: Dict[str, str]):
        """设置/更新请求头"""
        self.session.headers.update(headers)

    def set_auth(self, auth_type: str, credentials: Dict[str, str]):
        """动态设置认证"""
        if auth_type == 'basic':
            self.session.auth = (credentials.get('username'), credentials.get('password'))
        elif auth_type == 'bearer':
            self.session.headers.update({'Authorization': f"Bearer {credentials.get('token')}"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)

        if 'headers' in kwargs:
            self.session.headers.update(kwargs.pop('headers'))

        try:
            self.logger.info(f"{method} {url}")
            response = self.session.request(method, url, **kwargs)
            self.logger.info(f"响应状态: {response.status_code}")

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            self.logger.error(f"请求超时: {url}")
            raise APIRequestError(f"请求超时: {url}")
        except Exception as e:
            self.logger.error(f"请求异常: {e}")
            raise APIRequestError(f"请求异常: {e}")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理响应"""
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}, 响应: {response.text}")
            raise APIResponseError(f"HTTP错误: {e}")
        except requests.exceptions.JSONDecodeError:
            return {'text': response.text, 'status_code': response.status_code}

    def _mask_sensitive(self, data: Dict) -> Dict:
        """脱敏处理"""
        if not data:
            return data
        masked = data.copy()
        sensitive_keys = ['password', 'token', 'secret', 'api_key']
        for key in sensitive_keys:
            if key in masked:
                masked[key] = '***'
            elif 'json' in masked and isinstance(masked.get('json'), dict):
                for sk in sensitive_keys:
                    if sk in masked['json']:
                        masked['json'][sk] = '***'
        return masked

    # ===== 公共方法 =====
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        return self._request('POST', endpoint, data=data, json=json_data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        return self._request('PUT', endpoint, data=data, json=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._request('DELETE', endpoint, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict] = None,
              json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        return self._request('PATCH', endpoint, data=data, json=json_data, **kwargs)