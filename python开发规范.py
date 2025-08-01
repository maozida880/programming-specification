# -*- coding: utf-8 -*-

## **捷停车 Python 开发规范 **

### **引言**

欢迎加入！在捷停车公司，Python 在后端服务、数据科学、自动化运维等领域扮演着至关重要的角色。代码的质量直接决定了产品的稳定性和团队的开发效率。

本规范不仅仅是一系列规则，更是一种专业的开发哲学。遵循它，你的代码将变得更易读、更易维护、更健壮，从而让你和你的团队都能更高效地工作。**记住：代码的生命周期中，被阅读的次数远超被编写的次数。**

-----

### **一、代码风格与格式 (PEP 8)**

我们遵循 [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) 作为代码风格的黄金标准。以下是其中最核心、必须遵守的几点。

**强烈建议：** 安装并配置代码格式化工具 `Black` 和 `isort`，它们可以自动帮你处理大部分格式问题。

#### **1.1 命名规范 (Naming Conventions)**

清晰的命名是代码自解释能力的基础。

  * **变量、函数、方法:** `snake_case` (小写字母 + 下划线)

      * **推荐:** `user_name`, `calculate_shipping_cost()`
      * **禁止:** `UserName`, `calculateShippingCost()`

  * **类 (Class):** `PascalCase` (或称 `CapWords`)

      * **推荐:** `class UserProfile:`, `class AccountBalance:`
      * **禁止:** `class user_profile:`, `class userprofile:`

  * **常量 (Constant):** `ALL_CAPS` (全大写 + 下划线)

      * **推荐:** `MAX_OVERFLOW_CONNECTIONS = 10`
      * **禁止:** `max_overflow_connections = 10`

  * **模块与包 (Module & Package):** `short_lowercase` (简短、全小写)

      * **推荐:** `import utils.http_client`
      * **禁止:** `import Utils.HttpClient`

#### **1.2 缩进与换行**

  * **缩进:** 使用 **4个空格** 作为一级缩进。**禁止** 使用 Tab 键。

  * **行长度:** 每行代码建议不超过 **88个字符** (Black 默认) 或 99个字符。对于过长的代码行，应在操作符后、逗号后或括号内进行换行。

  * **示例:**
"""

# 推荐的换行方式
    def long_function_name(
        var_one, var_two,
        var_three, var_four
    ):
        print(var_one)

    income = (
        gross_wages
        + taxable_interest
        + (dividends - qualified_dividends)
        - ira_deduction
        - student_loan_interest
    )

"""#### **1.3 导包规范 (Imports)**

  * **顺序:** 导包应分组，并按以下顺序排列，组间空一行：

    1.  标准库 (`os`, `sys`, `datetime`)
    2.  第三方库 (`requests`, `pandas`)
    3.  本地应用/项目库 (`from my_project import api`)

  * **格式:** 每个 `import` 只导入一个模块。

  * **示例:**
"""

# 不推荐
    import os, sys, requests, my_project

    # 推荐 (使用 isort 工具可自动格式化)
    import os
    import sys
    from datetime import datetime

    import requests
    import pandas as pd

    from my_project.models import User
    from my_project.utils import get_db_connection

"""#### **1.4 空格的使用**

在二元操作符两侧、逗号后、`#` 注释后都应有一个空格。
"""

# 推荐
x = 1
y = x * 2 + 1
my_list = [1, 2, 3]
print(x, y)  # 打印 x 和 y 的值

# 不推荐
x=1
y=x*2+1
my_list=[1,2,3]
print(x,y)#打印x和y的值

"""-----

### **二、注释与文档字符串 (Comments & Docstrings)**

注释解释“为什么”，文档解释“做什么”。

#### **2.1 行内/块注释**

用于解释复杂算法、业务逻辑或代码的“陷阱”。
"""

# 这是一个块注释，解释下面这段复杂逻辑的目的。
# 我们需要先计算用户的信用分，然后再决定是否批准贷款。
# 信用分的计算参考了央行 xyz 模型。
credit_score = calculate_score(user_id)

# 这是一个行内注释
# 为了防止除零错误，这里设置一个默认值
if divisor == 0:
    divisor = 1

"""#### **2.2 文档字符串 (Docstrings - PEP 257)**

**所有** 的公共模块、类、函数和方法都 **必须** 有 Docstring。我们推荐使用 **Google 风格** 的 Docstring。

  * **格式:**

      * 单行总结。
      * 空一行。
      * (可选) 更详细的描述。
      * `Args:`: 描述每个参数，包括名称、类型和说明。
      * `Returns:`: 描述返回值，包括类型和说明。
      * `Raises:`: (可选) 描述可能抛出的异常。

  * **示例:**
"""

def fetch_user_data(user_id: int, include_profile: bool = False) -> dict:
        """根据用户ID获取用户数据。

        如果用户不存在，将抛出异常。可以指定是否包含详细的个人资料。

        Args:
            user_id (int): 用户的唯一ID。
            include_profile (bool): 是否在返回结果中包含个人资料。默认为 False。

        Returns:
            dict: 包含用户基本信息的字典。如果 include_profile 为 True，
                  还会包含 "profile" 键。

        Raises:
            ValueError: 如果 user_id 不存在。
        """
        # ... 函数实现 ...
        if not user_exists(user_id):
            raise ValueError(f"User with ID {user_id} not found.")

        # ... more code ...

"""**好处:** 良好的 Docstring 不仅方便人阅读，还可以被IDE、文档生成工具（如 Sphinx）自动提取，形成项目文档。

