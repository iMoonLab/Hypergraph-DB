# API 参考概述

Hypergraph-DB 提供了简洁而强大的 API 来创建、操作和查询超图。本节提供所有可用类和方法的完整参考。

## 核心类

### HypergraphDB

主要的超图数据库类，提供完整的超图操作功能。

```python
from hyperdb import HypergraphDB

# 创建新的超图
hg = HypergraphDB()

# 从文件加载现有超图
hg = HypergraphDB("my_hypergraph.hgdb")
```

[查看完整 HypergraphDB API →](hypergraph.zh.md)

### BaseHypergraphDB

抽象基类，定义了超图数据库的核心接口。

```python
from hyperdb import BaseHypergraphDB

# 主要用于继承和扩展
class CustomHypergraphDB(BaseHypergraphDB):
    # 自定义实现
    pass
```

[查看完整 BaseHypergraphDB API →](base.zh.md)

## 快速 API 参考

### 基础操作

| 方法 | 描述 | 示例 |
|------|------|------|
| `add_v(id, data)` | 添加顶点 | `hg.add_v("A", {"name": "Alice"})` |
| `add_e(tuple, data)` | 添加超边 | `hg.add_e(("A", "B"), {"type": "friend"})` |
| `remove_v(id)` | 移除顶点 | `hg.remove_v("A")` |
| `remove_e(tuple)` | 移除超边 | `hg.remove_e(("A", "B"))` |
| `v(id)` | 获取顶点数据 | `data = hg.v("A")` |
| `e(tuple)` | 获取超边数据 | `data = hg.e(("A", "B"))` |

### 查询操作

| 方法 | 描述 | 示例 |
|------|------|------|
| `has_v(id)` | 检查顶点是否存在 | `hg.has_v("A")` |
| `has_e(tuple)` | 检查超边是否存在 | `hg.has_e(("A", "B"))` |
| `degree_v(id)` | 顶点度数 | `deg = hg.degree_v("A")` |
| `degree_e(tuple)` | 超边大小 | `size = hg.degree_e(("A", "B"))` |
| `nbr_v(id)` | 顶点的邻居顶点 | `neighbors = hg.nbr_v("A")` |
| `nbr_e_of_v(id)` | 顶点的邻居超边 | `edges = hg.nbr_e_of_v("A")` |
| `nbr_v_of_e(tuple)` | 超边的邻居顶点 | `vertices = hg.nbr_v_of_e(("A", "B"))` |

### 全局属性

| 属性 | 描述 | 示例 |
|------|------|------|
| `all_v` | 所有顶点 | `vertices = hg.all_v` |
| `all_e` | 所有超边 | `edges = hg.all_e` |
| `num_v` | 顶点数量 | `count = hg.num_v` |
| `num_e` | 超边数量 | `count = hg.num_e` |

### 持久化操作

| 方法 | 描述 | 示例 |
|------|------|------|
| `save(path)` | 保存到文件 | `hg.save("graph.hgdb")` |
| `load(path)` | 从文件加载 | `hg.load("graph.hgdb")` |

### 可视化

| 方法 | 描述 | 示例 |
|------|------|------|
| `draw(port, open_browser)` | 启动可视化 | `hg.draw(port=8080)` |

[查看完整可视化 API →](visualization.zh.md)

## 常用模式

### 创建和填充超图

```python
from hyperdb import HypergraphDB

# 创建超图
hg = HypergraphDB()

# 批量添加顶点
users = [
    ("user1", {"name": "张三", "age": 25}),
    ("user2", {"name": "李四", "age": 30}),
    ("user3", {"name": "王五", "age": 28})
]

for user_id, user_data in users:
    hg.add_v(user_id, user_data)

# 批量添加超边
relationships = [
    (("user1", "user2"), {"type": "朋友"}),
    (("user1", "user2", "user3"), {"type": "项目团队"})
]

for vertices, edge_data in relationships:
    hg.add_e(vertices, edge_data)
```

### 查询和分析

```python
# 分析超图结构
print(f"超图包含 {hg.num_v} 个顶点和 {hg.num_e} 条超边")

# 找出度数最高的顶点
most_connected = max(hg.all_v, key=lambda v: hg.degree_v(v))
print(f"最活跃的用户: {hg.v(most_connected)['name']}")

# 分析超边大小分布
edge_sizes = [hg.degree_e(e) for e in hg.all_e]
avg_size = sum(edge_sizes) / len(edge_sizes)
print(f"平均超边大小: {avg_size:.2f}")
```

### 数据更新

```python
# 更新顶点数据
hg.update_v("user1", {"age": 26, "location": "北京"})

# 更新超边数据
hg.update_e(("user1", "user2"), {"strength": 0.9})

# 检查更新结果
updated_user = hg.v("user1")
updated_edge = hg.e(("user1", "user2"))
```

## 错误处理

### 常见异常

```python
try:
    # 尝试添加顶点
    hg.add_v("user1", {"name": "张三"})
    
    # 尝试添加超边（顶点必须已存在）
    hg.add_e(("user1", "user999"), {"type": "朋友"})
    
except AssertionError as e:
    print(f"断言错误: {e}")
    
except KeyError as e:
    print(f"键错误: {e}")
    
except Exception as e:
    print(f"其他错误: {e}")
```

### 最佳实践

1. **顶点 ID**: 使用可哈希的、有意义的标识符
2. **数据验证**: 在添加数据前进行验证
3. **异常处理**: 适当处理可能的错误
4. **性能考虑**: 对于大型数据集，考虑批量操作

## 类型提示

Hypergraph-DB 支持类型提示以提供更好的开发体验：

```python
from typing import Dict, Any, Tuple, List, Set
from hyperdb import HypergraphDB

def analyze_hypergraph(hg: HypergraphDB) -> Dict[str, Any]:
    """分析超图并返回统计信息"""
    return {
        "num_vertices": hg.num_v,
        "num_edges": hg.num_e,
        "avg_degree": sum(hg.degree_v(v) for v in hg.all_v) / hg.num_v
    }
```

## 扩展 API

### 自定义分析方法

```python
from hyperdb import HypergraphDB

class AnalyticsHypergraphDB(HypergraphDB):
    """扩展了分析功能的超图数据库"""
    
    def clustering_coefficient(self, vertex_id: str) -> float:
        """计算顶点的聚类系数"""
        neighbors = self.nbr_v(vertex_id)
        if len(neighbors) < 2:
            return 0.0
        
        # 计算邻居之间的连接
        connections = 0
        total_possible = len(neighbors) * (len(neighbors) - 1) // 2
        
        for edge in self.all_e:
            edge_vertices = self.nbr_v_of_e(edge)
            if len(edge_vertices.intersection(neighbors)) >= 2:
                connections += 1
        
        return connections / total_possible if total_possible > 0 else 0.0
    
    def k_core_decomposition(self, k: int) -> Set[str]:
        """k-核分解：找出度数至少为k的顶点"""
        return {v for v in self.all_v if self.degree_v(v) >= k}
```

## 下一步

- **[HypergraphDB 详细 API](hypergraph.zh.md)**: 主类的完整方法文档
- **[BaseHypergraphDB API](base.zh.md)**: 基类和扩展指南
- **[可视化 API](visualization.zh.md)**: 可视化功能详解
- **[示例代码](../examples/basic-usage.zh.md)**: 实际使用案例

通过这些 API，您可以充分利用 Hypergraph-DB 的强大功能来建模和分析复杂的多元关系！🚀
