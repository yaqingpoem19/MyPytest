# base/soap_client.py
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any, Union
from xml.dom import minidom

import requests
from .base_client import BaseClient
from common.exceptions import APIRequestError, APIResponseError


class SOAPClient(BaseClient):
    """
    SOAP Web Service 客户端
    支持 SOAP 1.1 和 SOAP 1.2
    """

    def __init__(self, wsdl_url: str, soap_version: str = '1.1', **kwargs):
        """
        初始化 SOAP 客户端
        :param wsdl_url: WSDL 地址（或服务地址）
        :param soap_version: SOAP版本 ('1.1' 或 '1.2')
        """
        super().__init__(wsdl_url, **kwargs)
        self.soap_version = soap_version
        self.namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/' if soap_version == '1.1'
            else 'http://www.w3.org/2003/05/soap-envelope',
            'xsd': 'http://www.w3.org/2001/XMLSchema',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }
        self._setup_soap_headers()
        self.logger.info(f"SOAP客户端初始化完成，服务地址: {wsdl_url}, 版本: {soap_version}")

    def _setup_soap_headers(self):
        """设置 SOAP 请求头"""
        if self.soap_version == '1.1':
            self.session.headers.update({
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '',
            })
        else:  # SOAP 1.2
            self.session.headers.update({
                'Content-Type': 'application/soap+xml; charset=utf-8',
            })

    def request(self, method: str, endpoint: str = '', **kwargs) -> Dict[str, Any]:
        """
        SOAP 请求（重写基类方法，但SOAP通常用POST）
        """
        # SOAP通常只用POST方法
        return self.soap_call(method, endpoint, **kwargs)

    def soap_call(self, action: str, endpoint: str = '',
                  body: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        调用 SOAP Web Service
        :param action: 操作名称（方法名）
        :param endpoint: 端点路径（可选）
        :param body: 请求体数据（字典格式，将被转换为XML）
        :param kwargs: 额外参数
        :return: 响应数据（转换为字典）
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url

        # 构建 SOAP 请求体
        soap_body = self._build_soap_envelope(action, body)
        self.logger.info(f"SOAP调用: {action}, URL: {url}")
        self.logger.debug(f"SOAP请求体: {soap_body}")

        # 设置 SOAPAction 头
        if self.soap_version == '1.1' and action:
            self.session.headers.update({'SOAPAction': action})

        try:
            response = self.session.post(url, data=soap_body.encode('utf-8'), timeout=self.timeout)
            self.logger.info(f"响应状态码: {response.status_code}")

            # 解析 SOAP 响应
            return self._parse_soap_response(response.text, action)

        except requests.exceptions.Timeout:
            self.logger.error(f"SOAP请求超时: {url}")
            raise APIRequestError(f"SOAP请求超时: {url}")
        except Exception as e:
            self.logger.error(f"SOAP请求异常: {e}")
            raise APIRequestError(f"SOAP请求异常: {e}")

    def _build_soap_envelope(self, action: str, body: Optional[Dict] = None) -> str:
        """构建 SOAP 信封"""
        root = ET.Element(f"{{{self.namespaces['soap']}}}Envelope")

        # 添加Header（可选）
        header = ET.SubElement(root, f"{{{self.namespaces['soap']}}}Header")

        # 添加Body
        body_elem = ET.SubElement(root, f"{{{self.namespaces['soap']}}}Body")

        if body:
            # 创建操作节点
            action_elem = ET.SubElement(body_elem, action)

            # 添加数据
            self._dict_to_xml(body, action_elem)

        # 格式化XML
        xml_str = ET.tostring(root, encoding='unicode')
        return self._pretty_xml(xml_str)

    def _dict_to_xml(self, data: Dict, parent: ET.Element):
        """将字典转换为XML元素"""
        for key, value in data.items():
            # 处理命名空间
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_xml(value, child)
            elif isinstance(value, list):
                for item in value:
                    child = ET.SubElement(parent, key)
                    if isinstance(item, dict):
                        self._dict_to_xml(item, child)
                    else:
                        child.text = str(item)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)

    def _parse_soap_response(self, response_xml: str, action: str) -> Dict[str, Any]:
        """解析 SOAP 响应"""
        try:
            root = ET.fromstring(response_xml)

            # 查找Body
            body = root.find(f".//{{{self.namespaces['soap']}}}Body")
            if body is None:
                raise APIResponseError("SOAP响应中找不到Body")

            # 查找Fault（错误）
            fault = body.find(f".//{{{self.namespaces['soap']}}}Fault")
            if fault is not None:
                fault_code = fault.findtext("faultcode", "Unknown")
                fault_string = fault.findtext("faultstring", "Unknown error")
                raise APIResponseError(f"SOAP Fault: {fault_code} - {fault_string}")

            # 提取响应数据
            # 查找响应节点（通常是 action + Response）
            response_node_name = f"{action}Response"
            response_node = body.find(f".//{response_node_name}")

            if response_node is not None:
                result = self._xml_to_dict(response_node)
                return result
            else:
                # 如果没有找到具体的响应节点，返回整个body
                return self._xml_to_dict(body)

        except ET.ParseError as e:
            self.logger.error(f"SOAP响应解析失败: {e}")
            return {'raw_response': response_xml}
        except Exception as e:
            self.logger.error(f"SOAP响应处理异常: {e}")
            return {'raw_response': response_xml}

    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """将XML元素转换为字典"""
        result = {}

        for child in element:
            # 去除命名空间前缀
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

            if len(child) == 0:
                # 叶子节点
                result[tag] = child.text
            else:
                # 递归处理子节点
                child_dict = self._xml_to_dict(child)
                if tag in result:
                    # 处理重复标签（转为列表）
                    if not isinstance(result[tag], list):
                        result[tag] = [result[tag]]
                    result[tag].append(child_dict)
                else:
                    result[tag] = child_dict

        return result

    def _pretty_xml(self, xml_str: str) -> str:
        """格式化XML字符串"""
        try:
            dom = minidom.parseString(xml_str)
            return dom.toprettyxml(indent="  ")
        except Exception:
            return xml_str

    def set_soap_action(self, action: str):
        """设置 SOAPAction 头（SOAP 1.1）"""
        if self.soap_version == '1.1':
            self.session.headers.update({'SOAPAction': action})