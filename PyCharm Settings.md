# PyCharm Settings
- j: JetBrains
- n: New
- e: Every Time
- o: Optional
---
## Settings → Python
### Interpreter
    1. Settings → Python → Interpreter
    2. Python Interpreter → 点击 → Show All…
    3. + → Add Local Interpreter…
        3.1 Generate new
            3.1.1 Type: Virtualenv
            3.1.2 Base python: D:\miniconda3\python.exe
            3.1.3 Location: ..\.venv\Scripts\python.exe
        3.2 Select existing
            3.2.1 Type: Conda
            3.2.2 Path to conda: D:\miniconda3\Scripts\conda.exe
            3.2.3 Environment: py314
    4. 右键刚刚 Add 的 Interpreter → Rename
## Settings → Tools
### Terminal (-jno)
    1. Settings → Tools → Terminal
    2. Shell path: cmd.exe "/K" "D:\miniconda3\Scripts\activate.bat"
    3. Default tab name: miniconda3
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
### [Configuration](https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/index.html)
    conda config --prepend channels conda-forge
    conda config --set channel_priority strict
    conda config --append create_default_packages pytest-asyncio
    conda config --append create_default_packages requests
    conda config --append create_default_packages pandas
    conda config --append create_default_packages pandas-stubs
### [Tasks](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/index.html)
#### conda
    # 显示当前 conda 安装信息
    conda info
    # 显示 conda 版本
    conda --version
    # 更新 conda 至当前版本
    conda update -n base conda
#### environments
    # 创建环境，并安装指定版本的包
    conda create -n <env> <package>=<version>
    # 创建环境，并不安装默认包
    conda create --no-default-packages -n <env> <package>
    # 根据 environment.yml 创建环境
    conda env create -f environment.yml
    # 在指定路径创建环境
    conda create -p <path> <package>
    # 根据 environment.yml 更新环境，并移除未定义在文件里的包
    conda env update -f environment.yml --prune
    # 克隆环境
    conda create -n <env> --clone <existed_env>
    # 根据 spec-file.txt 创建环境，或安装包
    conda list --explicit > spec-file.txt
    conda create -n <env> --file spec-file.txt[.conda_envs_dir_test](../../../miniconda3/envs/.conda_envs_dir_test)
    conda install -n <env> --file spec-file.txt

    # 激活环境
    conda activate <env>
    # 停用环境
    conda deactivate

    # 显示所有环境
    conda info -e --json
    conda env list

    # 重命名环境
    conda rename -n <env> <new_env>

    # 将环境导出为 YAML
    conda export > environment.yml
    conda env export > environment.yml
    conda export -n <env> -f=environment.yml
    conda export -n <env> --format=yml
    # 将环境导出为 YAML，只记录显式 conda install 的包，排除平台指定依赖
    conda export --from-history > environment.yml

    # 列出修订历史
    conda list --revisions
    # 恢复到指定修订版本
    conda install --revision=REVNUM

    # 移除环境
    conda remove -n <env> --all
    conda env remove -n <env>
#### channels
    # 在通道列表顶部添加新通道，使其成为最高优先级
    conda config --prepend channels <new_channel>
    # 只从最高优先级的通道安装包及其依赖
    conda config --set channel_priority strict
#### packages
    # 查看指定包在指定通道是否可供安装
    conda search -c <channel> <package>
    # 安装包
    #   ① conda install -n <env> -c <channel> <package>=<version>
    #   ② http://anaconda.org
    #   ③ pip install <package>
    # 列出指定环境已安装的包
    conda list -n <env> <package>1
    # 更新指定环境的指定包到最新的兼容版本
    conda update -n <env> <package>
    # 更新所有包
    conda update --all
    # 配置在创建环境时默认安装的包
    conda config --append create_default_packages <package>
    # 移除指定环境的指定包
    conda remove -n <env> <package>
---
