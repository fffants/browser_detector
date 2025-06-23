import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser
from .detector import BrowserDetector


class BrowserDetectorGUI:
    """浏览器检测工具的图形用户界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("浏览器检测工具")
        self.root.geometry("700x400")
        self.root.resizable(True, True)
        
        self.detector = BrowserDetector()
        self.browsers = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="浏览器检测工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 描述
        desc_label = ttk.Label(main_frame, text="检测系统中安装的所有浏览器及其版本信息")
        desc_label.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # 检测按钮
        detect_button = ttk.Button(button_frame, text="检测浏览器", command=self.detect_browsers)
        detect_button.pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        refresh_button = ttk.Button(button_frame, text="刷新", command=self.detect_browsers)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 启动按钮
        launch_button = ttk.Button(button_frame, text="启动选中的浏览器", command=self.launch_selected_browser)
        launch_button.pack(side=tk.LEFT, padx=5)
        
        # 树形视图 - 显示浏览器信息
        columns = ("浏览器", "版本", "路径")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W)
        
        # 调整列宽
        self.tree.column("浏览器", width=100)
        self.tree.column("版本", width=100)
        self.tree.column("路径", width=400)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # 放置树形视图和滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 状态栏
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var.set("准备就绪")
    
    def detect_browsers(self):
        """检测浏览器并显示结果"""
        self.status_var.set("正在检测浏览器...")
        self.root.update()
        
        # 清空树形视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            self.browsers = self.detector.detect_browsers()
            
            if not self.browsers:
                messagebox.showinfo("结果", "未检测到任何浏览器")
                self.status_var.set("检测完成，未找到浏览器")
                return
            
            # 填充树形视图
            for browser_name, info in self.browsers.items():
                version = info.get('version', 'Unknown')
                path = info.get('path', 'Unknown')
                self.tree.insert("", tk.END, values=(browser_name, version, path))
            
            self.status_var.set(f"检测完成，发现 {len(self.browsers)} 个浏览器")
        except Exception as e:
            messagebox.showerror("错误", f"检测过程中出错: {str(e)}")
            self.status_var.set("检测失败")
    
    def launch_selected_browser(self):
        """启动选中的浏览器"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一个浏览器")
            return
            
        item = selection[0]
        browser_name = self.tree.item(item, "values")[0]
        self._launch_browser(browser_name)
    
    def _launch_browser(self, browser_name):
        """启动指定的浏览器"""
        path = self.browsers.get(browser_name, {}).get('path')
        
        if path and os.path.exists(path):
            try:
                webbrowser.register(browser_name.lower(), None, webbrowser.BackgroundBrowser(path))
                webbrowser.get(browser_name.lower()).open("https://www.google.com")
                self.status_var.set(f"已启动 {browser_name}")
            except Exception as e:
                messagebox.showerror("错误", f"无法启动浏览器: {str(e)}")
        else:
            messagebox.showerror("错误", "无法找到浏览器可执行文件") 