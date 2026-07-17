# 基础的读取Excel文件方法
import openpyxl
from pathlib import Path
from typing import List, Dict, Any, Optional
from common.exceptions import DataError
from common.logger import get_logger

logger = get_logger("OperationExcel")

class OperationExcel:
    def __init__(self, file_path, sheet_name="Sheet1"):
        self.file_path = file_path
        self.sheet_name = sheet_name

        if not self.file_path.exists():
            raise DataError(f"Excel文件不存在: {file_path}")

    def get_data(self):
        """读取Excel所有行数据，返回字典列表，每行是一个字典"""
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[self.sheet_name]
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return []
        # 第一行作为表头
        keys = [str(h) if h else f"col_{i}" for i, h in enumerate(rows[0])]
        result = []
        for row in rows[1:]:
            # 过滤掉全空的行
            if any(cell is not None for cell in row):
                row_dict = dict(zip(keys, row))
                # row_dict = {}
                # for i, key in enumerate(keys):
                #     row_dict[key] = row[i] if i < len(row) else None
                result.append(row_dict)

        logger.info(f"读取Excel成功: {len(result)} 行")
        return result

    def get_column(self, column_name: str) -> List[Any]:
        """获取指定列数据"""
        data = self.get_data()
        return [row.get(column_name) for row in data if column_name in row]

    def get_row(self, row_index: int) -> Dict[str, Any]:
        """获取指定行数据"""
        data = self.get_data()
        if 0 <= row_index < len(data):
            return data[row_index]
        return {}


if __name__ == '__main__':
    myexcel = OperationExcel("F:/测试文件/test.xlsx")
    print(f'读取excel文件表数据：')
    print('*' * 50)
    print(myexcel.get_data())