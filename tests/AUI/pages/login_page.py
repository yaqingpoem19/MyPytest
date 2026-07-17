
from playwright.sync_api import Page
from AUI.page_base import PageBase
from tests.AUI.pages.home_page import HomePage

class LoginPage(PageBase):
    """登录页面"""

    # 定位器
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    REMEMBER_ME = "#rememberMe"

    def __init__(self, page: Page):
        super().__init__(page)

    def login(self, username: str, password: str, remember: bool = False):
        """执行登录"""
        self.logger.info(f"登录: {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)

        if remember:
            self.click(self.REMEMBER_ME)

        self.click(self.LOGIN_BUTTON)

        # 等待登录完成，返回首页
        return HomePage(self.page)

    def login_expect_fail(self, username: str, password: str):
        """登录（期望失败）"""
        self.logger.info(f"登录（失败预期）: {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        """获取错误信息"""
        return self.get_text(self.ERROR_MESSAGE)