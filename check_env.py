# check_env.py
import sys
import re
import subprocess
from pathlib import Path


class EnvironmentChecker:
    """环境依赖检查器"""

    # 常见包名与导入名的映射（当包名和导入名不一致时）
    IMPORT_MAP = {
        "pytest-html": "pytest_html",
        "allure-pytest": "allure_pytest",
        "pytest-xdist": "pytest_xdist",
        "pytest-rerunfailures": "pytest_rerunfailures",
        "pytest-ordering": "pytest_ordering",
        "pytest-timeout": "pytest_timeout",
        "pytest-assume": "pytest_assume",
        "pytest-reportlog": "pytest_reportlog",
        "python-dotenv": "dotenv",
        "pyyaml": "yaml",
        "psycopg2-binary": "psycopg2",
        "python-dateutil": "dateutil",
        "jsonschema": "jsonschema",
        "jsonpath": "jsonpath",
        "retry": "retry",
    }

    # 需要特殊检查的包（无法通过普通 import 检查）
    SPECIAL_CHECK = {
        "black": "black",
        "flake8": "flake8",
        "mypy": "mypy",
        "pre-commit": "pre_commit",
    }

    def __init__(self, requirements_file="requirements.txt"):
        self.requirements_file = Path(requirements_file)
        self.packages = []
        self.results = []

    def parse_requirements(self):
        """
        解析 requirements.txt 文件，提取包名和版本约束
        支持多种格式：
        - pytest>=7.4.0
        - requests==2.31.0
        - openpyxl
        - pytest-html>=4.0.0,<5.0.0
        - # 注释行（跳过）
        - git+https://...（跳过，暂不支持检查）
        """
        if not self.requirements_file.exists():
            print(f"❌ 找不到 requirements.txt 文件: {self.requirements_file}")
            print("请确保在项目根目录执行此脚本")
            return False

        with open(self.requirements_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith("#"):
                    continue
                # 跳过 git 安装的包（无法通过 pip show 检查）
                if line.startswith("git+") or line.startswith("-e"):
                    continue
                # 跳过 -i 镜像源配置
                if line.startswith("-i") or line.startswith("--"):
                    continue

                # 提取包名（去掉版本约束）
                # 匹配格式：包名>=版本 或 包名==版本 或 包名
                match = re.match(r'^([a-zA-Z0-9\-_.]+)', line)
                if match:
                    pkg_name = match.group(1)
                    # 如果有版本约束，也记录下来（用于显示）
                    version_constraint = line[len(pkg_name):].strip()
                    self.packages.append({
                        "name": pkg_name,
                        "constraint": version_constraint,
                        "raw": line
                    })
        return True

    def check_package(self, pkg_name):
        """
        检查单个包是否已安装
        返回: (是否安装, 版本号)
        """
        # 获取导入名（处理包名和导入名不一致的情况）
        import_name = self.IMPORT_MAP.get(pkg_name, pkg_name)

        # 特殊处理：有些包即使安装了，import 时名称也不同
        if pkg_name in self.SPECIAL_CHECK:
            import_name = self.SPECIAL_CHECK[pkg_name]

        try:
            # 尝试导入包
            module = __import__(import_name)
            # 获取版本号
            version = self.get_package_version(module, pkg_name)
            return True, version
        except ImportError:
            # 有些包虽然安装成功，但导入名不同，尝试使用 pip show
            return self.check_with_pip_show(pkg_name)
        except Exception:
            return False, None

    def get_package_version(self, module, pkg_name):
        """获取包的版本号"""
        # 优先从 __version__ 获取
        if hasattr(module, "__version__"):
            return module.__version__

        # 尝试从 pkg_resources 获取（更可靠）
        try:
            import pkg_resources
            version = pkg_resources.get_distribution(pkg_name).version
            return version
        except Exception:
            pass

        # 如果都获取不到，使用 pip show
        return self.get_version_from_pip(pkg_name)

    def get_version_from_pip(self, pkg_name):
        """使用 pip show 获取版本号"""
        try:
            result = subprocess.run(
                ["pip", "show", pkg_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return "unknown"

    def check_with_pip_show(self, pkg_name):
        """通过 pip show 检查包是否安装"""
        try:
            result = subprocess.run(
                ["pip", "show", pkg_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # 提取版本号
                version = "unknown"
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        version = line.split(":", 1)[1].strip()
                        break
                return True, version
        except Exception:
            pass
        return False, None

    def compare_version(self, installed, constraint):
        """
        简单对比版本（仅做显示提示，不做严格校验）
        返回: (是否满足, 提示信息)
        """
        if not constraint:
            return True, "无版本要求"

        # 简单提取版本号
        version_match = re.search(r'([\d.]+)', constraint)
        if not version_match:
            return True, f"版本约束: {constraint}"

        required_version = version_match.group(1)
        if installed == "unknown":
            return True, f"需要 {constraint}，但无法获取已安装版本"

        # 简单比较（实际应用中建议使用 packaging 库）
        try:
            installed_parts = [int(x) for x in installed.split(".")]
            required_parts = [int(x) for x in required_version.split(".")]

            # 比较主要版本号
            if installed_parts[0] < required_parts[0]:
                return False, f"版本过低: 已装 {installed}, 需要 {constraint}"
            elif installed_parts[0] > required_parts[0]:
                return True, f"版本更新: 已装 {installed} (需要 {constraint})"
            else:
                # 主版本相同，比较次版本
                if len(installed_parts) > 1 and len(required_parts) > 1:
                    if installed_parts[1] < required_parts[1]:
                        return False, f"版本过低: 已装 {installed}, 需要 {constraint}"
                return True, f"已装 {installed} (需要 {constraint})"
        except Exception:
            return True, f"已装 {installed} (需要 {constraint})"

    def run_check(self):
        """执行所有检查"""
        print("=" * 70)
        print("  🔍 Pytest 接口自动化测试环境检查")
        print("=" * 70)
        print(f"📋 检查文件: {self.requirements_file}\n")

        # 解析 requirements.txt
        if not self.parse_requirements():
            return False

        if not self.packages:
            print("⚠️ 没有找到需要检查的包，请检查 requirements.txt 格式")
            return False

        # 统计结果
        total = len(self.packages)
        installed_count = 0
        missing_packages = []
        version_warnings = []

        # 逐个检查
        for idx, pkg in enumerate(self.packages, 1):  # 遍历列表（所有包），从1开始计数
            pkg_name = pkg["name"]
            constraint = pkg["constraint"]

            installed, version = self.check_package(pkg_name)

            # 显示结果
            if installed:
                installed_count += 1
                # 检查版本
                if constraint:
                    ok, msg = self.compare_version(version, constraint)
                    if not ok:
                        version_warnings.append({
                            "name": pkg_name,
                            "msg": msg
                        })
                    status_icon = "✅" if ok else "⚠️"
                    status_text = f"{status_icon} 已安装"
                else:
                    status_text = "✅ 已安装"

                print(f"[{idx:2d}/{total}] {status_text}  {pkg_name:<25} 版本: {version}")
            else:
                missing_packages.append(pkg_name)
                print(f"[{idx:2d}/{total}] ❌ 未安装   {pkg_name:<25} 需要: {constraint if constraint else '最新版本'}")

        # 生成报告
        print("\n" + "=" * 70)
        print("  📊 检查结果汇总")
        print("=" * 70)
        print(f"总计依赖包: {total} 个")
        print(f"已安装:     {installed_count} 个")
        print(f"未安装:     {len(missing_packages)} 个")

        if version_warnings:
            print(f"\n⚠️ 版本警告: {len(version_warnings)} 个")
            for warn in version_warnings:
                print(f"   - {warn['name']}: {warn['msg']}")

        print("\n" + "=" * 70)

        # 给出建议
        if missing_packages:
            print("❌ 缺少以下依赖包，请执行安装命令:")
            print(f"\n   pip install {' '.join(missing_packages)}")
            print("\n   或一次性安装所有依赖:")
            print("   pip install -r requirements.txt")
            return False
        else:
            if version_warnings:
                print("⚠️ 所有包已安装，但部分版本可能不符合 requirements.txt 要求")
                print("建议执行以下命令更新到指定版本:")
                print("   pip install -r requirements.txt --upgrade")
            else:
                print("🎉 所有依赖包已安装且版本符合要求！")
                print("✅ 环境检查通过，可以开始编写测试用例了！")
            return True


def main():
    """主函数"""
    checker = EnvironmentChecker()
    success = checker.run_check()

    # 返回退出码（用于 CI/CD 流程）
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()