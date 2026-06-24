# coding=utf-8
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

class PyREST(object):
    def __init__(self, endpoint, header={'Content-Type': 'application/json', 'Connection': 'close'}):
        self.session = requests.session()
        self.session.headers.update(header)
        self.response = requests.Response()
        self.endpoint = endpoint

    def get(self, resource, params=None, stream=False):
        self.response = self.session.get(self.endpoint+resource, params=params, stream=stream)
        return self.response

    def post(self, resource, payload=None, params=None):
        self.response = self.session.post(self.endpoint+resource, json=payload, params=params)
        return self.response

    def post_data(self, resource, data=None):
        # header = {'Content-type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive'}
        # self.session.headers.update(header)

        self.response = self.session.post(self.endpoint + resource, data)
        print(self.response.url)
        return self.response

    def post_file(self, resource, files):
        self.response = self.session.post(self.endpoint+resource, files=files)

    def put(self, resource, payload=None, params=None):
        self.response = self.session.put(self.endpoint+resource, json=payload, params=params)

    def option(self, resource):
        self.response = self.session.options(self.endpoint+resource)
        return self.response

    def delete(self, resource):
        self.response = self.session.delete(self.endpoint+resource)
        return self.response

    def url(self):
        return self.response.url

    def json_result(self):
        '''
            response result returned as a json format.
        '''
        return self.response.json()

    def text(self):
        '''
            response result returned as a txt format.
        '''
        return self.response.text

    def status_code(self):
        '''
            response result returned status_code
        '''
        return self.response.status_code


if __name__ == '__main__':
    req = PyREST()







