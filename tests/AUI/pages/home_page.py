# tests/ui/pages/home_page.py
from playwright.sync_api import Page
from AUI.page_base import PageBase


class HomePage(PageBase):
    """首页"""

    WELCOME_TEXT = ".welcome-text"
    USER_MENU = ".user-menu"
    LOGOUT_BUTTON = ".logout-btn"
    NAV_USER = "a[href='/users']"
    NAV_ORDER = "a[href='/orders']"

    def __init__(self, page: Page):
        super().__init__(page)
        # 等待页面加载完成
        self.wait_for_selector(self.WELCOME_TEXT)

    def get_welcome_text(self) -> str:
        """获取欢迎文本"""
        return self.get_text(self.WELCOME_TEXT)

    def logout(self):
        """退出登录"""
        self.logger.info("退出登录")
        self.click(self.USER_MENU)
        self.click(self.LOGOUT_BUTTON)

        from tests.AUI.pages.login_page import LoginPage
        return LoginPage(self.page)

    def navigate_to_user_page(self):
        """跳转到用户页面"""
        self.logger.info("跳转到用户页面")
        self.click(self.NAV_USER)

        from tests.AUI.pages.user_page import UserPage
        return UserPage(self.page)
