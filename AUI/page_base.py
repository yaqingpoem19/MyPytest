# ui/base/page_base.py
from typing import Optional, Union, List
from playwright.sync_api import Page, Locator, expect
from common.logger import get_logger
from common.exceptions import UIActionError


class PageBase:
    """页面基类"""

    def __init__(self, page: Page, timeout: int = 30000):
        self.page = page
        self.timeout = timeout
        self.logger = get_logger(self.__class__.__name__)

    # ===== 元素操作 =====

    def find(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """查找元素"""
        return self.page.locator(selector).first

    def find_all(self, selector: str) -> List[Locator]:
        """查找所有元素"""
        return self.page.locator(selector).all()

    def click(self, selector: str, timeout: Optional[int] = None, **kwargs) -> 'PageBase':
        """点击元素"""
        try:
            self.logger.info(f"点击: {selector}")
            self.page.locator(selector).click(timeout=timeout or self.timeout, **kwargs)
            return self
        except Exception as e:
            self.logger.error(f"点击失败: {selector}, {e}")
            raise UIActionError(f"点击失败: {selector}, {e}")

    def fill(self, selector: str, text: str, timeout: Optional[int] = None, **kwargs) -> 'PageBase':
        """输入文本"""
        try:
            self.logger.info(f"输入: {selector} = {text}")
            self.page.locator(selector).fill(text, timeout=timeout or self.timeout, **kwargs)
            return self
        except Exception as e:
            self.logger.error(f"输入失败: {selector}, {e}")
            raise UIActionError(f"输入失败: {selector}, {e}")

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取文本"""
        try:
            text = self.page.locator(selector).text_content(timeout=timeout or self.timeout)
            return text or ""
        except Exception as e:
            self.logger.error(f"获取文本失败: {selector}, {e}")
            return ""

    def get_value(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取输入框的值"""
        try:
            return self.page.locator(selector).input_value(timeout=timeout or self.timeout)
        except Exception as e:
            self.logger.error(f"获取值失败: {selector}, {e}")
            return ""

    def get_attribute(self, selector: str, attr_name: str, timeout: Optional[int] = None) -> str:
        """获取元素属性"""
        try:
            return self.page.locator(selector).get_attribute(attr_name, timeout=timeout or self.timeout)
        except Exception as e:
            self.logger.error(f"获取属性失败: {selector}, {e}")
            return ""

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否可见"""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout or self.timeout)
        except Exception:
            return False

    def is_exists(self, selector: str) -> bool:
        """检查元素是否存在"""
        try:
            return self.page.locator(selector).count() > 0
        except Exception:
            return False

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None):
        """等待元素出现"""
        self.page.wait_for_selector(selector, state=state, timeout=timeout or self.timeout)
        return self

    def wait_for_timeout(self, milliseconds: int):
        """等待指定时间"""
        self.page.wait_for_timeout(milliseconds)
        return self

    # ===== 页面操作 =====

    def navigate(self, url: str, timeout: Optional[int] = None) -> 'PageBase':
        """导航到指定URL"""
        self.logger.info(f"导航到: {url}")
        self.page.goto(url, timeout=timeout or self.timeout)
        return self

    def get_url(self) -> str:
        """获取当前URL"""
        return self.page.url

    def get_title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    def refresh(self) -> 'PageBase':
        """刷新页面"""
        self.page.reload()
        return self

    def go_back(self) -> 'PageBase':
        """后退"""
        self.page.go_back()
        return self

    def screenshot(self, name: str = "screenshot") -> str:
        """截图"""
        from pathlib import Path
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)

        filename = f"{name}_{self.page.title()[:20]}_{self.page.url.split('/')[-1][:10]}.png"
        file_path = screenshot_dir / filename
        self.page.screenshot(path=str(file_path), full_page=True)
        self.logger.info(f"截图保存: {file_path}")
        return str(file_path)

    # ===== 断言 =====

    def assert_text(self, selector: str, expected: str, timeout: Optional[int] = None):
        """断言文本内容"""
        actual = self.get_text(selector, timeout)
        assert actual == expected, f"文本断言失败: 期望 '{expected}', 实际 '{actual}'"
        self.logger.info(f"✅ 文本断言通过: {expected}")

    def assert_contains_text(self, selector: str, expected: str, timeout: Optional[int] = None):
        """断言文本包含"""
        actual = self.get_text(selector, timeout)
        assert expected in actual, f"文本包含断言失败: '{expected}' 不在 '{actual}' 中"
        self.logger.info(f"✅ 文本包含断言通过: {expected}")

    def assert_visible(self, selector: str, timeout: Optional[int] = None):
        """断言元素可见"""
        assert self.is_visible(selector, timeout), f"元素不可见: {selector}"
        self.logger.info(f"✅ 元素可见断言通过: {selector}")

    def assert_not_visible(self, selector: str, timeout: Optional[int] = None):
        """断言元素不可见"""
        assert not self.is_visible(selector, timeout), f"元素仍然可见: {selector}"
        self.logger.info(f"✅ 元素不可见断言通过: {selector}")

    def assert_url(self, expected_url: str):
        """断言当前URL"""
        actual = self.get_url()
        assert actual == expected_url, f"URL断言失败: 期望 '{expected_url}', 实际 '{actual}'"
        self.logger.info(f"✅ URL断言通过: {expected_url}")

    def assert_url_contains(self, expected_part: str):
        """断言URL包含"""
        actual = self.get_url()
        assert expected_part in actual, f"URL包含断言失败: '{expected_part}' 不在 '{actual}' 中"
        self.logger.info(f"✅ URL包含断言通过: {expected_part}")