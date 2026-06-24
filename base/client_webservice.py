# base/webservice_client.py
from typing import Optional, Dict, Any
import requests

from .client_soap import SOAPClient
from common.exceptions import APIRequestError


class WebServiceClient(SOAPClient):
    """
    WebService 客户端（通用）
    实际上是 SOAP 客户端的别名，但增加了一些便利方法
    支持 RESTful 风格的 WebService（JSON-RPC, XML-RPC）
    """

    def __init__(self, base_url: str, ws_type: str = 'soap', **kwargs):
        """
        初始化 WebService 客户端
        :param base_url: 服务地址
        :param ws_type: WebService类型 ('soap', 'xmlrpc', 'jsonrpc')
        """
        if ws_type == 'soap':
            super().__init__(base_url, **kwargs)
        elif ws_type == 'xmlrpc':
            self.ws_type = 'xmlrpc'
            self.base_url = base_url.rstrip('/')
            self.timeout = kwargs.get('timeout', 30)
            self.session = requests.Session()
            self.logger = get_logger('XMLRPCClient')
            self.session.headers.update({'Content-Type': 'text/xml'})
        elif ws_type == 'jsonrpc':
            self.ws_type = 'jsonrpc'
            self.base_url = base_url.rstrip('/')
            self.timeout = kwargs.get('timeout', 30)
            self.session = requests.Session()
            self.logger = get_logger('JSONRPCClient')
            self.session.headers.update({'Content-Type': 'application/json'})
        else:
            raise ValueError(f"不支持的WebService类型: {ws_type}")

        self.ws_type = ws_type
        self.logger.info(f"WebService客户端初始化完成，类型: {ws_type}, URL: {base_url}")

    def request(self, method: str, endpoint: str = '', **kwargs) -> Dict[str, Any]:
        """统一请求接口"""
        if self.ws_type == 'soap':
            return self.soap_call(method, endpoint, **kwargs)
        elif self.ws_type == 'xmlrpc':
            return self._xmlrpc_call(method, **kwargs)
        elif self.ws_type == 'jsonrpc':
            return self._jsonrpc_call(method, **kwargs)
        else:
            raise ValueError(f"不支持的WebService类型: {self.ws_type}")

    def _xmlrpc_call(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """XML-RPC 调用"""
        # 构建 XML-RPC 请求体
        xml_request = self._build_xmlrpc_request(method, params)

        try:
            response = self.session.post(self.base_url, data=xml_request, timeout=self.timeout)
            response.raise_for_status()

            # 解析 XML-RPC 响应
            return self._parse_xmlrpc_response(response.text)

        except Exception as e:
            self.logger.error(f"XML-RPC调用失败: {e}")
            raise APIRequestError(f"XML-RPC调用失败: {e}")

    def _build_xmlrpc_request(self, method: str, params: Optional[Dict] = None) -> str:
        """构建 XML-RPC 请求"""
        xml = f'<?xml version="1.0"?>\n<methodCall>\n'
        xml += f'  <methodName>{method}</methodName>\n'

        if params:
            xml += '  <params>\n'
            for key, value in params.items():
                xml += f'    <param>\n'
                xml += f'      <value><{self._xmlrpc_type(value)}>{value}</{self._xmlrpc_type(value)}></value>\n'
                xml += f'    </param>\n'
            xml += '  </params>\n'

        xml += '</methodCall>'
        return xml

    def _xmlrpc_type(self, value) -> str:
        """获取 XML-RPC 类型"""
        if isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'double'
        elif isinstance(value, bool):
            return 'boolean'
        else:
            return 'string'

    def _parse_xmlrpc_response(self, response_xml: str) -> Dict[str, Any]:
        """解析 XML-RPC 响应"""
        import xml.etree.ElementTree as ET

        try:
            root = ET.fromstring(response_xml)

            # 检查是否有 fault
            fault = root.find('.//fault')
            if fault is not None:
                fault_value = fault.find('.//value')
                if fault_value is not None:
                    fault_struct = fault_value.find('.//struct')
                    if fault_struct is not None:
                        fault_code = fault_struct.find(".//member[name='faultCode']/value")
                        fault_string = fault_struct.find(".//member[name='faultString']/value")
                        raise APIResponseError(
                            f"XML-RPC Fault: {fault_code.text if fault_code is not None else 'Unknown'} - "
                            f"{fault_string.text if fault_string is not None else 'Unknown error'}"
                        )

            # 提取返回结果
            params = root.find('.//params')
            if params is not None:
                param = params.find('.//param')
                if param is not None:
                    value = param.find('.//value')
                    if value is not None:
                        # 尝试提取各种类型的值
                        for child in value:
                            return {child.tag: child.text}

            return {'raw_response': response_xml}

        except ET.ParseError as e:
            self.logger.error(f"XML-RPC响应解析失败: {e}")
            return {'raw_response': response_xml}

    def _jsonrpc_call(self, method: str, params: Optional[Dict] = None,
                      rpc_id: int = 1) -> Dict[str, Any]:
        """JSON-RPC 调用"""
        # 构建 JSON-RPC 请求体
        json_request = {
            'jsonrpc': '2.0',
            'method': method,
            'id': rpc_id,
        }

        if params:
            json_request['params'] = params

        try:
            response = self.session.post(self.base_url, json=json_request, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()

            # 检查错误
            if 'error' in result and result['error']:
                error = result['error']
                raise APIResponseError(f"JSON-RPC Error: {error.get('code')} - {error.get('message')}")

            return result

        except requests.exceptions.JSONDecodeError as e:
            self.logger.error(f"JSON-RPC响应解析失败: {e}")
            return {'raw_response': response.text}
        except Exception as e:
            self.logger.error(f"JSON-RPC调用失败: {e}")
            raise APIRequestError(f"JSON-RPC调用失败: {e}")