# Pycharm Settings
- j: JetBrains
- n: New
- e: Every Time
- o: Optional
---
## Settings → Project
### Python Interpreter
    1. Settings → Project:[项目名] →  Python Interpreter
    2. Python Interpreter → 点击 → Show All…
    3. + → Add Local Interpreter…
    4. Generate new
        4.1 Type: Virtualenv
        4.2 Base python: D:\anaconda3\python.exe
        4.3 Location: ..\.venv\Scripts\python.exe
    5. 右键刚刚 Add 的 Interpreter → Rename
## Settings → Tools
### Terminal (-jno)
    1. Settings → Tools → Terminal
    2. Shell path: cmd.exe "/K" "D:\miniconda3\Scripts\activate.bat"
---
## pip
    pip install package_name
    pip install --upgrade package_name
    pip show package_name
    pip uninstall package_name
    pip show package_name
    pip list
    pip freeze > requirements.txt
    pip install -r requirements.txt
    pip cache purge
---
## pipdeptree
    # 完整依赖树
    pipdeptree
    # 查看指定包的依赖
    pipdeptree -p package_name
    # 查看指定包被哪些依赖
    pipdeptree -r -p package_name
---
## [anaconda](https://www.anaconda.com/docs/getting-started/getting-started)
### [Conda Commands](https://docs.conda.io/projects/conda/en/stable/commands/index.html)
    # 创建一个 Conda 环境，并安装指定包
    conda create -n <env_name> -y <package_name>=<version>
    # 切换当前终端会话的 Conda 环境
    conda activate <env_name>
    conda info --envs
    conda env list
    conda env remove -n <env_name>
---
