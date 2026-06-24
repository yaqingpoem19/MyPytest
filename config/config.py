# config/config.py
from pathlib import Path
from typing import Optional, Dict
from .config_reader import config as _config


class Config:
    """
    配置类 - 提供更友好的访问接口
    使用示例:
        Config.BASE_URL          # 获取当前环境的 BASE_URL
        Config.AUTH_TOKEN        # 获取认证配置
        Config.REPORT_DIR        # 获取报告目录
    """

    # ==================== 环境配置 ====================

    @classmethod
    @property
    def CURRENT_ENV(cls) -> str:
        """当前运行环境"""
        return _config.get('ENV', 'CURRENT_ENV')

    @classmethod
    @property
    def BASE_URL(cls) -> str:
        """基础URL"""
        return _config.get_env_value('BASE_URL')

    @classmethod
    @property
    def REST_BASE_URL(cls) -> str:
        """REST API 基础URL"""
        return _config.get_env_value('REST_BASE_URL')

    @classmethod
    @property
    def SOAP_WSDL_URL(cls) -> str:
        """SOAP WSDL URL"""
        return _config.get_env_value('SOAP_WSDL_URL')

    @classmethod
    @property
    def XMLRPC_URL(cls) -> str:
        """XML-RPC URL"""
        return _config.get_env_value('XMLRPC_URL')

    @classmethod
    @property
    def JSONRPC_URL(cls) -> str:
        """JSON-RPC URL"""
        return _config.get_env_value('JSONRPC_URL')

    @classmethod
    @property
    def TIMEOUT(cls) -> int:
        """请求超时时间（秒）"""
        return _config.get_env_int('TIMEOUT', 30)

    @classmethod
    @property
    def MAX_RETRIES(cls) -> int:
        """最大重试次数"""
        return _config.get_env_int('MAX_RETRIES', 3)

    @classmethod
    @property
    def LOG_LEVEL(cls) -> str:
        """日志级别"""
        return _config.get_env_value('LOG_LEVEL', 'INFO')

    # ==================== 认证配置 ====================

    @classmethod
    @property
    def AUTH_TYPE(cls) -> str:
        """默认认证类型"""
        return _config.get('AUTH', 'DEFAULT_AUTH_TYPE', 'bearer')

    @classmethod
    @property
    def AUTH_USERNAME(cls) -> str:
        """认证用户名"""
        return _config.get('AUTH', 'TEST_USERNAME', '')

    @classmethod
    @property
    def AUTH_PASSWORD(cls) -> str:
        """认证密码"""
        return _config.get('AUTH', 'TEST_PASSWORD', '')

    @classmethod
    @property
    def API_KEY(cls) -> str:
        """API Key"""
        return _config.get('AUTH', 'API_KEY', '')

    @classmethod
    @property
    def BEARER_TOKEN(cls) -> str:
        """Bearer Token"""
        return _config.get('AUTH', 'BEARER_TOKEN', '')

    # ==================== 数据库配置 ====================

    @classmethod
    @property
    def DB_HOST(cls) -> str:
        return _config.get('DATABASE', 'DB_HOST', 'localhost')

    @classmethod
    @property
    def DB_PORT(cls) -> int:
        return _config.get_int('DATABASE', 'DB_PORT', 3306)

    @classmethod
    @property
    def DB_USER(cls) -> str:
        return _config.get('DATABASE', 'DB_USER', '')

    @classmethod
    @property
    def DB_PASSWORD(cls) -> str:
        return _config.get('DATABASE', 'DB_PASSWORD', '')

    @classmethod
    @property
    def DB_NAME(cls) -> str:
        return _config.get('DATABASE', 'DB_NAME', '')

    # ==================== 报告配置 ====================

    @classmethod
    @property
    def REPORT_DIR(cls) -> Path:
        """报告目录"""
        dir_name = _config.get('REPORT', 'REPORT_DIR', 'report')
        return Path(__file__).parent.parent / dir_name

    @classmethod
    @property
    def REPORT_NAME(cls) -> str:
        """报告文件名"""
        return _config.get('REPORT', 'REPORT_NAME', 'test_report.html')

    @classmethod
    @property
    def ALLURE_RESULTS_DIR(cls) -> Path:
        """Allure结果目录"""
        dir_name = _config.get('REPORT', 'ALLURE_RESULTS_DIR', 'allure-results')
        return Path(__file__).parent.parent / dir_name

    # ==================== 日志配置 ====================

    @classmethod
    @property
    def LOG_DIR(cls) -> Path:
        """日志目录"""
        dir_name = _config.get('LOG', 'LOG_DIR', 'log')
        return Path(__file__).parent.parent / dir_name

    @classmethod
    @property
    def LOG_FILE(cls) -> str:
        """日志文件名"""
        return _config.get('LOG', 'LOG_FILE', 'test.log')

    @classmethod
    @property
    def LOG_ROTATION(cls) -> str:
        """日志轮转策略"""
        return _config.get('LOG', 'LOG_ROTATION', '1 day')

    @classmethod
    @property
    def LOG_RETENTION(cls) -> str:
        """日志保留策略"""
        return _config.get('LOG', 'LOG_RETENTION', '7 days')

    # ==================== 请求头配置 ====================

    @classmethod
    @property
    def USER_AGENT(cls) -> str:
        return _config.get('HEADERS', 'USER_AGENT', 'Pytest-AutoTest/1.0')

    @classmethod
    @property
    def ACCEPT(cls) -> str:
        return _config.get('HEADERS', 'ACCEPT', 'application/json')

    @classmethod
    @property
    def ACCEPT_LANGUAGE(cls) -> str:
        return _config.get('HEADERS', 'ACCEPT_LANGUAGE', 'zh-CN,zh;q=0.9')

    # ==================== 测试数据配置 ====================

    @classmethod
    @property
    def TEST_DATA_DIR(cls) -> Path:
        """测试数据目录"""
        dir_name = _config.get('DATA', 'TEST_DATA_DIR', 'data')
        return Path(__file__).parent.parent / dir_name

    @classmethod
    @property
    def USER_DATA_FILE(cls) -> str:
        return _config.get('DATA', 'USER_DATA_FILE', 'user_data.xlsx')

    @classmethod
    @property
    def ORDER_DATA_FILE(cls) -> str:
        return _config.get('DATA', 'ORDER_DATA_FILE', 'order_data.xlsx')

    # ==================== 性能配置 ====================

    @classmethod
    @property
    def CONCURRENT_USERS(cls) -> int:
        return _config.get_int('PERFORMANCE', 'CONCURRENT_USERS', 10)

    @classmethod
    @property
    def LOOP_COUNT(cls) -> int:
        return _config.get_int('PERFORMANCE', 'LOOP_COUNT', 100)

    # ==================== 工具方法 ====================

    @classmethod
    def get_auth_credentials(cls) -> Dict[str, str]:
        """获取认证凭证"""
        auth_type = cls.AUTH_TYPE
        if auth_type == 'basic':
            return {
                'username': cls.AUTH_USERNAME,
                'password': cls.AUTH_PASSWORD
            }
        elif auth_type == 'bearer':
            return {'token': cls.BEARER_TOKEN}
        elif auth_type == 'api_key':
            return {'key': 'X-API-Key', 'value': cls.API_KEY}
        return {}

    @classmethod
    def switch_env(cls, env: str):
        """切换环境（用于运行时动态切换）"""
        _config.set_env(env)

    @classmethod
    def get_env_info(cls) -> Dict[str, str]:
        """获取当前环境信息"""
        return {
            'environment': cls.CURRENT_ENV,
            'base_url': cls.BASE_URL,
            'timeout': cls.TIMEOUT,
            'log_level': cls.LOG_LEVEL
        }


# 导出配置实例，方便使用
config = Config