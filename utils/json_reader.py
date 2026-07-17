# utils/json_reader.py
import json
from pathlib import Path
from typing import Dict, Any, Optional
from common.logger import get_logger
from common.exceptions import DataError

logger = get_logger("JsonReader")


class JsonReader:
    """JSON 读取器"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise DataError(f"JSON文件不存在: {file_path}")

    def get_data(self) -> Dict[str, Any]:
        """读取JSON数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"读取JSON成功: {self.file_path}")
            return data
        except Exception as e:
            logger.error(f"读取JSON失败: {e}")
            raise DataError(f"读取JSON失败: {e}")

    def get_value(self, key: str, default: Any = None) -> Any:
        """获取指定键的值"""
        data = self.get_data()
        logger.info(f"获取JSON中的key值: {key}")
        return data.get(key, default)

    @staticmethod
    def save_data(data: Dict[str, Any], file_path: str):
        """保存JSON数据"""
        path = Path(file_path)
        path.parent.mkdir(exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"保存JSON成功: {file_path}")



if __name__ == '__main__':
    reader = JsonReader("F:/中科院空间技术航天项目资料/全量人员信息简化.txt")
    print(reader.get_data())
    print(reader.get_value('email'))