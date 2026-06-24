# pytest 的核心特性文件，放在根目录，里面的fixture可以供所有 tests 目录下的用例使用
import pytest
from base.pyrest import RequestMethod

import pytest
from config.config import Config
from base.client_restful import RESTClient
from base.client_soap import SOAPClient
from base.client_webservice import WebServiceClient

@pytest.fixture(scope="session")
def api_client():
    """提供一个全局的API客户端fixture"""
    return RequestMethod()

@pytest.fixture(scope="function")
def test_data():
    """提供一个测试数据fixture，可以在这里写死数据或读取Excel"""
    # 这里简单演示，返回一个字典
    return {"username": "admin", "password": "123456"}

###############################################################

@pytest.fixture(scope='session')
def rest_client():
    """RESTful API 客户端 fixture"""
    return RESTClient()


@pytest.fixture(scope='session')
def soap_client():
    """SOAP 客户端 fixture"""
    return SOAPClient()


@pytest.fixture(scope='session')
def jsonrpc_client():
    """JSON-RPC 客户端 fixture"""
    return WebServiceClient(ws_type='jsonrpc')


@pytest.fixture(scope='session')
def xmlrpc_client():
    """XML-RPC 客户端 fixture"""
    return WebServiceClient(ws_type='xmlrpc')


@pytest.fixture(scope='session')
def env_info():
    """当前环境信息 fixture"""
    return config.get_env_info()