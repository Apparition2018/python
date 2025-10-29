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
    Tasks: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/index.html
    # 显示详细信息
    conda info

    # 创建环境，并安装指定包
    conda create -n <env> -y <package>=<version>
    # 复制环境
    conda create -n <env> --clone <existed_env>
    # 在指定的路径创建环境，并安装指定包
    conda create -p <path> <package>=<version> 
    # 导出 YAML
    conda export > environment.yml
    # 根据 environment.yml 创建环境
    conda env create -f environment.yml
    # 切换环境
    conda activate <env>
    # 停用环境
    conda deactivate
    # 显示已创建环境
    conda info -e
    conda env list
    # 重命名环境
    conda rename -n <env> <new_env>
    # 移除环境
    conda remove -n <env> --all
    conda env remove -n <env>

    # 查看指定包是否可安装
    conda search <package>
    # 安装指定包
    #   ① conda install -n <env> <package>=<version>
    #   ② 从 anaconda.org 安装
    #   ③ conda install -c conda-forge <package>
    #   ④ pip install <package>
    # 更新指定环境下的指定包到当前版本
    conda update -n <env> <package>
    # 更新所有包
    conda update --all
    # 根据 environment.yml 安装包
    conda env update -f environment.yml
    # 移除指定环境的指定包
    conda remove -n <env> <package>
---
