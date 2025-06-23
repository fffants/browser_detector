import os
import sys
import winreg
import subprocess
from typing import Dict, List, Optional, Tuple


class BrowserDetector:
    """检测系统中安装的浏览器及其版本"""
    
    def __init__(self):
        self.browsers = {}
        # 常见浏览器的注册表路径
        self.registry_paths = {
            'Chrome': r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe',
            'Firefox': r'SOFTWARE\Mozilla\Mozilla Firefox',
            'Edge': r'SOFTWARE\Microsoft\Edge\BLBeacon',
            'Opera': r'SOFTWARE\Clients\StartMenuInternet\OperaStable\Capabilities',
            'Brave': r'SOFTWARE\BraveSoftware\Brave-Browser\BLBeacon',
            'Vivaldi': r'SOFTWARE\Vivaldi',
        }
        # 常见浏览器的安装路径
        self.common_paths = {
            'Chrome': [r'C:\Program Files\Google\Chrome\Application\chrome.exe', 
                      r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'],
            'Firefox': [r'C:\Program Files\Mozilla Firefox\firefox.exe',
                       r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'],
            'Edge': [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'],
            'Opera': [r'C:\Program Files\Opera\launcher.exe',
                     r'C:\Program Files (x86)\Opera\launcher.exe'],
            'Brave': [r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                     r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'],
            'Vivaldi': [r'C:\Program Files\Vivaldi\Application\vivaldi.exe',
                       r'C:\Program Files (x86)\Vivaldi\Application\vivaldi.exe'],
        }
        # 版本注册表路径
        self.version_registry_paths = {
            'Chrome': r'SOFTWARE\Google\Chrome\BLBeacon',
            'Edge': r'SOFTWARE\Microsoft\Edge\BLBeacon',
            'Brave': r'SOFTWARE\BraveSoftware\Brave-Browser\BLBeacon',
        }
    
    def detect_browsers(self) -> Dict[str, Dict[str, str]]:
        """检测所有已安装的浏览器及其版本"""
        self.detect_from_registry()
        self.detect_from_file_paths()
        return self.browsers
    
    def detect_from_registry(self) -> None:
        """从Windows注册表中检测浏览器"""
        for browser_name, reg_path in self.registry_paths.items():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    if browser_name == 'Chrome':
                        path = winreg.QueryValue(key, None)
                        version = self.get_version_from_registry(browser_name) or self.get_file_version(path)
                    elif browser_name == 'Firefox':
                        version = winreg.QueryValue(key, 'CurrentVersion')
                        path = self.get_firefox_path()
                    elif browser_name == 'Edge':
                        version = winreg.QueryValueEx(key, 'version')[0]
                        path = self.get_edge_path()
                    elif browser_name == 'Opera':
                        # Opera需要特殊处理
                        path = self.get_opera_path()
                        version = self.get_file_version(path)
                    elif browser_name == 'Brave':
                        version = winreg.QueryValueEx(key, 'version')[0]
                        path = self.get_brave_path()
                    elif browser_name == 'Vivaldi':
                        path = self.get_vivaldi_path()
                        version = self.get_file_version(path)
                    
                    if version and path:
                        self.browsers[browser_name] = {
                            'version': version,
                            'path': path
                        }
            except (FileNotFoundError, PermissionError, OSError):
                # 注册表项不存在，继续检测下一个
                continue
    
    def detect_from_file_paths(self) -> None:
        """从文件系统中检测浏览器"""
        for browser_name, paths in self.common_paths.items():
            if browser_name in self.browsers:
                continue  # 已经在注册表中找到
                
            for path in paths:
                if os.path.exists(path):
                    # 优先从注册表获取版本
                    version = self.get_version_from_registry(browser_name) or self.get_file_version(path)
                    if version:
                        self.browsers[browser_name] = {
                            'version': version,
                            'path': path
                        }
                    break
    
    def get_version_from_registry(self, browser_name: str) -> Optional[str]:
        """从注册表获取浏览器版本"""
        if browser_name in self.version_registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.version_registry_paths[browser_name]) as key:
                    version = winreg.QueryValueEx(key, 'version')[0]
                    return version
            except (FileNotFoundError, PermissionError, OSError):
                pass
        return None
    
    def get_browser_version(self, browser_name: str, path: str) -> Optional[str]:
        """根据浏览器类型获取版本信息"""
        # 优先从注册表获取版本
        version = self.get_version_from_registry(browser_name)
        if version:
            return version
            
        # 如果注册表中没有，则从文件属性获取
        return self.get_file_version(path)
    
    def get_chrome_version(self, path: str) -> Optional[str]:
        """获取Chrome版本"""
        return self.get_version_from_registry('Chrome') or self.get_file_version(path)
    
    def get_firefox_path(self) -> Optional[str]:
        """获取Firefox路径"""
        for path in self.common_paths['Firefox']:
            if os.path.exists(path):
                return path
        return None
    
    def get_firefox_version(self, path: str) -> Optional[str]:
        """获取Firefox版本"""
        # 直接从文件属性获取，不运行Firefox
        return self.get_file_version(path)
    
    def get_edge_path(self) -> Optional[str]:
        """获取Edge路径"""
        for path in self.common_paths['Edge']:
            if os.path.exists(path):
                return path
        return None
    
    def get_edge_version(self, path: str) -> Optional[str]:
        """获取Edge版本"""
        return self.get_version_from_registry('Edge') or self.get_file_version(path)
    
    def get_opera_path(self) -> Optional[str]:
        """获取Opera路径"""
        for path in self.common_paths['Opera']:
            if os.path.exists(path):
                return path
        return None
    
    def get_opera_version(self, path: str) -> Optional[str]:
        """获取Opera版本"""
        return self.get_file_version(path)
    
    def get_brave_path(self) -> Optional[str]:
        """获取Brave路径"""
        for path in self.common_paths['Brave']:
            if os.path.exists(path):
                return path
        return None
    
    def get_vivaldi_path(self) -> Optional[str]:
        """获取Vivaldi路径"""
        for path in self.common_paths['Vivaldi']:
            if os.path.exists(path):
                return path
        return None
    
    def get_vivaldi_version(self, path: str) -> Optional[str]:
        """获取Vivaldi版本"""
        return self.get_file_version(path)
    
    def get_chrome_based_version(self, path: str) -> Optional[str]:
        """获取基于Chrome的浏览器版本"""
        # 不再执行浏览器，直接使用文件版本信息
        return self.get_file_version(path)
    
    def get_file_version(self, path: str) -> Optional[str]:
        """使用Windows API获取文件版本信息"""
        if sys.platform != 'win32' or not path or not os.path.exists(path):
            return None
            
        try:
            import win32api
            info = win32api.GetFileVersionInfo(path, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
            return version
        except (ImportError, KeyError, AttributeError, OSError):
            # win32api模块不可用或获取版本失败
            try:
                # 使用PowerShell作为备用方法，但不直接运行浏览器
                cmd = f'powershell -command "(Get-Item \'{path}\').VersionInfo.ProductVersion"'
                version = subprocess.check_output(cmd, shell=True, text=True).strip()
                return version
            except subprocess.SubprocessError:
                return None