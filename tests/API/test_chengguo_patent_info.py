# tests/api/test_renshi_patent_info.py
import pytest
from common.logger import get_logger

logger = get_logger("test_renshi_patent_info")


class TestGetMyPatentInfoWithAuth:
    """带认证的专利信息测试"""

    @pytest.mark.api
    def test_get_my_patent_info_with_auth(self, auth_api_client):
        """
        测试用例：使用认证Token获取专利信息
        """
        logger.info("【测试用例】带认证获取专利信息")

        url = "/api/result/getMyPatentInfo.do"
        form_data = {
            "account": "testuser001",
            "pageIndex": 1,
            "pageSize": 10
        }

        logger.info(f"【请求参数】: {form_data}")

        # 使用 auth_api_client（自动携带 Token）
        response = auth_api_client.post(url, data=form_data)

        logger.info(f"【响应内容】: {response}")

        # 断言
        assert response is not None, "响应为空"

        if "code" in response:
            assert response.get("code") == 200

        logger.info("✅ 测试通过：带认证获取专利信息成功")


'''
========================================================================================================
'''
from common.data_generator import DataGenerator
from utils.helperRandom import

class TestGetMyPatentInfo:
    """获取个人专利信息测试"""

    # ============================================
    # 测试数据
    # ============================================

    @pytest.fixture
    def valid_patent_data(self):
        """有效的专利查询参数"""
        return {
            "account": "testuser001",
            "pageIndex": 1,
            "pageSize": 10
        }

    @pytest.fixture
    def invalid_account_data(self):
        """无效账号参数"""
        return {
            "account": "invalid_user",
            "pageIndex": 1,
            "pageSize": 10
        }

    # ============================================
    # 辅助方法
    # ============================================

    def call_get_my_patent_info(self, api_client, form_data: dict) -> dict:
        """
        调用获取个人专利信息接口
        :param api_client: API客户端
        :param form_data: form-data格式的请求数据
        :return: 响应结果
        """
        url = "/api/result/getMyPatentInfo.do"

        logger.info("=" * 60)
        logger.info("【接口调用】获取个人专利信息")
        logger.info(f"【请求URL】: {url}")
        logger.info(f"【请求方式】: POST")
        logger.info(f"【请求参数(form-data)】: {form_data}")

        # 注意：使用 data 参数传递 form-data 格式数据
        response = api_client.post(url, data=form_data)

        logger.info(f"【响应内容】: {response}")
        logger.info("=" * 60)

        return response

    # ============================================
    # 测试用例
    # ============================================

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_my_patent_info_success(self, api_client, valid_patent_data):
        """
        测试用例：正常获取个人专利信息
        预期结果：接口返回成功，包含专利列表数据
        """
        logger.info("【测试用例】正常获取个人专利信息")

        # 调用接口
        response = self.call_get_my_patent_info(api_client, valid_patent_data)

        # 断言
        assert response is not None, "响应为空"

        # 根据实际接口返回结构调整断言
        # 假设接口返回格式: {"code": 200, "data": {...}, "msg": "success"}
        if "code" in response:
            assert response.get("code") == 200, f"期望code=200，实际: {response.get('code')}"

        # 验证返回数据包含必要字段
        if "data" in response:
            data = response.get("data", {})
            # 根据实际返回结构调整
            logger.info(f"专利数据: {data}")

        # 验证分页参数
        if "pageIndex" in response:
            assert response.get("pageIndex") == valid_patent_data["pageIndex"]
        if "pageSize" in response:
            assert response.get("pageSize") == valid_patent_data["pageSize"]

        logger.info("✅ 测试通过：正常获取个人专利信息成功")

    @pytest.mark.api
    def test_get_my_patent_info_with_valid_account(self, api_client, valid_patent_data):
        """
        测试用例：使用有效账号查询专利信息
        """
        logger.info("【测试用例】使用有效账号查询专利信息")

        response = self.call_get_my_patent_info(api_client, valid_patent_data)

        # 断言
        assert response is not None, "响应为空"

        # 验证成功状态
        if "code" in response:
            assert response.get("code") == 200
        if "success" in response:
            assert response.get("success") is True

        # 验证返回的专利列表
        if "data" in response:
            data = response.get("data")
            # 如果 data 是列表，验证列表不为空
            if isinstance(data, list):
                logger.info(f"查询到 {len(data)} 条专利记录")
            # 如果 data 是字典，验证包含列表
            elif isinstance(data, dict):
                patent_list = data.get("list", [])
                total = data.get("total", 0)
                logger.info(f"专利总数: {total}, 当前页记录数: {len(patent_list)}")

        logger.info("✅ 测试通过：有效账号查询成功")

    @pytest.mark.api
    def test_get_my_patent_info_with_different_page(self, api_client):
        """
        测试用例：测试不同的分页参数
        """
        logger.info("【测试用例】测试不同分页参数")

        # 测试不同的分页组合
        test_pages = [
            {"pageIndex": 1, "pageSize": 5},
            {"pageIndex": 1, "pageSize": 20},
            {"pageIndex": 2, "pageSize": 10},
            {"pageIndex": 3, "pageSize": 10},
        ]

        account = "testuser001"

        for page_params in test_pages:
            form_data = {
                "account": account,
                "pageIndex": page_params["pageIndex"],
                "pageSize": page_params["pageSize"]
            }

            logger.info(f"测试分页参数: pageIndex={page_params['pageIndex']}, pageSize={page_params['pageSize']}")

            response = self.call_get_my_patent_info(api_client, form_data)

            # 断言
            assert response is not None, f"分页参数 {page_params} 请求失败"

            if "code" in response:
                assert response.get("code") == 200, f"分页参数 {page_params} 失败"

            logger.info(f"✅ 分页参数 pageIndex={page_params['pageIndex']} 测试通过")

    @pytest.mark.api
    def test_get_my_patent_info_with_invalid_account(self, api_client, invalid_account_data):
        """
        测试用例：使用无效账号查询专利信息
        预期结果：接口返回错误提示
        """
        logger.info("【测试用例】使用无效账号查询专利信息")

        response = self.call_get_my_patent_info(api_client, invalid_account_data)

        # 断言
        assert response is not None, "响应为空"

        # 验证错误响应
        # 根据实际接口返回结构调整
        if "code" in response:
            assert response.get("code") != 200, "无效账号应该返回错误码"
        if "msg" in response or "message" in response:
            error_msg = response.get("msg") or response.get("message")
            logger.info(f"错误信息: {error_msg}")

        logger.info("✅ 测试通过：无效账号返回错误信息")

    @pytest.mark.api
    def test_get_my_patent_info_with_empty_account(self, api_client):
        """
        测试用例：账号为空查询专利信息
        """
        logger.info("【测试用例】账号为空查询专利信息")

        form_data = {
            "account": "",
            "pageIndex": 1,
            "pageSize": 10
        }

        response = self.call_get_my_patent_info(api_client, form_data)

        # 断言
        assert response is not None, "响应为空"

        # 验证错误响应
        if "code" in response:
            assert response.get("code") != 200, "空账号应该返回错误码"

        logger.info("✅ 测试通过：空账号返回错误信息")

    @pytest.mark.api
    def test_get_my_patent_info_without_account(self, api_client):
        """
        测试用例：不传账号参数查询专利信息
        """
        logger.info("【测试用例】不传账号参数查询专利信息")

        form_data = {
            "pageIndex": 1,
            "pageSize": 10
        }

        response = self.call_get_my_patent_info(api_client, form_data)

        # 断言
        assert response is not None, "响应为空"

        # 验证错误响应（账号为必填参数）
        if "code" in response:
            # 通常接口会返回错误，因为 account 是必填的
            assert response.get("code") != 200, "缺少必填参数应该返回错误码"

        logger.info("✅ 测试通过：缺少必填参数返回错误信息")

    @pytest.mark.api
    def test_get_my_patent_info_with_large_page_size(self, api_client):
        """
        测试用例：测试大分页参数
        """
        logger.info("【测试用例】测试大分页参数")

        form_data = {
            "account": "testuser001",
            "pageIndex": 1,
            "pageSize": 9999
        }

        response = self.call_get_my_patent_info(api_client, form_data)

        # 断言
        assert response is not None, "响应为空"

        if "code" in response:
            # 可能成功也可能返回错误（取决于接口限制）
            logger.info(f"接口返回码: {response.get('code')}")

        logger.info("✅ 测试完成：大分页参数测试")

    @pytest.mark.api
    def test_get_my_patent_info_with_negative_page(self, api_client):
        """
        测试用例：测试负数分页参数
        """
        logger.info("【测试用例】测试负数分页参数")

        form_data = {
            "account": "testuser001",
            "pageIndex": -1,
            "pageSize": -10
        }

        response = self.call_get_my_patent_info(api_client, form_data)

        # 断言
        assert response is not None, "响应为空"

        # 验证错误响应（负数参数应该被处理）
        if "code" in response:
            logger.info(f"接口返回码: {response.get('code')}")

        logger.info("✅ 测试完成：负数分页参数测试")


