# config/config.py
import configparser
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """
    配置类 - 单例模式，统一管理所有配置
    支持多环境、多服务配置
    """
    _instance = None
    _config = None
    current_env = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        """加载配置文件"""
        config_dir = Path(__file__).parent
        config_file = config_dir / 'config.ini'

        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")

        self._config = configparser.ConfigParser()
        self._config.read(config_file, encoding='utf-8')
        self.current_env = self._config.get('ENV', 'CURRENT_ENV', fallback='TEST')

    # ===== 通用读取方法 =====
    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """获取配置值"""
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_int(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        try:
            return self._config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_bool(self, section: str, key: str, fallback: Optional[bool] = None) -> bool:
        try:
            return self._config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_env(self, key: str, fallback: Optional[str] = None) -> str:
        """获取当前环境配置"""
        return self.get(self.current_env, key, fallback)

    def get_env_int(self, key: str, fallback: Optional[int] = None) -> int:
        return self.get_int(self.current_env, key, fallback)

    def get_env_dict(self) -> Dict[str, str]:
        """获取当前环境所有配置"""
        return dict(self._config.items(self.current_env))

    def set_env(self, env: str):
        """切换环境"""
        if env not in self._config.sections():
            raise ValueError(f"无效环境: {env}，可用环境: {self.get_available_envs()}")
        self.current_env = env

    def get_available_envs(self) -> list:
        """获取所有可用环境"""
        exclude = ['ENV', 'AUTH', 'DATABASE', 'REPORT', 'LOG', 'HEADERS']
        return [s for s in self._config.sections() if s not in exclude]

    # ===================================  ===================================
    # ===== API 配置 =====
    def get_api_base_url(self) -> str:
        return self.get(f"{self.current_env.upper()}", 'BASE_URL')

    def get_api_timeout(self) -> int:
        return self.get_int(f"{self.current_env.upper()}", 'TIMEOUT', 30)

    def get_api_token(self) -> str:
        return self.get(f"{self.current_env.upper()}", 'TOKEN', '')

    def get_api_log_level(self) -> str:
        return self.get(f"{self.current_env.upper()}", 'LOG_LEVEL', 'INFO')

    # ===== UI 配置 =====
    def get_ui_base_url(self) -> str:
        return self.get(f"{self.current_env.upper()}_UI", 'BASE_URL')

    def get_ui_username(self) -> str:
        return self.get(f"{self.current_env.upper()}_UI", 'USERNAME', '')

    def get_ui_password(self) -> str:
        return self.get(f"{self.current_env.upper()}_UI", 'PASSWORD', '')

    def get_ui_headless(self) -> bool:
        return self.get_bool(f"{self.current_env.upper()}_UI", 'HEADLESS', False)

    def get_ui_timeout(self) -> int:
        return self.get_int(f"{self.current_env.upper()}_UI", 'TIMEOUT', 30000)

    # ===== 数据库配置 =====
    def get_db_config(self) -> dict:
        return {
            'host': self.get('DATABASE', 'DB_HOST', 'localhost'),
            'port': self.get_int('DATABASE', 'DB_PORT', 3306),
            'user': self.get('DATABASE', 'DB_USER', ''),
            'password': self.get('DATABASE', 'DB_PASSWORD', ''),
            'database': self.get('DATABASE', 'DB_NAME', ''),
        }


    # ====================================== 环境配置 ===================================
    @property
    def CURRENT_ENV(self) -> str:
        return self.current_env

    @property
    def BASE_HOST(self) -> str:
        return self.get_env('BASE_HOST')

    @property
    def TIMEOUT(self) -> int:
        return self.get_env_int('TIMEOUT', 30)

    @property
    def MAX_RETRIES(self) -> int:
        return self.get_env_int('MAX_RETRIES', 3)

    @property
    def LOG_LEVEL(self) -> str:
        return self.get_env('LOG_LEVEL', 'INFO')

    # ===================================== 服务端口配置 ===================================
    @property
    def PORT_MODEL_SERVICE(self) -> int:
        return self.get_env_int('PORT_MODEL_SERVICE', 30071)

    @property
    def PORT_VALID_SERVICE(self) -> int:
        return self.get_env_int('PORT_VALID_SERVICE', 31053)

    @property
    def PORT_DATA_COMMIT_STORE_SERVICE(self) -> int:
        return self.get_env_int('PORT_DATA_COMMIT_STORE_SERVICE', 31360)

    @property
    def PORT_GENERATE_PACKAGE_NO(self) -> int:
        return self.get_env_int('PORT_GENERATE_PACKAGE_NO', 31100)


    # ===================================== 服务URL ===================================
    @property
    def MODEL_SERVICE_URL(self) -> str:
        return f"http://{self.BASE_HOST}:{self.PORT_MODEL_SERVICE}"

    @property
    def VALID_SERVICE_URL(self) -> str:
        return f"http://{self.BASE_HOST}:{self.PORT_VALID_SERVICE}"

    @property
    def DATA_COMMIT_STORE_SERVICE_URL(self) -> str:
        return f"http://{self.BASE_HOST}:{self.PORT_DATA_COMMIT_STORE_SERVICE}"

    @property
    def GENERATE_PACKAGE_NO_URL(self) -> str:
        return f"http://{self.BASE_HOST}:{self.PORT_GENERATE_PACKAGE_NO}"


    @property
    def SERVICE_PORTS(self) -> Dict[str, int]:
        """所有服务端口映射"""
        return {
            'model': self.PORT_MODEL_SERVICE,
            'valid': self.PORT_VALID_SERVICE,
            'datacommitstore': self.PORT_DATA_COMMIT_STORE_SERVICE,
            'generatepackageno': self.PORT_GENERATE_PACKAGE_NO,
        }

    @property
    def SERVICE_URLS(self) -> Dict[str, str]:
        """所有服务URL映射"""
        return {
            'model': self.MODEL_SERVICE_URL,
            'valid': self.VALID_SERVICE_URL,
            'datacommitstore': self.DATA_COMMIT_STORE_SERVICE_URL,
            'generatepackageno': self.GENERATE_PACKAGE_NO_URL
        }

    def get_service_url(self, service_name: str) -> str:
        """获取指定服务的URL"""
        service_name = service_name.lower()
        urls = self.SERVICE_URLS
        if service_name not in urls:
            raise ValueError(f"未知服务: {service_name}，可用服务: {list(urls.keys())}")
        return urls[service_name]

    def get_service_port(self, service_name: str) -> int:
        """获取指定服务的端口"""
        service_name = service_name.lower()
        ports = self.SERVICE_PORTS
        if service_name not in ports:
            raise ValueError(f"未知服务: {service_name}，可用服务: {list(ports.keys())}")
        return ports[service_name]

    # ===== 认证配置 =====
    @property
    def AUTH_TYPE(self) -> str:
        return self.get('AUTH', 'DEFAULT_AUTH_TYPE', 'bearer')

    @property
    def AUTH_USERNAME(self) -> str:
        return self.get('AUTH', 'TEST_USERNAME', '')

    @property
    def AUTH_PASSWORD(self) -> str:
        return self.get('AUTH', 'TEST_PASSWORD', '')

    @property
    def BEARER_TOKEN(self) -> str:
        return self.get('AUTH', 'BEARER_TOKEN', '')

    @property
    def API_KEY(self) -> str:
        return self.get('AUTH', 'API_KEY', '')

    def get_auth_credentials(self) -> dict:
        """获取认证凭证"""
        auth_type = self.AUTH_TYPE
        if auth_type == 'basic':
            return {'username': self.AUTH_USERNAME, 'password': self.AUTH_PASSWORD}
        elif auth_type == 'bearer':
            return {'token': self.BEARER_TOKEN}
        elif auth_type == 'api_key':
            return {'key': 'X-API-Key', 'value': self.API_KEY}
        return {}

    # ===== 数据库配置 =====
    @property
    def DB_HOST(self) -> str:
        return self.get('DATABASE', 'DB_HOST', 'localhost')

    @property
    def DB_PORT(self) -> int:
        return self.get_int('DATABASE', 'DB_PORT', 3306)

    @property
    def DB_USER(self) -> str:
        return self.get('DATABASE', 'DB_USER', '')

    @property
    def DB_PASSWORD(self) -> str:
        return self.get('DATABASE', 'DB_PASSWORD', '')

    @property
    def DB_NAME(self) -> str:
        return self.get('DATABASE', 'DB_NAME', '')

    def get_db_config(self) -> dict:
        """获取数据库完整配置"""
        return {
            'host': self.DB_HOST,
            'port': self.DB_PORT,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'database': self.DB_NAME,
        }

    # ===== 目录配置 =====
    @property
    def REPORT_DIR(self) -> Path:
        return Path(__file__).parent.parent / self.get('REPORT', 'REPORT_DIR', 'report')

    @property
    def LOG_DIR(self) -> Path:
        return Path(__file__).parent.parent / self.get('LOG', 'LOG_DIR', 'log')

    @property
    def REPORT_NAME(self) -> str:
        return self.get('REPORT', 'REPORT_NAME', 'test_report.html')

    @property
    def LOG_FILE(self) -> str:
        return self.get('LOG', 'LOG_FILE', 'test.log')

    # ===== 请求头配置 =====
    @property
    def USER_AGENT(self) -> str:
        return self.get('HEADERS', 'USER_AGENT', 'Pytest-AutoTest/1.0')

    @property
    def ACCEPT(self) -> str:
        return self.get('HEADERS', 'ACCEPT', 'application/json')

    # ===== 工具方法 =====
    def get_env_info(self) -> dict:
        """获取当前环境信息"""
        return {
            'environment': self.current_env,
            'host': self.BASE_HOST,
            'timeout': self.TIMEOUT,
            'max_retries': self.MAX_RETRIES,
            'log_level': self.LOG_LEVEL,
            'services': self.SERVICE_PORTS,
            'service_urls': self.SERVICE_URLS,
        }

    # def get_env_info(self) -> dict:
    # """获取环境信息"""
    #     return {
    #         'environment': self.current_env,
    #         'api_base_url': self.get_api_base_url(),
    #         'ui_base_url': self.get_ui_base_url(),
    #         'timeout': self.get_api_timeout(),
    #     }

    def show_config(self):
        """显示所有配置信息"""
        print("=" * 70)
        print("  📋 接口自动化测试框架 - 配置信息")
        print("=" * 70)

        print(f"\n【环境】: {self.current_env}")
        print(f"【主机】: {self.BASE_HOST}")
        print(f"【超时】: {self.TIMEOUT}s")
        print(f"【重试】: {self.MAX_RETRIES}次")
        print(f"【日志】: {self.LOG_LEVEL}")

        print("\n【服务端口及URL】")
        for service, port in self.SERVICE_PORTS.items():
            url = f"http://{self.BASE_HOST}:{port}"
            print(f"  {service:12} -> {port}  ({url})")

        print("\n【认证配置】")
        print(f"  认证类型: {self.AUTH_TYPE}")
        if self.AUTH_TYPE == 'basic':
            print(f"  用户名:   {self.AUTH_USERNAME}")
            print(f"  密码:     {'*' * len(self.AUTH_PASSWORD)}")
        elif self.AUTH_TYPE == 'bearer':
            token = self.BEARER_TOKEN
            print(f"  Token:    {token[:15] + '...' if len(token) > 15 else token}")
        elif self.AUTH_TYPE == 'api_key':
            key = self.API_KEY
            print(f"  API Key:  {key[:15] + '...' if len(key) > 15 else key}")

        print("\n【数据库配置】")
        print(f"  主机:     {self.DB_HOST}")
        print(f"  端口:     {self.DB_PORT}")
        print(f"  用户:     {self.DB_USER}")
        print(f"  数据库:   {self.DB_NAME}")

        print("\n【目录配置】")
        print(f"  报告目录: {self.REPORT_DIR}")
        print(f"  日志目录: {self.LOG_DIR}")

        print("\n【可用环境】")
        for env in self.get_available_envs():
            marker = "✅" if env == self.current_env else "  "
            print(f"  {marker} {env}")

        print("\n" + "=" * 70)
        print("💡 提示:")
        print("   1. 修改 config/config.ini 中的 CURRENT_ENV 切换环境")
        print("   2. 运行: pytest --env staging 指定环境运行测试")
        print("   3. 使用: config.get_service_url('order') 获取服务URL")
        print("=" * 70)


# 全局配置实例
config = Config()

if __name__ == '__main__':
    # 显示配置信息
    config.show_config()

    # 测试服务URL获取
    print("\n【测试服务URL获取】")
    for service in ['model', 'valid', 'datacommitstore']:
        url = config.get_service_url(service)
        port = config.get_service_port(service)
        print(f"  {service}: {url} (端口: {port})")