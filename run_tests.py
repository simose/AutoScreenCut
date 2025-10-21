#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI自动化测试执行脚本
使用Python + Playwright框架进行网站截图测试
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("           UI自动化测试执行器")
    print("         Python + Playwright 框架")
    print("=" * 60)
    print()

def check_virtual_env():
    """检查虚拟环境是否激活"""
    venv_path = r"D:\Cursor\UK0519\.venv"
    if not os.path.exists(venv_path):
        print(f"❌ 虚拟环境路径不存在: {venv_path}")
        return False
    
    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 虚拟环境已激活")
        return True
    else:
        print("⚠️  虚拟环境未激活，尝试激活...")
        return activate_venv()

def activate_venv():
    """激活虚拟环境"""
    venv_script = r"D:\Cursor\UK0519\.venv\Scripts\activate.bat"
    if os.path.exists(venv_script):
        print("✅ 虚拟环境脚本存在")
        return True
    else:
        print(f"❌ 虚拟环境激活脚本不存在: {venv_script}")
        return False

def check_dependencies():
    """检查必要的依赖包"""
    required_packages = ['pytest', 'playwright']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n需要安装的包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        if 'playwright' in missing_packages:
            print("playwright install chromium")
        return False
    
    return True

def check_playwright_browsers():
    """检查Playwright浏览器是否安装"""
    try:
        result = subprocess.run(['playwright', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Playwright 浏览器已安装")
            return True
        else:
            print("❌ Playwright 浏览器未安装")
            print("请运行: playwright install chromium")
            return False
    except Exception as e:
        print(f"❌ 检查Playwright浏览器时出错: {e}")
        return False

def create_screenshot_dir():
    """创建截图目录"""
    screenshot_dir = r"D:\AutoScreenCut"
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        print(f"✅ 截图目录已准备: {screenshot_dir}")
        return True
    except Exception as e:
        print(f"❌ 创建截图目录失败: {e}")
        return False

def run_tests():
    """运行测试"""
    print("\n🚀 开始执行测试...")
    print("-" * 40)
    
    # 切换到项目目录
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"📁 工作目录: {project_dir}")
    
    # 执行pytest命令
    cmd = [sys.executable, "-m", "pytest", "tests/test_screenshots.py", "-v", "-s"]
    
    try:
        print("📋 执行命令:", " ".join(cmd))
        print()
        
        # 运行测试
        result = subprocess.run(cmd, 
                              capture_output=False,  # 实时显示输出
                              text=True,
                              cwd=project_dir)
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print("🎉 测试执行成功！")
        else:
            print("❌ 测试执行失败！")
            print(f"返回码: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 执行测试时出错: {e}")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    print("🔍 检查运行环境...")
    if not check_virtual_env():
        print("❌ 虚拟环境检查失败，请手动激活虚拟环境后重试")
        return 1
    
    if not check_dependencies():
        print("❌ 依赖包检查失败，请安装必要的包后重试")
        return 1
    
    if not check_playwright_browsers():
        print("❌ Playwright浏览器检查失败，请安装浏览器后重试")
        return 1
    
    if not create_screenshot_dir():
        print("❌ 截图目录创建失败")
        return 1
    
    print("\n✅ 环境检查完成，所有依赖都已就绪！")
    
    # 运行测试
    success = run_tests()
    
    # 显示结果
    print("\n" + "=" * 60)
    if success:
        print("🎊 所有测试已完成！")
        print("📸 截图已保存到: D:\\AutoScreenCut")
    else:
        print("💥 测试执行过程中出现错误")
    
    print("=" * 60)
    
    # 自动退出，不等待用户输入
    print("\n⏰ 3秒后自动退出...")
    time.sleep(3)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        sys.exit(1)