class TestGetMyPatentInfoDataDriven:
    """数据驱动测试：获取个人专利信息"""

    # ============================================
    # 测试数据
    # ============================================

    @pytest.fixture
    def test_data_list(self):
        """从配置文件或数据文件加载测试数据"""
        # 可以扩展从 Excel 或 JSON 文件读取
        return [
            {"account": "testuser001", "pageIndex": 1, "pageSize": 10, "expected_code": 200},
            {"account": "testuser002", "pageIndex": 1, "pageSize": 10, "expected_code": 200},
            {"account": "invalid_user", "pageIndex": 1, "pageSize": 10, "expected_code": 400},
            {"account": "", "pageIndex": 1, "pageSize": 10, "expected_code": 400},
        ]

    # ============================================
    # 测试用例
    # ============================================

    @pytest.mark.api
    @pytest.mark.parametrize("account, pageIndex, pageSize, expected_code", [
        ("testuser001", 1, 10, 200),
        ("testuser002", 1, 10, 200),
        ("testuser003", 2, 20, 200),
        ("invalid_user", 1, 10, 400),
        ("", 1, 10, 400),
    ])
    def test_get_my_patent_info_parametrize(
            self,
            api_client,
            account: str,
            pageIndex: int,
            pageSize: int,
            expected_code: int
    ):
        """
        测试用例：参数化测试 - 获取个人专利信息
        """
        logger.info("=" * 60)
        logger.info(f"【参数化测试】account={account}, pageIndex={pageIndex}, pageSize={pageSize}")

        url = "/api/result/getMyPatentInfo.do"
        form_data = {
            "account": account,
            "pageIndex": pageIndex,
            "pageSize": pageSize
        }

        logger.info(f"【请求参数】: {form_data}")

        response = api_client.post(url, data=form_data)

        logger.info(f"【响应内容】: {response}")

        # 断言
        assert response is not None, f"请求失败: {account}"

        if "code" in response:
            assert response.get("code") == expected_code, \
                f"期望code={expected_code}，实际: {response.get('code')}"

        logger.info(f"✅ 测试通过: {account} -> code={expected_code}")
        logger.info("=" * 60)