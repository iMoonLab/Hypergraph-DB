# 安装指南

## 稳定版本

**Hypergraph-DB** 的稳定版本可在 PyPI 上获得。您可以使用 `pip` 安装：

```bash
pip install hypergraph-db
```

## 开发版安装

如需开发或获取最新功能，您可以从 GitHub 仓库安装：

```bash
pip install git+https://github.com/iMoonLab/Hypergraph-DB.git
```

!!! warning "开发版本"
    开发版本可能不稳定且未完全测试。如果您遇到任何错误，请在 [GitHub Issues](https://github.com/iMoonLab/Hypergraph-DB/issues) 中报告。

## 使用 uv（推荐用于开发）

为了更快的依赖管理，我们推荐使用 [uv](https://github.com/astral-sh/uv)：

### 安装 uv

=== "Windows"
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "macOS/Linux"
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### 克隆和设置

```bash
# 克隆仓库
git clone https://github.com/iMoonLab/Hypergraph-DB.git
cd Hypergraph-DB

# 安装开发依赖
uv sync --extra dev

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows
```

## 验证安装

安装完成后，您可以验证 Hypergraph-DB 是否正确安装：

```python
import hyperdb
print(f"Hypergraph-DB 版本: {hyperdb.__version__}")

# 创建一个简单的超图
hg = hyperdb.HypergraphDB()
hg.add_v("A", {"name": "顶点A"})
hg.add_v("B", {"name": "顶点B"})
hg.add_e(("A", "B"), {"type": "连接"})

print(f"超图已创建，包含 {hg.num_v} 个顶点和 {hg.num_e} 条超边")
```

## 系统要求

### 最低要求

- **Python**: >= 3.10
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 推荐 >= 4GB
- **硬盘空间**: >= 100MB

### 推荐配置

- **Python**: 3.11 或 3.12
- **操作系统**: 最新稳定版本
- **内存**: >= 8GB（用于处理大型超图）
- **硬盘空间**: >= 1GB（包括文档和示例）

## 依赖项

Hypergraph-DB 具有最小的核心依赖：

### 核心依赖

```toml
# 无额外依赖 - 纯 Python 实现
```

### 可选依赖

```toml
# 可视化功能（自动安装）
"Flask>=2.0.0"  # Web 服务器
"Jinja2>=3.0.0"  # 模板引擎

# 开发工具
"pytest>=6.0"    # 测试框架
"black"           # 代码格式化
"isort"           # 导入排序
"mkdocs"          # 文档生成
```

## 故障排除

### 常见问题

**问题**: `pip install hypergraph-db` 失败

**解决方案**:
1. 确保您的 Python 版本 >= 3.10
2. 更新 pip: `pip install --upgrade pip`
3. 使用虚拟环境: `python -m venv venv && source venv/bin/activate`

**问题**: 导入错误

**解决方案**:
```python
# 检查安装
pip list | grep hypergraph

# 重新安装
pip uninstall hypergraph-db
pip install hypergraph-db
```

**问题**: 可视化无法工作

**解决方案**:
1. 检查防火墙设置
2. 确保端口 8080 未被占用
3. 手动打开浏览器访问 `http://localhost:8080`

### 获取帮助

如果您遇到安装问题，请：

1. 检查 [GitHub Issues](https://github.com/iMoonLab/Hypergraph-DB/issues)
2. 创建新的 issue，包含：
   - Python 版本
   - 操作系统信息
   - 完整的错误信息
   - 安装步骤

## 下一步

安装完成后，查看以下资源开始使用：

- **[快速开始](quickstart.zh.md)**: 基本用法和示例
- **[超图基础](hypergraph-basics.zh.md)**: 了解超图概念
- **[API 参考](../api/index.zh.md)**: 完整的 API 文档
- **[可视化指南](../visualization/index.zh.md)**: 交互式可视化功能
