# ui/base/browser_helper.py
from typing import Optional, Dict, Any
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from common.logger import get_logger
from common.exceptions import UIActionError


class BrowserHelper:
    """浏览器辅助类"""

    def __init__(self, headless: bool = False, viewport: Optional[Dict] = None):
        self.headless = headless
        self.viewport = viewport or {"width": 1920, "height": 1080}
        self.logger = get_logger("BrowserHelper")

        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    def launch(self, browser_type: str = "chromium") -> 'BrowserHelper':
        """启动浏览器"""
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()

            if browser_type == "chromium":
                self.browser = self.playwright.chromium.launch(headless=self.headless)
            elif browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(headless=self.headless)
            elif browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"不支持的浏览器类型: {browser_type}")

            self.logger.info(f"浏览器已启动: {browser_type} (headless={self.headless})")
            return self
        except Exception as e:
            self.logger.error(f"启动浏览器失败: {e}")
            raise UIActionError(f"启动浏览器失败: {e}")

    def new_context(self, **kwargs) -> 'BrowserHelper':
        """创建新上下文"""
        self.context = self.browser.new_context(
            viewport=self.viewport,
            **kwargs
        )
        self.logger.info("浏览器上下文已创建")
        return self

    def new_page(self) -> Page:
        """创建新页面"""
        if not self.context:
            self.new_context()
        return self.context.new_page()

    def close(self):
        """关闭浏览器"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.logger.info("浏览器已关闭")
        except Exception as e:
            self.logger.error(f"关闭浏览器失败: {e}")

    def screenshot(self, page: Page, name: str = "screenshot") -> str:
        """截图"""
        from pathlib import Path
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)

        filename = f"{name}_{page.title()[:20]}.png"
        file_path = screenshot_dir / filename
        page.screenshot(path=str(file_path), full_page=True)
        self.logger.info(f"截图保存: {file_path}")
        return str(file_path)