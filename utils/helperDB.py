
from typing import Dict, List, Any, Optional
from common.logger import get_logger
from common.exceptions import AutoTestException
from config.config import config
import pymysql

logger = get_logger("DatabaseHelper")


class DatabaseHelper:
    """数据库操作辅助类"""

    def __init__(self, db_config: Optional[Dict] = None):
        self.db_config = db_config or config.get_db_config()
        self.connection = None

    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                charset='utf8mb4'
            )
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise AutoTestException(f"数据库连接失败: {e}")

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict]:
        """执行查询"""
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, params or ())
            result = cursor.fetchall()
            cursor.close()
            logger.debug(f"查询成功: {sql}")
            return result
        except Exception as e:
            logger.error(f"查询失败: {e}")
            raise AutoTestException(f"查询失败: {e}")

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行更新"""
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            affected = cursor.execute(sql, params or ())
            self.connection.commit()
            cursor.close()
            logger.debug(f"更新成功: {sql}, 影响行数: {affected}")
            return affected
        except Exception as e:
            self.connection.rollback()
            logger.error(f"更新失败: {e}")
            raise AutoTestException(f"更新失败: {e}")

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()