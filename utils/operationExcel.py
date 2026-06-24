# 基础的读取Excel文件方法
import openpyxl

class OperationExcel:
    def __init__(self, file_path, sheet_name="Sheet1"):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def get_data(self):
        """获取所有行数据，返回列表，每行是一个字典"""
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[self.sheet_name]
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return []
        # 第一行作为表头
        keys = rows[0]
        result = []
        for row in rows[1:]:
            # 过滤掉全空的行
            if any(cell is not None for cell in row):
                row_dict = dict(zip(keys, row))
                result.append(row_dict)
        return result