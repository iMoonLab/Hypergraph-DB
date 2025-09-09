# Hypergraph-DB

<div align="center">
  <img src="../assets/logo.svg" alt="Hypergraph-DB Logo" width="200"/>
</div>

[![PyPI version](https://img.shields.io/pypi/v/hypergraph-db?color=purple)](https://pypi.org/project/hypergraph-db/)
[![Python](https://img.shields.io/pypi/pyversions/hypergraph-db?color=purple)](https://pypi.org/project/hypergraph-db/)
[![License](https://img.shields.io/github/license/iMoonLab/Hypergraph-DB?color=purple)](https://github.com/iMoonLab/Hypergraph-DB/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/iMoonLab/Hypergraph-DB?color=purple)](https://github.com/iMoonLab/Hypergraph-DB)

Hypergraph-DB 是一个轻量级、灵活且基于 Python 的数据库，专为建模和管理**超图**而设计——这是一种广义的图结构，其中边（超边）可以连接任意数量的顶点。这使得 Hypergraph-DB 成为在各种领域（如知识图谱、社交网络和科学数据建模）中表示实体间复杂关系的理想解决方案。

## ✨ 特性

- **🚀 轻量快速**: 纯 Python 实现，依赖最少
- **🔗 超图支持**: 原生支持连接多个顶点的超边
- **💾 持久化**: 内置序列化和加载功能
- **📊 可视化**: 在 Web 浏览器中进行交互式超图可视化
- **🔍 灵活查询**: 丰富的顶点和超边查询功能
- **🛠️ 简单 API**: 直观易用的接口

## 🎯 使用场景

- **知识图谱**: 建模实体间的复杂关系
- **社交网络**: 表示群体交互和多方关系
- **科学数据**: 在研究数据中建模复杂依赖关系
- **推荐系统**: 捕获用户、物品和上下文之间的多路交互

## 📈 性能

Hypergraph-DB 专为高效性而设计。以下是一些性能基准测试：

| 顶点数 | 超边数 | 添加顶点 | 添加边 | 查询时间 | 总时间 |
|--------|--------|----------|--------|----------|--------|
| 100,000  | 20,000     | 0.12s    | 0.17s  | 0.04s    | 0.58s  |
| 500,000  | 100,000    | 0.85s    | 1.07s  | 0.22s    | 3.34s  |
| 1,000,000| 200,000    | 1.75s    | 1.82s  | 0.51s    | 6.60s  |

## 🚀 快速开始

### 安装

```bash
pip install hypergraph-db
```

### 基本用法

```python
from hyperdb import HypergraphDB

# 创建超图
hg = HypergraphDB()

# 添加带属性的顶点
hg.add_v(1, {"name": "Alice", "age": 30})
hg.add_v(2, {"name": "Bob", "age": 25})
hg.add_v(3, {"name": "Charlie", "age": 35})

# 添加连接多个顶点的超边
hg.add_e((1, 2), {"relation": "friends"})
hg.add_e((1, 2, 3), {"relation": "project_team"})

# 查询超图
print(f"顶点: {hg.all_v}")
print(f"边: {hg.all_e}")

# 可视化超图
hg.draw()  # 在网页浏览器中打开可视化
```

## 📚 文档

- **[快速开始](getting-started/installation.zh.md)**: 安装和基本设置
- **[API 参考](api/index.zh.md)**: 完整的 API 文档  
- **[可视化指南](visualization/index.zh.md)**: 交互式超图可视化
- **[示例](examples/basic-usage.zh.md)**: 实用示例和教程

## 🤝 贡献

欢迎贡献！请查看我们的 [GitHub 仓库](https://github.com/iMoonLab/Hypergraph-DB) 了解更多信息。

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](about/license.zh.md) 文件。

## 📬 联系方式

- **作者**: 丰一帆
- **邮箱**: evanfeng97@qq.com
- **GitHub**: [@iMoonLab](https://github.com/iMoonLab)

---

*由 iMoonLab 团队用 ❤️ 构建*
