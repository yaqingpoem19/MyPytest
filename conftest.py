# conftest.py pytest的核心特性文件，全局配置，放在根目录，里面的fixture可以供所有 tests 目录下的用例使用

import pytest
from config.config import config
from API.base import RESTClient


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="指定运行环境: dev, test, staging, production"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_env(request):
    """环境初始化"""
    env = request.config.getoption("--env")
    if env:
        config.switch_env(env)
        print(f"\n✅ 环境切换为: {env}")

    info = config.get_env_info()
    print(f"\n📋 当前配置:")
    print(f"   环境: {info['environment']}")
    print(f"   主机: {info['host']}")
    print(f"   超时: {info['timeout']}s")

    print("\n【服务地址】")
    for service, port in info['services'].items():
        print(f"   {service}: http://{info['host']}:{port}")


# ===== 各服务客户端 Fixture =====

@pytest.fixture(scope="session")
def model_client():
    """web端接口查询服务客户端"""
    return RESTClient(service_name='model')


@pytest.fixture(scope="session")
def valid_client():
    """提资数据校验服务"""
    return RESTClient(service_name='valid')


@pytest.fixture(scope="session")
def datacommitstore_client():
    """提资数据发布存储服务"""
    return RESTClient(service_name='datacommitstore')


@pytest.fixture(scope="session")
def packageno_client():
    """包号生成服务"""
    return RESTClient(service_name='generatePackageNo')


# ===== 通用客户端（保持向后兼容） =====

@pytest.fixture(scope="session")
def api_client():
    """通用API客户端（默认使用模型服务）"""
    return RESTClient(service_name='model')


# ===== 动态客户端工厂 =====

@pytest.fixture
def get_client():
    """动态获取服务客户端的工厂函数"""

    def _get_client(service_name: str):
        return RESTClient(service_name=service_name)

    return _get_client


# ===== 环境信息 =====

@pytest.fixture
def env_info():
    """环境信息"""
    return config.get_env_info()


@pytest.fixture
def service_urls():
    """所有服务URL"""
    return {
        'model': config.MODEL_SERVICE_URL,
        'valid': config.VALID_SERVICE_URL,
        'datacommitstore': config.DATA_COMMIT_STORE_SERVICE_URL,
        'generatepackageno': config.GENERATE_PACKAGE_NO_URL,
    }


# ===== 自动清理 =====
@pytest.fixture(autouse=True)
def auto_cleanup():
    """测试后自动清理"""
    yield
    # 测试完成后清理（如删除临时数据）
    pass