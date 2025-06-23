import argparse
import os
from typing import Dict, Any, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .detector import BrowserDetector


class BrowserDetectorCLI:
    """浏览器检测工具的命令行界面"""
    
    def __init__(self):
        self.detector = BrowserDetector()
        self.browsers = {}
        self.console = Console() if HAS_RICH else None
    
    def parse_arguments(self):
        """解析命令行参数"""
        parser = argparse.ArgumentParser(description="检测系统中已安装的浏览器及其版本")
        parser.add_argument("-j", "--json", action="store_true", help="以JSON格式输出结果")
        parser.add_argument("-l", "--launch", type=str, help="启动指定的浏览器 (例如: chrome, firefox)")
        parser.add_argument("-a", "--all", action="store_true", help="显示所有详细信息")
        
        return parser.parse_args()
    
    def detect_browsers(self):
        """检测浏览器"""
        print("正在检测浏览器...")
        self.browsers = self.detector.detect_browsers()
        
        if not self.browsers:
            print("未检测到任何浏览器")
            return False
        
        return True
    
    def display_browsers(self, json_format=False, show_all=False):
        """显示检测到的浏览器"""
        if json_format:
            self._display_json()
        elif HAS_RICH:
            self._display_rich_table(show_all)
        else:
            self._display_plain_text(show_all)
    
    def _display_json(self):
        """以JSON格式显示结果"""
        import json
        print(json.dumps(self.browsers, indent=2))
    
    def _display_rich_table(self, show_all=False):
        """使用Rich库显示漂亮的表格"""
        table = Table(title="检测到的浏览器", box=box.ROUNDED)
        
        table.add_column("浏览器", style="cyan", no_wrap=True)
        table.add_column("版本", style="green")
        
        if show_all:
            table.add_column("路径", style="yellow")
        
        for browser_name, info in self.browsers.items():
            if show_all:
                table.add_row(browser_name, info.get('version', 'Unknown'), info.get('path', 'Unknown'))
            else:
                table.add_row(browser_name, info.get('version', 'Unknown'))
        
        self.console.print(table)
    
    def _display_plain_text(self, show_all=False):
        """以纯文本格式显示结果"""
        print("\n检测到的浏览器:")
        print("-" * 40)
        
        for browser_name, info in self.browsers.items():
            print(f"浏览器: {browser_name}")
            print(f"版本: {info.get('version', 'Unknown')}")
            
            if show_all:
                print(f"路径: {info.get('path', 'Unknown')}")
            
            print("-" * 40)
    
    def launch_browser(self, browser_name: str):
        """启动指定的浏览器"""
        import webbrowser
        
        browser_name = browser_name.capitalize()
        if browser_name not in self.browsers:
            print(f"未找到浏览器: {browser_name}")
            return False
        
        path = self.browsers[browser_name].get('path')
        if path and os.path.exists(path):
            try:
                webbrowser.register(browser_name.lower(), None, webbrowser.BackgroundBrowser(path))
                webbrowser.get(browser_name.lower()).open("https://www.google.com")
                print(f"已启动 {browser_name}")
                return True
            except Exception as e:
                print(f"启动浏览器出错: {str(e)}")
        else:
            print("无法找到浏览器可执行文件")
        
        return False
    
    def run(self):
        """运行CLI界面"""
        args = self.parse_arguments()
        
        if not self.detect_browsers():
            return
        
        if args.launch:
            self.launch_browser(args.launch)
        else:
            self.display_browsers(args.json, args.all) 