-----

### **三、编程最佳实践 (Best Practices)**

#### **3.1 明确与简洁 (Clarity & Simplicity)**

  * **一个函数只做一件事 (Single Responsibility Principle):** 函数应该短小精悍，功能单一。

  * **避免魔术数字 (Magic Numbers):** 使用常量代替硬编码在代码里的数字或字符串。
"""

# 不推荐
    if user.status == 2:  # 2 是什么意思？
        # ...

    # 推荐
    STATUS_APPROVED = 2
    if user.status == STATUS_APPROVED:
        # ...

"""#### **3.2 错误处理 (Error Handling)**

  * **使用 `try...except` 处理可能发生的异常**，如文件操作、网络请求、数据库访问。

  * **`except` 要具体，不要裸奔:** 永远不要使用裸的 `except:`，它会捕获所有异常，包括 `SystemExit` 和 `KeyboardInterrupt`，隐藏真正的错误。
"""

# 不推荐
    try:
        response = requests.get("https://api.example.com/data")
        data = response.json()
    except: # 捕获了所有异常，无法区分是网络问题还是JSON解析问题
        print("An error occurred.")

    # 推荐
    try:
        response = requests.get("https://api.example.com/data")
        response.raise_for_status()  # 检查HTTP错误
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

"""#### **3.3 上下文管理器 (`with` 语句)**

对于文件、数据库连接、锁等需要“获取”和“释放”的资源，**必须** 使用 `with` 语句，它能保证资源被正确关闭，即使在发生异常时也是如此。
"""

# 推荐
with open("my_file.txt", "w") as f:
    f.write("Hello, world!")
# 文件在这里会自动关闭

# 不推荐
f = open("my_file.txt", "w")
f.write("Hello, world!")
f.close() # 如果上一行代码出错，这一行将不会被执行

"""#### **3.4 善用数据结构**

  * **列表推导式 (List Comprehensions):** 优先使用列表推导式来创建列表，它比 `for` 循环更简洁、通常也更快。
"""

# 推荐
    squares = [x**2 for x in range(10) if x % 2 == 0]

    # 不推荐
    squares = []
    for x in range(10):
        if x % 2 == 0:
            squares.append(x**2)

"""* **选择正确的数据结构:**

      * `list`: 有序集合，元素可重复。
      * `tuple`: 不可变的 `list`，用作函数返回值、字典的键等。
      * `dict`: 键值对集合，用于高效的查找 (O(1))。
      * `set`: 无序集合，元素唯一。用于去重和成员资格测试。

-----

### **四、项目结构与环境管理**

#### **4.1 虚拟环境 (Virtual Environments)**

**所有** 项目都 **必须** 在其独立的虚拟环境中开发。这可以隔离不同项目的依赖，避免版本冲突。

  * **创建:** `python -m venv venv`
  * **激活 (macOS/Linux):** `source venv/bin/activate`
  * **激活 (Windows):** `.\venv\Scripts\activate`

#### **4.2 依赖管理**

  * 项目的所有依赖都必须记录在 `requirements.txt` 文件中。
  * **生成:** `pip freeze > requirements.txt`
  * **安装:** `pip install -r requirements.txt`

#### **4.3 项目目录结构**

一个典型的Python项目结构如下：

```
my_awesome_project/
├── .gitignore          # Git忽略文件配置
├── README.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── venv/               # 虚拟环境目录 (应被 .gitignore 忽略)
├── my_awesome_project/   # 源代码包
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── user.py
│   └── utils/
│       ├── __init__.py
│       └── db.py
└── tests/              # 测试代码
    ├── __init__.py
    └── test_user_api.py
```

-----

### **五、测试 (Testing)**

“没有经过测试的代码都是不可信的。”

  * **单元测试:** 新人应学习使用 `pytest` 或 `unittest` 框架为自己编写的核心函数和类编写单元测试。
  * **习惯:** 养成编写测试的习惯，这会大大提高你的代码质量和重构时的信心。

<!-- end list -->
"""

# tests/test_math.py
from my_awesome_project.utils import math_tools

def test_add_positive_numbers():
    """测试两个正数相加"""
    assert math_tools.add(2, 3) == 5

def test_add_negative_numbers():
    """测试两个负数相加"""
    assert math_tools.add(-2, -3) == -5

"""-----

### **六、版本控制 (Git)**

  * **提交信息 (Commit Message):** 提交信息必须清晰、有意义。推荐使用 `类型: 描述` 的格式。
      * `feat: Add user registration API` (新功能)
      * `fix: Correct password validation logic` (修复Bug)
      * `docs: Update README with setup instructions` (文档修改)
      * `refactor: Improve database connection handling` (代码重构)
  * **分支策略:** 遵循团队的分支策略，通常是在自己的 `feature/xxx` 分支上开发，完成后提交 Merge Request (或 Pull Request)。

-----

### **结语**

编写符合规范的、高质量的代码，是对自己、对团队、对产品负责的表现。一开始可能会觉得有些束缚，但当你习惯之后，会发现它能让你免于许多低级错误和后期维护的痛苦，从而将更多精力投入到创造性的工作中。

**从你的第一行代码开始，就以专业的标准要求自己！**
"""
