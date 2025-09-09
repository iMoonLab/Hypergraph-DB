# HypergraphDB 类

`HypergraphDB` 是 Hypergraph-DB 的核心类，提供了创建、操作和查询超图的完整功能。

## 详细说明

`HypergraphDB` 是 Hypergraph-DB 的核心类，提供了创建、操作和查询超图的完整功能。

### 主要特性

- **顶点管理**: 添加、删除、更新和查询顶点
- **超边管理**: 添加、删除、更新和查询超边
- **邻接查询**: 查找顶点和超边的邻居关系
- **持久化**: 保存和加载超图数据
- **可视化**: 内置的 Web 可视化功能

### 使用示例

```python
from hyperdb import HypergraphDB

# 创建新的超图
hg = HypergraphDB()

# 添加顶点
hg.add_v("张三", {"年龄": 25, "职业": "工程师"})
hg.add_v("李四", {"年龄": 30, "职业": "设计师"})
hg.add_v("王五", {"年龄": 28, "职业": "产品经理"})

# 添加超边
hg.add_e(("张三", "李四"), {"关系": "朋友"})
hg.add_e(("张三", "李四", "王五"), {"关系": "项目团队"})

# 查询操作
print(f"顶点数量: {hg.num_v}")
print(f"超边数量: {hg.num_e}")
print(f"张三的度数: {hg.degree_v('张三')}")
print(f"张三的邻居: {hg.nbr_v('张三')}")

# 可视化
hg.draw()
```
