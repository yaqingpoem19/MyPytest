
                     基于Pytest的接口自动化测试框架

├── base/                      # 基础层
│   └── method.py              # 封装请求方法 (如调用requests库)[citation:2]
├── common/                    # 公共模块
│   ├── login.py               # 封装登录逻辑，提供fixture[citation:2]
│   └── public.py              # 公共函数 (如读取文件)[citation:2]
├── config/                    # 配置管理
│   └── config.py              # 读取配置文件
├── data/                      # 测试数据
│   └── data.xlsx              # Excel格式测试数据[citation:2]
├── utils/                     # 工具类
│   └── operationExcel.py      # 封装读取Excel的方法[citation:2]
├── tests/                     # 测试用例目录 (遵循pytest命名规则)
│   ├── __init__.py            # 必须存在，使目录成为包[citation:8]
│   ├── test_user_api.py       # 测试文件，以test_开头
│   └── test_product_api.py
├── log/                       # 日志目录[citation:2]
├── report/                    # 测试报告目录 (如allure报告)[citation:2]
├── pyproject.toml             # 项目配置和依赖管理 (或使用requirements.txt)[citation:4]
└── conftest.py                # 存放全局fixture和插件的配置文件