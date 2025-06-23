# 浏览器检测工具

这是一个完全由AI写的程序，没什么卵用

一个用于检测系统中安装的浏览器及其版本的Python工具。

## 功能

- 检测系统中安装的所有常见浏览器
- 获取浏览器版本信息
- 提供图形用户界面(GUI)和命令行界面(CLI)
- 支持启动检测到的浏览器

## 支持的浏览器

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Opera
- Brave Browser
- Vivaldi

## 安装依赖:

```bash
pip install -r requirements.txt
```

## 使用方法

### 图形用户界面(GUI)

启动GUI模式:

```bash
python -m browser_detector.main
```

或:

```bash
python -m browser_detector.main --gui
```

### 命令行界面(CLI)

启动CLI模式:

```bash
python -m browser_detector.main --cli
```

CLI选项:

- `-j, --json`: 以JSON格式输出结果
- `-l, --launch BROWSER`: 启动指定的浏览器 (例如: chrome, firefox)
- `-a, --all`: 显示所有详细信息

例如:

```bash
# 显示详细信息
python -m browser_detector.main --cli --all

# 以JSON格式输出
python -m browser_detector.main --cli --json

# 启动Chrome浏览器
python -m browser_detector.main --cli --launch chrome
```

## 系统要求

- Windows 系统
- Python 3.6+
