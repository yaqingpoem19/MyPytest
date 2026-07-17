# common/exceptions.py
class AutoTestException(Exception):
    """自动化测试异常基类"""
    pass


class APIRequestError(AutoTestException):
    """API请求异常"""
    pass


class APIResponseError(AutoTestException):
    """API响应异常"""
    pass


class AuthenticationError(AutoTestException):
    """认证异常"""
    pass


class UIActionError(AutoTestException):
    """UI操作异常"""
    pass


class ConfigError(AutoTestException):
    """配置异常"""
    pass


class DataError(AutoTestException):
    """数据异常"""
    pass