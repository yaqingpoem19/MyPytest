# common/logger.py
import logging
import sys
from pathlib import Path


def get_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """获取日志记录器"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper()))

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # 文件处理器
        log_dir = Path(__file__).parent.parent / 'log'
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / 'test.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger