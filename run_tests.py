# run_tests.py
# !/usr/bin/env python
"""
测试运行入口
用法:
    python run_tests.py                      # 运行所有测试
    python run_tests.py --type api           # 只运行API测试
    python run_tests.py --type ui            # 只运行UI测试
    python run_tests.py --type e2e           # 只运行端到端测试
    python run_tests.py --env test           # 指定环境
    python run_tests.py --marker smoke       # 按标记运行
    python run_tests.py --parallel           # 并行运行
    python run_tests.py --report             # 生成报告
"""

import sys
import subprocess
from argparse import ArgumentParser


def run_tests(args):
    """运行测试"""
    cmd = ["pytest"]

    # 测试类型
    type_map = {
        "api": ["tests/api/"],
        "ui": ["tests/ui/"],
        "e2e": ["tests/e2e/"],
        "all": ["tests/"]
    }
    cmd.extend(type_map.get(args.type, ["tests/"]))

    # 环境
    if args.env:
        cmd.extend(["--env", args.env])

    # 标记
    if args.marker:
        cmd.extend(["-m", args.marker])

    # 并行
    if args.parallel:
        cmd.extend(["-n", "auto"])

    # 无头模式
    if args.headless:
        cmd.append("--headless")

    # 报告
    if args.report:
        cmd.extend([
            "--html=report/test_report.html",
            "--self-contained-html",
            "--junitxml=report/junit.xml"
        ])

    # 调试
    if args.debug:
        cmd.append("--log-cli-level=DEBUG")

    # 基本参数
    cmd.extend(["-v", "-s"])

    # 执行
    print(f"\n🚀 执行命令: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = ArgumentParser(description="自动化测试运行器")
    parser.add_argument("--type", choices=["api", "ui", "e2e", "all"],
                        default="all", help="测试类型")
    parser.add_argument("--env", choices=["dev", "test", "staging", "prod"],
                        default="test", help="运行环境")
    parser.add_argument("--marker", type=str, help="按标记运行")
    parser.add_argument("--parallel", action="store_true", help="并行运行")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--debug", action="store_true", help="调试模式")

    args = parser.parse_args()
    sys.exit(run_tests(args))


if __name__ == "__main__":
    main()