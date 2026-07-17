# common/logger.py
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class LoggerManager:
    """统一日志管理器"""

    _loggers = {}
    _log_dir = Path("logs")

    @classmethod
    def get_logger(cls, name: str, level: str = "INFO") -> logging.Logger:
        """获取日志记录器; cls代表‌被调用的当前类本身（类对象），用于访问类属性、调用其他类方法或实例化对象;无需实例化即可调用"""
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        if logger.handlers:
            return logger

        cls._log_dir.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台输出
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

        # 文件输出
        log_file = cls._log_dir / f"{datetime.now().strftime('%Y%m%d')}_{name}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger


def get_logger(name: str = "AutoTest", level: str = "INFO") -> logging.Logger:
    """便捷获取日志记录器"""
    return LoggerManager.get_logger(name, level)