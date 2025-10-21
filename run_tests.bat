@echo off
chcp 65001 >nul
title UI自动化测试执行器

echo ================================================
echo            UI自动化测试执行器
echo          Python + Playwright 框架
echo ================================================
echo.

REM 激活虚拟环境
echo 正在激活虚拟环境...
call "D:\Cursor\UK0519\.venv\Scripts\activate.bat"

REM 切换到项目目录
cd /d "D:\Cursor\001"

REM 运行Python脚本
echo 开始执行测试...
python run_tests.py

REM 自动退出，不暂停
timeout /t 3 /nobreak >nul
