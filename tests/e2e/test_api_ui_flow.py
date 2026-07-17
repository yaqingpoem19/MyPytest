# tests/e2e/test_api_ui_flow.py
import pytest
from common.logger import get_logger
from utils.helperRandom import DataGenerator
from config.config import config

logger = get_logger("test_api_ui_flow")


class TestAPIUIFlow:
    """API + UI 端到端测试"""

    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_user_lifecycle(self, auth_api_client, login_page):
        """
        用户完整生命周期测试：
        1. API创建用户
        2. UI验证用户存在
        3. API删除用户
        4. UI验证用户已删除
        """
        # ===== 步骤1：API创建用户 =====
        user_data = DataGenerator.generate_user_data()
        username = user_data["username"]

        logger.info("=" * 60)
        logger.info(f"步骤1: API创建用户 {username}")
        create_resp = auth_api_client.post("/api/users", json_data=user_data)
        assert create_resp.get("code") == 200
        user_id = create_resp.get("data", {}).get("id")
        logger.info(f"  ✅ 用户创建成功: ID={user_id}")

        # ===== 步骤2：UI验证用户 =====
        logger.info("步骤2: UI验证用户存在")
        home_page = login_page.login("admin", "admin123")
        user_page = home_page.navigate_to_user_page()
        user_page.search_user(username)

        assert user_page.get_user_count() >= 1, f"UI中未找到用户 {username}"
        user_page.screenshot(f"e2e_user_{username}_exists")
        logger.info(f"  ✅ UI验证成功: {username}")

        # ===== 步骤3：API删除用户 =====
        logger.info("步骤3: API删除用户")
        delete_resp = auth_api_client.delete(f"/api/users/{user_id}")
        assert delete_resp.get("code") == 200
        logger.info(f"  ✅ 用户删除成功: ID={user_id}")

        # ===== 步骤4：UI验证用户已删除 =====
        logger.info("步骤4: UI验证用户已删除")
        user_page.search_user(username)
        user_count_after = user_page.get_user_count()
        assert user_count_after == 0, f"删除后UI仍存在用户 {username}"
        user_page.screenshot(f"e2e_user_{username}_deleted")
        logger.info(f"  ✅ UI验证删除成功: {username}")

        logger.info("=" * 60)
        logger.info("✅ 端到端测试全部通过")

    @pytest.mark.e2e
    def test_order_flow(self, auth_api_client, login_page):
        """
        订单流程测试：
        1. API创建订单
        2. UI查看订单
        3. API更新订单状态
        4. UI验证状态更新
        """
        # ===== 步骤1：API创建订单 =====
        order_data = DataGenerator.generate_order_data()
        order_no = order_data["order_no"]

        logger.info("=" * 60)
        logger.info(f"步骤1: API创建订单 {order_no}")
        create_resp = auth_api_client.post("/api/orders", json_data=order_data)
        assert create_resp.get("code") == 200
        order_id = create_resp.get("data", {}).get("id")
        logger.info(f"  ✅ 订单创建成功: ID={order_id}")

        # ===== 步骤2：UI查看订单 =====
        logger.info("步骤2: UI查看订单")
        home_page = login_page.login("admin", "admin123")
        order_page = home_page.navigate_to_order_page()
        order_page.search_order(order_no)

        assert order_page.get_order_count() >= 1
        order_page.screenshot(f"e2e_order_{order_no}_exists")
        logger.info(f"  ✅ UI验证成功: {order_no}")

        # ===== 步骤3：API更新订单状态 =====
        logger.info("步骤3: API更新订单状态")
        update_resp = auth_api_client.put(
            f"/api/orders/{order_id}/status",
            json_data={"status": "paid"}
        )
        assert update_resp.get("code") == 200
        logger.info(f"  ✅ 订单状态更新成功: ID={order_id}")

        # ===== 步骤4：UI验证状态更新 =====
        logger.info("步骤4: UI验证状态更新")
        order_page.refresh()
        order_page.search_order(order_no)
        status = order_page.get_order_status(order_no)

        assert status == "paid", f"订单状态未更新，当前: {status}"
        order_page.screenshot(f"e2e_order_{order_no}_updated")
        logger.info(f"  ✅ UI验证状态更新成功: {status}")

        logger.info("=" * 60)
        logger.info("✅ 订单流程测试通过")