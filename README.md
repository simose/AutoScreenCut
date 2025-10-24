# AutoScreenCut - 自动化网页截图测试工具

## 项目简介

AutoScreenCut 是一个基于 Python + Playwright 框架开发的自动化网页截图测试工具。该工具能够自动访问指定网页，进行全页面滚动截图，并生成详细的测试报告。项目采用 Page Object Model (PO模式) 设计，具有良好的代码结构和可维护性。

## 功能特性

- 🌐 **多URL支持**: 支持批量测试多个网页URL
- 📸 **智能截图**: 自动滚动页面进行分段截图，确保完整页面覆盖
- 🎯 **A/B测试支持**: 支持A/B类型标记，便于对比测试
- 🚫 **弹窗处理**: 自动识别并关闭常见弹窗（Cookie同意、订阅等）
- 📊 **报告生成**: 自动生成HTML格式的测试报告
- ⚙️ **配置化管理**: 集中配置管理，易于维护和修改
- 🔄 **PO模式设计**: 采用Page Object Model，代码结构清晰

## 项目结构

```
AutoScreenCut/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   └── config.py          # 项目配置文件
├── pages/                  # 页面对象目录
│   ├── __init__.py
│   └── base_page.py       # 基础页面类
├── tests/                  # 测试用例目录
│   ├── __init__.py
│   └── test_screenshots.py # 截图测试用例
├── utils/                  # 工具类目录
│   ├── __init__.py
│   └── report_generator.py # 报告生成器
├── run_tests.py           # 测试运行脚本
├── run_tests.bat          # Windows批处理运行脚本
└── README.md              # 项目说明文档
```

## 环境要求

- **Python 3.7+**
- **Node.js 16+** (Playwright依赖)
- **Playwright**
- **pytest**

## 安装步骤

### 1. 克隆项目
```bash
git clone <项目地址>
cd AutoScreenCut
```

### 2. 创建Python虚拟环境
```bash
# 使用指定的虚拟环境路径
D:\Cursor\UK0519\.venv\Scripts\activate
```

### 3. 安装Python依赖
```bash
pip install playwright pytest allure-pytest
```

### 4. 安装Playwright浏览器
```bash
# 安装Playwright浏览器（需要Node.js环境）
playwright install chromium
# 或者安装所有浏览器
playwright install


## 配置说明

### 修改配置文件 `config/config.py`

```python
# 测试URL配置
URLS = [
    "https://www.jackery.com/",
    "https://www.jackery.com/products/jackery-explorer-5000-plus",
    # 添加更多需要测试的URL
]

# 截图路径配置
SCREENSHOTS_DIR = "D:\\AutoScreenCut"

# 报告路径配置
REPORTS_DIR = "D:\\AutoScreenCut\\reports"
```

### 配置项说明

- **URLS**: 需要测试的网页URL列表
- **SCREENSHOTS_DIR**: 截图保存目录

## 使用方法

### 方法一：使用批处理脚本（推荐）

双击运行 `run_tests.bat` 文件，脚本会自动：
1. 激活虚拟环境
2. 运行测试用例
3. 生成Allure报告
4. 自动打开测试报告

### 方法二：使用Python脚本

```bash
python run_tests.py
```

### 方法三：直接使用pytest

```bash
pytest tests/test_screenshots.py -v
```

## 测试流程

1. **启动测试**: 运行测试脚本
2. **输入类型**: 根据提示输入截图类型（A或B）
3. **自动执行**: 
   - 打开浏览器
   - 访问配置的URL
   - 最大化窗口
   - 等待2秒加载
   - 关闭弹窗
   - 开始滚动截图
4. **生成报告**: 自动生成HTML测试报告

## 截图命名规则

截图文件按以下格式命名：
- 主页: `homepage_YYYYMMDD_A/B_001.png`
- 其他页面: `页面名称_A/B_001.png`

例如：
- `homepage_20241201_A_001.png`
- `jackery_explorer_5000_plus_B_001.png`


## 自定义配置

### 修改截图路径
在 `config/config.py` 中修改 `SCREENSHOTS_DIR` 变量：
```python
SCREENSHOTS_DIR = "你的截图保存路径"
```

### 添加新的测试URL
在 `config/config.py` 中的 `URLS` 列表添加新URL：
```python
URLS = [
    "https://www.jackery.com/",
    "https://你的新URL.com",
]
```

### 修改等待时间
在 `tests/test_screenshots.py` 中修改等待时间：
```python
base_page.wait(2)  # 修改为需要的秒数
```

## 故障排除

### 常见问题

1.  **浏览器启动失败**
   - 确保已安装Playwright浏览器：`playwright install`
   - 检查虚拟环境是否正确激活
   - 如果Playwright安装失败，可能是Node.js环境问题

2. **Playwright安装失败**
   - 确保Node.js环境正常
   - 尝试重新安装：`pip uninstall playwright && pip install playwright`
   - 然后重新安装浏览器：`playwright install chromium`

3. **截图保存失败**
   - 检查截图目录是否存在写入权限
   - 确保磁盘空间充足

4. **弹窗关闭失败**
   - 某些特殊弹窗可能需要手动处理
   - 可以在 `base_page.py` 中添加新的选择器

## 开发说明

### 代码结构
- **PO模式**: 采用Page Object Model设计模式
- **配置分离**: 配置与代码分离，便于维护
- **模块化设计**: 功能模块化，易于扩展

### 扩展功能
如需添加新功能，可以：
1. 在 `pages/base_page.py` 中添加新的页面操作方法
2. 在 `tests/` 目录下添加新的测试用例
3. 在 `utils/` 目录下添加新的工具类

## 版本信息

- **当前版本**: 1.0.0
- **Python版本**: 3.7+
- **Playwright版本**: 最新稳定版
- **pytest版本**: 最新稳定版

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。

---

**注意**: 使用前请确保已正确配置虚拟环境和依赖包，并检查目标网站的访问权限。
