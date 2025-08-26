# Pycharm Settings
- -n: New
- -e: Every Time
---
## Settings → Project
### Python Interpreter
    1. Settings → Project:[项目名] →  Python Interpreter
    2. Python Interpreter → 点击 → Show All…
    3. + → Add Local Interpreter…
    4. Select existing → Python path: ..\.venv\Scripts\python.exe → OK
    5. 右键刚刚 Add 的 Interpreter → Rename
---
## Other
### pip
    pip install package_name
    pip install --upgrade package_name
    pip show package_name
    pip uninstall package_name
    pip show package_name
    pip list
    pip freeze > requirements.txt
    pip install -r requirements.txt
    pip cache purge
### pipdeptree
    # 完整依赖树
    pipdeptree
    # 查看指定包的依赖
    pipdeptree -p package_name
    # 查看指定包被哪些依赖
    pipdeptree -r -p package_name
---
