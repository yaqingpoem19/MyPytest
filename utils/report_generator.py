# utils/report_generator.py
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from common.logger import get_logger

logger = get_logger("ReportGenerator")


class ReportGenerator:
    """测试报告生成器"""

    def __init__(self, report_dir: str = "report"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)

    def generate_json_report(self, results: List[Dict], filename: str = "test_summary.json") -> str:
        """生成JSON格式报告"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'total': len(results),
            'passed': len([r for r in results if r.get('outcome') == 'passed']),
            'failed': len([r for r in results if r.get('outcome') == 'failed']),
            'skipped': len([r for r in results if r.get('outcome') == 'skipped']),
            'results': results
        }

        file_path = self.report_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        logger.info(f"JSON报告已生成: {file_path}")
        return str(file_path)

    def generate_html_report(self, results: List[Dict], filename: str = "test_report.html") -> str:
        """生成HTML格式报告"""
        total = len(results)
        passed = len([r for r in results if r.get('outcome') == 'passed'])
        failed = len([r for r in results if r.get('outcome') == 'failed'])
        skipped = len([r for r in results if r.get('outcome') == 'skipped'])
        pass_rate = f"{(passed / total * 100):.1f}%" if total > 0 else "0%"

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>自动化测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .summary-item {{ padding: 15px 30px; border-radius: 8px; font-weight: bold; }}
        .total {{ background: #f0f0f0; }}
        .passed {{ background: #d4edda; color: #155724; }}
        .failed {{ background: #f8d7da; color: #721c24; }}
        .skipped {{ background: #fff3cd; color: #856404; }}
        .rate {{ background: #cce5ff; color: #004085; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f2f2f2; }}
        .outcome-passed {{ color: green; }}
        .outcome-failed {{ color: red; }}
        .outcome-skipped {{ color: orange; }}
    </style>
</head>
<body>
    <h1>🚀 自动化测试报告</h1>
    <div style="color: #666; margin-bottom: 20px;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

    <div class="summary">
        <div class="summary-item total">📊 总计: {total}</div>
        <div class="summary-item passed">✅ 通过: {passed}</div>
        <div class="summary-item failed">❌ 失败: {failed}</div>
        <div class="summary-item skipped">⏭️ 跳过: {skipped}</div>
        <div class="summary-item rate">📈 通过率: {pass_rate}</div>
    </div>

    <h3>📋 详细结果</h3>
    <table>
        <thead>
            <tr>
                <th>测试类</th>
                <th>测试方法</th>
                <th>结果</th>
                <th>耗时(s)</th>
                <th>时间</th>
            </tr>
        </thead>
        <tbody>
"""
        for r in results:
            outcome = r.get('outcome', 'unknown')
            icon = '✅' if outcome == 'passed' else '❌' if outcome == 'failed' else '⏭️'
            html += f"""
            <tr>
                <td>{r.get('class', '')}</td>
                <td>{r.get('name', '')}</td>
                <td class="outcome-{outcome}">{icon} {outcome}</td>
                <td>{r.get('duration', 0):.2f}</td>
                <td>{r.get('start_time', '')}</td>
            </tr>
"""
        html += """
        </tbody>
    </table>
</body>
</html>
"""
        file_path = self.report_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"HTML报告已生成: {file_path}")
        return str(file_path)