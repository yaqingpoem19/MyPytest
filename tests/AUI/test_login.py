# tests/ui/test_login.py
import pytest
from common.logger import get_logger
from config.config import config

logger = get_logger("test_login")


class TestLogin:
    """登录测试"""

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_success(self, login_page):
        """测试登录成功"""
        username = config.get_ui_username()
        password = config.get_ui_password()

        logger.info(f"登录测试: {username}")
        home_page = login_page.login(username, password)
        welcome_text = home_page.get_welcome_text()

        assert "欢迎" in welcome_text or "Welcome" in welcome_text
        home_page.screenshot("login_success")
        logger.info("✅ 登录成功测试通过")

    @pytest.mark.ui
    def test_login_fail_wrong_password(self, login_page):
        """测试密码错误登录失败"""
        username = config.get_ui_username()

        login_page.login_expect_fail(username, "wrongpassword")
        error = login_page.get_error_message()

        assert error, "错误信息为空"
        assert "错误" in error or "Error" in error
        login_page.screenshot("login_fail_wrong_password")
        logger.info("✅ 密码错误登录失败测试通过")

    @pytest.mark.ui
    def test_login_fail_wrong_username(self, login_page):
        """测试用户名错误登录失败"""
        login_page.login_expect_fail("wronguser", "wrongpass")
        error = login_page.get_error_message()

        assert error, "错误信息为空"
        assert "错误" in error or "Error" in error
        login_page.screenshot("login_fail_wrong_username")
        logger.info("✅ 用户名错误登录失败测试通过")

    @pytest.mark.ui
    def test_login_and_logout(self, login_page):
        """测试登录和登出"""
        username = config.get_ui_username()
        password = config.get_ui_password()

        home_page = login_page.login(username, password)
        login_page_after = home_page.logout()

        # 验证回到登录页
        current_url = login_page_after.get_url()
        assert "/login" in current_url or "/auth" in current_url
        login_page_after.screenshot("logout_success")
        logger.info("✅ 登录登出测试通过")