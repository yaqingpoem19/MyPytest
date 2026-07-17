import pytest
import logging
import json
from pathlib import Path
from utils.operationExcel import OperationExcel
import requests

logger = logging.getLogger(__name__)

def get_project_codes():
    """从Excel获取项目代码列表"""
    try:
        excel = OperationExcel("F:/测试文件/test.xlsx")
        data = excel.get_data()
        # 提取 projectCode 字段
        codes = []
        for item in data:
            code = item.get('ProjectCode') or item.get('projectCode')
            if code:
                codes.append(code)
        return codes if codes else ["DM_fuqing_test01"]
    except Exception as e:
        logger.error(f"加载Excel数据失败: {e}")
        return ["DM_fuqing_test01"]


def build_payload(self, projectCode: str, package_no: str) -> dict:
    """
    构建主接口的请求体
    """
    return {
        "projectCode": projectCode,
        "packageCode": package_no,
        "owner": "sun",
        "instances": [{
            "objectModelCode": "OTHER_INFO01",
            "version": "",
            "attributes": [{
                "attributeModelCode": "STUCB1",
                "value": "STUCB1_0001"
            }]
        }]
    }

def generate_package_no(projectCode) -> str:
    """
    调用生成包号接口，获取 packageCode
    """
    url = "http://192.168.6.190:31100/v1.0/datasync/id/generatePackageNo"
    payload = [{"projectCode": projectCode}]
    headers = ({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    })
    try:
        response = requests.post(url, json=payload, headers=headers).json()
        print(f"【依赖接口-包号生成】响应结果: {response['data']}")
        return response['data']
    except Exception as e:
        logger.error(f"【依赖接口】请求异常: {e}")
        return None


if __name__ == '__main__':
    print("111" * 30)
    projects = get_project_codes()
    for project in projects:
        print("222" * 30)
        print(project)
        print("333" * 30)
        print(generate_package_no(project))

