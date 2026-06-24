# base/base_client.py
import json
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from common.logger import get_logger
from common.exceptions import APIRequestError, APIResponseError


class BaseClient(ABC):
    """所有接口客户端的基类"""

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)

        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # 默认请求头
        self.session.headers.update({
            'User-Agent': 'Pytest-AutoTest/1.0',
            'Accept': 'application/json',
        })

    def set_headers(self, headers: Dict[str, str]):
        """设置请求头"""
        self.session.headers.update(headers)

    def set_auth(self, auth_type: str, credentials: Dict[str, str]):
        """设置认证"""
        if auth_type == 'basic':
            self.session.auth = (credentials.get('username'), credentials.get('password'))
        elif auth_type == 'bearer':
            self.session.headers.update({'Authorization': f"Bearer {credentials.get('token')}"})
        elif auth_type == 'api_key':
            self.session.headers.update({credentials.get('key'): credentials.get('value')})

    @abstractmethod
    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """发起请求的抽象方法，子类必须实现"""
        pass

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """统一处理响应"""
        try:
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
        except requests.exceptions.JSONDecodeError:
            return {'text': response.text}
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}, 响应内容: {response.text}")
            raise APIResponseError(f"HTTP错误: {e}")
        except Exception as e:
            self.logger.error(f"响应处理异常: {e}")
            raise APIResponseError(f"响应处理异常: {e}")