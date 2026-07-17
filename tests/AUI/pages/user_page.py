# tests/ui/pages/user_page.py
from playwright.sync_api import Page
from AUI.page_base import PageBase


class UserPage(PageBase):
    """用户管理页面"""

    ADD_USER_BUTTON = ".add-user-btn"
    USER_TABLE = ".user-table"
    USER_NAME_INPUT = "#userName"
    USER_EMAIL_INPUT = "#userEmail"
    USER_PHONE_INPUT = "#userPhone"
    SAVE_BUTTON = ".save-btn"
    CANCEL_BUTTON = ".cancel-btn"
    CONFIRM_DELETE = ".confirm-delete"
    SEARCH_INPUT = "input[placeholder='搜索用户']"
    SEARCH_BUTTON = ".search-btn"

    def __init__(self, page: Page):
        super().__init__(page)
        self.wait_for_selector(self.USER_TABLE)

    def add_user(self, name: str, email: str, phone: str = ""):
        """添加用户"""
        self.logger.info(f"添加用户: {name}")
        self.click(self.ADD_USER_BUTTON)
        self.wait_for_selector(self.USER_NAME_INPUT)

        self.fill(self.USER_NAME_INPUT, name)
        self.fill(self.USER_EMAIL_INPUT, email)
        if phone:
            self.fill(self.USER_PHONE_INPUT, phone)

        self.click(self.SAVE_BUTTON)
        return self

    def delete_user(self, name: str):
        """删除用户"""
        self.logger.info(f"删除用户: {name}")
        self.click(f"tr:has-text('{name}') .delete-btn")
        self.click(self.CONFIRM_DELETE)
        return self

    def search_user(self, keyword: str):
        """搜索用户"""
        self.logger.info(f"搜索用户: {keyword}")
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        return self

    def get_user_count(self) -> int:
        """获取用户数量"""
        return self.page.locator(f"{self.USER_TABLE} tbody tr").count()

    def get_user_names(self) -> list:
        """获取所有用户名"""
        rows = self.page.locator(f"{self.USER_TABLE} tbody tr").all()
        names = []
        for row in rows:
            name_cell = row.locator("td").first
            if name_cell:
                names.append(name_cell.text_content() or "")
        return names

    def user_exists(self, name: str) -> bool:
        """检查用户是否存在"""
        self.search_user(name)
        return self.get_user_count() > 0