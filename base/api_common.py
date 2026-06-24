# base/method.py
# base/api_common.py
import requests
import json

class RequestMethod:
    @staticmethod
    def post(url, data=None, json_data=None, headers=None):
        """
        封装POST请求
        :param url: 接口地址
        :param data: form表单数据
        :param json_data: json格式数据
        :param headers: 请求头
        :return: 响应对象
        """
        try:
            response = requests.post(url, data=data, json=json_data, headers=headers)
            return response
        except Exception as e:
            print(f"请求报错: {e}")
            raise e

    @staticmethod
    def get(url, params=None, headers=None):
        """封装GET请求"""
        try:
            response = requests.get(url, params=params, headers=headers)
            return response
        except Exception as e:
            print(f"请求报错: {e}")
            raise e