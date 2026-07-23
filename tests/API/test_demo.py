import pytest
import logging
import json
from pathlib import Path
from utils.operationExcel import OperationExcel
import requests

logger = logging.getLogger(__name__)


# class TestModelService:
#     """模型服务测试"""
#
#     @pytest.mark.parametrize("projectCode,oid", [("DM_fuqing_test01", "DM_fuqing_test01")])
#     def test_get_tree(self, model_client,projectCode, oid):
#         """测试获取树结构"""
#         url = "/modelobjservice/v1.0/objrelationsvr/objectrelation/tree"
#         params = {"projectCode":projectCode,"oid":oid}
#
#         response = model_client.get(url, params=params)
#         logger.info(f"响应: {response}")
#
#         assert response.get("total") == 2
#         logger.info("✅ 获取树结构测试通过")


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


class TestGeneratePackageNo:
    """根据项目代号生成包号"""
    _url = "/v1.0/datasync/id/generatePackageNo"

    @pytest.mark.parametrize("projectCode", ["DM_fuqing_test01"])
    def test_generate_package_no(self, packageno_client, projectCode) -> str:
        """
        调用生成包号接口，获取 packageCode
        """
        # url = "/v1.0/datasync/id/generatePackageNo"
        payload = {"projectCode": projectCode}
        print("11" *30)
        response = packageno_client.post(self._url, json_data = payload)
        package_no = response["data"]
        print(f"【依赖接口-包号生成】响应结果: {response}")
        print(f"【依赖接口】获取到 packageCode: {package_no}")

        assert response is not None, f"生成包号接口调用失败，response: {response}"
        assert package_no != "", "生成的 package_no 为空"

        return package_no

# class TestValidService:
#     """提资数据校验服务测试"""
    # def build_payload(self, projectCode: str, package_no: str) -> dict:
    #     """
    #     构建主接口的请求体
    #     """
    #     return {
    #         "projectCode": projectCode,
    #         "packageCode": package_no,
    #         "owner": "sun",
    #         "instances": [{
    #             "objectModelCode": "OTHER_INFO01",
    #             "version": "",
    #             "attributes": [{
    #                 "attributeModelCode": "STUCB1",
    #                 "value": "STUCB1_0001"
    #             }]
    #         }]
    #     }
    #
    # # @pytest.mark.parametrize("projectCode", get_project_codes())
    # @pytest.mark.parametrize("projectCode", ["DM_fuqing_test01", ])
    # def test_valid_service(self, valid_client, packageno_client, projectCode):
    #     """测试提资数据校验服务"""
    #     print("=" * 60)
    #     print(f"【测试开始】项目代码: {projectCode}")
    #     print("=" * 60)
    #
    #     # ===== 步骤1：调用依赖接口，生成 packageNo =====
    #     package_no = self.generate_package_no(packageno_client, projectCode)
    #     # 断言依赖接口返回成功
    #     print(f'包号生成接口调用返回结果：{package_no}')
    #     # assert package_no is not None, f"生成包号失败，projectCode: {projectCode}"
    #     assert package_no != "", "生成的 packageCode 为空"
    #
    #     # ===== 步骤2：调用主测试接口 =====
    #     # 使用生成的 packageCode 作为参数
    #     url = f"/valid/instance/{projectCode}/sun"
    #     payload = self.build_payload(projectCode, package_no)
    #     logger.info(f"【步骤2】请求URL: {url}")
    #     logger.info(f"【步骤2】请求参数: {payload}")
    #
    #     response = valid_client.post(url, payload)
    #
    #     assert response.get("code") == 200
    #     logger.info("✅ 获取产品列表测试通过")
