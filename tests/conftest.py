# tests/conftest.py
import pytest
from pathlib import Path
from common.logger import get_logger
from config.config import config
from API.rest_client import RESTClient
from AUI.browser_helper import BrowserHelper

logger = get_logger("conftest")


# ===== 命令行参数 =====
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="指定运行环境: dev, test, staging, prod"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="UI测试使用无头模式"
    )


# ===== 环境初始化 =====
@pytest.fixture(scope="session", autouse=True)
def setup_environment(request):
    """全局环境初始化"""
    env = request.config.getoption("--env")
    if env:
        config.switch_env(env)
        logger.info(f"环境切换为: {env}")

    info = config.get_env_info()
    logger.info("=" * 60)
    logger.info("  📋 测试环境信息")
    logger.info("=" * 60)
    logger.info(f"  环境: {info['environment']}")
    logger.info(f"  API地址: {info['api_base_url']}")
    logger.info(f"  UI地址: {info['ui_base_url']}")
    logger.info(f"  超时: {info['timeout']}s")
    logger.info("=" * 60)


# ===== API Fixtures =====
@pytest.fixture(scope="session")
def api_client():
    """API客户端"""
    return RESTClient(config.get_api_base_url(), config.get_api_timeout())


@pytest.fixture(scope="session")
def auth_api_client():
    """带认证的API客户端"""
    client = RESTClient(config.get_api_base_url(), config.get_api_timeout())
    token = config.get_api_token()
    if token:
        client.set_auth(token)
    return client


# ===== UI Fixtures =====
@pytest.fixture(scope="session")
def browser_helper(request):
    """浏览器辅助"""
    headless = request.config.getoption("--headless") or config.get_ui_headless()
    helper = BrowserHelper(headless=headless)
    helper.launch()
    helper.new_context()
    yield helper
    helper.close()


@pytest.fixture
def page(browser_helper):
    """页面fixture"""
    page = browser_helper.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page):
    """登录页面"""
    from tests.ui.pages.login_page import LoginPage
    return LoginPage(page)


# ===== 测试结果收集 =====
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """收集测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_sessionfinish(session, exitstatus):
    """测试结束后打印摘要"""
    print("\n" + "=" * 60)
    print("  📊 测试执行摘要")
    print("=" * 60)

    total = 0
    passed = 0
    failed = 0
    skipped = 0

    for item in session.items:
        total += 1
        if hasattr(item, 'rep_call'):
            if item.rep_call.outcome == 'passed':
                passed += 1
            elif item.rep_call.outcome == 'failed':
                failed += 1
            elif item.rep_call.outcome == 'skipped':
                skipped += 1

    print(f"  总测试数: {total}")
    print(f"  ✅ 通过: {passed}")
    print(f"  ❌ 失败: {failed}")
    print(f"  ⏭️ 跳过: {skipped}")
    if total > 0:
        print(f"  通过率: {(passed / total * 100):.1f}%")
    print("=" * 60)