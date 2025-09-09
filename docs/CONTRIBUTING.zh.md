# 为 Hypergraph-DB 做贡献

感谢您对为 Hypergraph-DB 做贡献的兴趣！我们欢迎社区的贡献，并感谢您帮助我们让这个项目变得更好。

##  行为准则

本项目和所有参与者都受我们的行为准则约束。通过参与，您需要遵守此准则。

## 🤝 如何贡献

有多种方式为 Hypergraph-DB 做贡献：

- 🐛 **报告错误** - 帮助我们识别和修复问题
- 💡 **建议功能** - 分享新功能的想法
- 📖 **改进文档** - 帮助我们的文档更清晰、更全面
- 🔧 **提交代码** - 修复错误或实现新功能
- 🧪 **编写测试** - 帮助提高我们的测试覆盖率
- 🌐 **翻译** - 帮助项目支持更多语言

## 🛠️ 开发环境设置

### 前提条件

- Python 3.8 或更高版本
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip
- Git

### 设置开发环境

1. **Fork 并克隆仓库**:
   ```bash
   git clone https://github.com/your-username/Hypergraph-DB.git
   cd Hypergraph-DB
   ```

2. **安装依赖**:
   ```bash
   # 使用 uv（推荐）
   uv sync
   
   # 或使用 pip
   pip install -e ".[dev]"
   ```

3. **运行测试确保一切正常**:
   ```bash
   # 使用 uv
   uv run pytest
   
   # 或使用 pip
   pytest
   ```

4. **设置 pre-commit 钩子**（可选但推荐）:
   ```bash
   uv run pre-commit install
   ```

## 📤 提交更改

### Pull Request 流程

1. **从 `main` 创建新分支**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **根据我们的风格指南进行更改**

3. **为新功能添加测试**

4. **如需要，更新文档**

5. **运行测试并确保通过**:
   ```bash
   uv run pytest
   ```

6. **运行类型检查**:
   ```bash
   uv run mypy hyperdb
   ```

7. **格式化您的代码**:
   ```bash
   uv run black hyperdb tests
   uv run isort hyperdb tests
   ```

8. **提交更改并使用清晰的消息**:
   ```bash
   git commit -m "feat: 添加新的超图算法"
   ```

9. **推送您的分支**:
   ```bash
   git push origin feature/your-feature-name
   ```

10. **在 GitHub 上创建 Pull Request**

### 提交消息指南

我们遵循[约定式提交](https://www.conventionalcommits.org/)规范：

- `feat:` - 新功能
- `fix:` - 错误修复
- `docs:` - 仅文档更改
- `style:` - 不影响代码含义的更改
- `refactor:` - 既不修复错误也不添加功能的代码更改
- `test:` - 添加缺失测试或修正现有测试
- `chore:` - 构建过程或辅助工具的更改

## 🐛 报告问题

报告问题时，请包含：

1. **错误描述**: 清楚描述问题
2. **环境**: Python 版本、操作系统、包版本
3. **重现步骤**: 能重现问题的最小代码示例
4. **期望行为**: 您期望发生什么
5. **实际行为**: 实际发生了什么
6. **堆栈跟踪**: 如果适用，包含完整的错误消息

请在报告问题时提供尽可能详细的信息。

## 📖 文档

我们使用 [MkDocs](https://www.mkdocs.org/) 和 Material 主题来编写文档：

### 本地构建文档

```bash
# 安装文档依赖
uv sync --extra docs

# 本地服务文档
uv run mkdocs serve

# 构建文档
uv run mkdocs build
```

### 文档指南

- 编写清晰、简洁的说明
- 为新功能包含代码示例
- 尽可能同时更新中英文版本
- 使用正确的 Markdown 格式
- 在有帮助时添加图表或图像

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行带覆盖率的测试
uv run pytest --cov=hyperdb

# 运行特定测试文件
uv run pytest tests/test_hypergraph.py

# 运行匹配模式的测试
uv run pytest -k "test_add_vertex"
```

### 编写测试

- 为所有新功能编写测试
- 使用描述性测试名称
- 遵循现有测试结构
- 包含边界情况和错误条件
- 力求高测试覆盖率

### 测试结构

```python
def test_feature_name():
    """测试描述。"""
    # 准备
    hg = HypergraphDB()
    
    # 执行
    result = hg.some_method()
    
    # 断言
    assert result == expected_value
```

## 📝 代码风格指南

### Python 代码风格

我们使用以下工具来维护代码质量：

- **[Black](https://black.readthedocs.io/)** - 代码格式化
- **[isort](https://pycqa.github.io/isort/)** - 导入排序
- **[mypy](https://mypy.readthedocs.io/)** - 类型检查
- **[flake8](https://flake8.pycqa.github.io/)** - 代码检查

### 代码指南

1. **类型提示**: 为所有公共 API 使用类型提示
2. **文档字符串**: 遵循 [NumPy 文档字符串风格](https://numpydoc.readthedocs.io/en/latest/format.html)
3. **变量名**: 使用描述性名称（`vertex_id` 而不是 `vid`）
4. **函数名**: 函数使用动词（`add_vertex` 而不是 `vertex_add`）
5. **类名**: 使用 PascalCase（`HypergraphDB`）
6. **常量**: 使用 UPPER_SNAKE_CASE（`MAX_VERTICES`）

### 文档字符串示例

```python
def add_vertex(self, vertex_id: Hashable, attributes: Optional[Dict[str, Any]] = None) -> None:
    """向超图添加顶点。

    Parameters
    ----------
    vertex_id : Hashable
        顶点的唯一标识符。
    attributes : dict, optional
        顶点属性字典，默认为 None。

    Raises
    ------
    ValueError
        如果 vertex_id 已在超图中存在。

    Examples
    --------
    >>> hg = HypergraphDB()
    >>> hg.add_vertex(1, {"name": "Alice", "age": 30})
    """
```

## 🏷️ 发布流程

发布由维护者处理，遵循语义版本控制：

- **主版本** (X.0.0): 破坏性更改
- **次版本** (0.X.0): 新功能，向后兼容
- **补丁版本** (0.0.X): 错误修复，向后兼容

## 🙋 获取帮助

如果您需要帮助或有疑问：

1. 查看[文档](https://imoonlab.github.io/Hypergraph-DB/)
2. 搜索[现有问题](https://github.com/iMoonLab/Hypergraph-DB/issues)
3. 创建[新讨论](https://github.com/iMoonLab/Hypergraph-DB/discussions)
4. 加入我们的社区频道（如果可用）

## 📄 许可证

通过为 Hypergraph-DB 做贡献，您同意您的贡献将在 Apache License 2.0 下获得许可。

---

感谢您为 Hypergraph-DB 做贡献！🚀
