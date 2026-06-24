# config/config_reader.py
import os
import configparser
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigReader:
    """配置文件读取器 - 单例模式"""

    _instance = None
    _config = None

    def __new__(cls):
        """单例模式：确保全局只有一个配置实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化配置读取器"""
        if self._config is None:
            self._load_config()

    def _load_config(self):
        """加载配置文件"""
        self._config = configparser.ConfigParser()

        # 配置文件路径
        config_dir = Path(__file__).parent
        config_file = config_dir / 'config.ini'

        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")

        # 读取配置文件
        self._config.read(config_file, encoding='utf-8')

        # 设置当前环境
        self.current_env = self._config.get('ENV', 'CURRENT_ENV', fallback='test')

        # 验证环境配置是否存在
        if self.current_env not in self._config.sections():
            raise ValueError(f"配置文件中不存在环境: {self.current_env}")

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """获取配置项的值"""
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_int(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        """获取整型配置项"""
        try:
            return self._config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_boolean(self, section: str, key: str, fallback: Optional[bool] = None) -> bool:
        """获取布尔型配置项"""
        try:
            return self._config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_float(self, section: str, key: str, fallback: Optional[float] = None) -> float:
        """获取浮点型配置项"""
        try:
            return self._config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_env_value(self, key: str, fallback: Optional[str] = None) -> str:
        """获取当前环境下的配置值"""
        return self.get(self.current_env, key, fallback)

    def get_env_int(self, key: str, fallback: Optional[int] = None) -> int:
        """获取当前环境下的整型配置值"""
        return self.get_int(self.current_env, key, fallback)

    def get_env_bool(self, key: str, fallback: Optional[bool] = None) -> bool:
        """获取当前环境下的布尔型配置值"""
        return self.get_boolean(self.current_env, key, fallback)

    def get_section(self, section: str) -> Dict[str, str]:
        """获取整个配置节"""
        if section not in self._config:
            return {}
        return dict(self._config.items(section))

    def get_env_section(self) -> Dict[str, str]:
        """获取当前环境的所有配置"""
        return self.get_section(self.current_env)

    def set_env(self, env: str):
        """切换环境"""
        if env not in self._config.sections():
            raise ValueError(f"无效的环境: {env}")
        self.current_env = env

    def get_all_envs(self) -> list:
        """获取所有可用的环境列表"""
        # 排除非环境配置节
        exclude_sections = ['ENV', 'AUTH', 'DATABASE', 'REPORT', 'LOG',
                            'HEADERS', 'DATA', 'PERFORMANCE']
        return [s for s in self._config.sections() if s not in exclude_sections]


# 全局配置实例
config = ConfigReader()