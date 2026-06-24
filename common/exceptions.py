# common/exceptions.py
class APIException(Exception):
    """API异常基类"""
    pass

class APIRequestError(APIException):
    """请求异常"""
    pass

class APIResponseError(APIException):
    """响应异常"""
    pass

class AuthenticationError(APIException):
    """认证异常"""
    pass