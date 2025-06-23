import sys
import argparse
import tkinter as tk

from browser_detector.detector import BrowserDetector
from browser_detector.gui import BrowserDetectorGUI
from browser_detector.cli import BrowserDetectorCLI


def main():
    """程序主入口"""
    parser = argparse.ArgumentParser(description="浏览器检测工具")
    parser.add_argument("--cli", action="store_true", help="使用命令行界面")
    parser.add_argument("--gui", action="store_true", help="使用图形用户界面")
    
    # 先解析--cli和--gui参数
    args, remaining = parser.parse_known_args()
    
    # 如果没有指定接口类型，默认使用GUI
    use_gui = not args.cli or args.gui
    
    if use_gui:
        # 启动GUI
        root = tk.Tk()
        app = BrowserDetectorGUI(root)
        root.mainloop()
    else:
        # 启动CLI
        sys.argv = [sys.argv[0]] + remaining  # 重置sys.argv，移除--cli参数
        cli = BrowserDetectorCLI()
        cli.run()


if __name__ == "__main__":
    main() 