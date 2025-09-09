# 超图基础

!!! info "关于超图"
    超图是图论的一个自然推广，其中的边（称为超边）可以连接任意数量的顶点，而不仅仅是两个顶点。这使得超图特别适合建模复杂的多元关系。

## 什么是超图？

### 传统图 vs 超图

**传统图**只能表示二元关系：
```
Alice ←→ Bob (一条边)
Bob ←→ Charlie (另一条边)
Alice ←→ Charlie (第三条边)
```

**超图**可以自然地表示多元关系：
```
{Alice, Bob, Charlie} → 项目团队 (一条超边)
```

### 形式化定义

一个超图 H = (V, E) 包含：
- **V**: 顶点集合
- **E**: 超边集合，其中每条超边 e ∈ E 是 V 的一个子集

## 超图的优势

### 1. 自然建模复杂关系

```python
from hyperdb import HypergraphDB

# 学术合作网络示例
hg = HypergraphDB()

# 研究人员
hg.add_v("alice", {"name": "Alice Chen", "field": "ML"})
hg.add_v("bob", {"name": "Bob Smith", "field": "NLP"})  
hg.add_v("charlie", {"name": "Charlie Wang", "field": "CV"})

# 一篇论文的多位共同作者 - 用一条超边表示
hg.add_e(("alice", "bob", "charlie"), {
    "paper": "多模态深度学习综述",
    "venue": "Nature AI",
    "year": 2024
})
```

### 2. 减少数据冗余

**传统图方法**（需要多条边）：
```python
# 需要 3 条边表示 3 人的合作
graph.add_edge("alice", "bob", {"paper": "论文A"})
graph.add_edge("bob", "charlie", {"paper": "论文A"})  
graph.add_edge("alice", "charlie", {"paper": "论文A"})
```

**超图方法**（只需要 1 条超边）：
```python
# 只需要 1 条超边
hypergraph.add_e(("alice", "bob", "charlie"), {"paper": "论文A"})
```

### 3. 保持语义完整性

超边保持了群体关系的原子性 - 三人团队是一个整体，不是三个二元关系的组合。

## 超图概念

### 顶点度数

顶点的度数是包含该顶点的超边数量：

```python
# Alice 参与了多少个项目/论文？
alice_degree = hg.degree_v("alice")
print(f"Alice 的度数: {alice_degree}")
```

### 超边大小

超边的大小是其包含的顶点数量：

```python
# 这个项目团队有多少人？
team_edge = ("alice", "bob", "charlie")
team_size = hg.degree_e(team_edge)
print(f"团队规模: {team_size}")
```

### 邻接关系

在超图中，两个顶点是邻接的，如果它们共同出现在至少一条超边中：

```python
# Alice 的所有合作伙伴
alice_neighbors = hg.nbr_v("alice")
print(f"Alice 的合作伙伴: {alice_neighbors}")
```

## 超图的类型

### 1. k-均匀超图

所有超边都恰好包含 k 个顶点：

```python
# 3-均匀超图：所有团队都是3人
hg = HypergraphDB()
hg.add_e(("a", "b", "c"), {"team": "Alpha"})
hg.add_e(("d", "e", "f"), {"team": "Beta"})
hg.add_e(("g", "h", "i"), {"team": "Gamma"})
```

### 2. 简单超图

没有重复的超边，且不包含空超边：

```python
# 每个超边都是唯一的
hg.add_e(("alice", "bob"), {"project": "A"})
hg.add_e(("alice", "bob"), {"project": "B"})  # 这会更新现有超边
```

### 3. 加权超图

超边和/或顶点带有权重：

```python
hg.add_v("alice", {"expertise": 0.9})
hg.add_e(("alice", "bob"), {"collaboration_strength": 0.8})
```

## 实际应用场景

### 1. 社交网络分析

```python
# 群体活动和多方互动
social_hg = HypergraphDB()

# 朋友聚会
social_hg.add_e(("alice", "bob", "charlie", "diana"), {
    "activity": "聚餐",
    "date": "2024-01-15",
    "location": "餐厅A"
})

# 工作团队
social_hg.add_e(("alice", "bob", "eve"), {
    "activity": "项目会议",
    "project": "移动应用开发"
})
```

### 2. 生物信息学

```python
# 蛋白质相互作用网络
bio_hg = HypergraphDB()

# 蛋白质复合体（多个蛋白质的相互作用）
bio_hg.add_e(("protein1", "protein2", "protein3"), {
    "complex": "转录因子复合体",
    "function": "基因转录调控",
    "location": "细胞核"
})
```

### 3. 推荐系统

```python
# 用户-物品-上下文的三元关系
rec_hg = HypergraphDB()

# 用户在特定上下文中对物品的交互
rec_hg.add_e(("user123", "movie456", "weekend", "home"), {
    "interaction": "观看",
    "rating": 4.5,
    "timestamp": "2024-01-20"
})
```

### 4. 知识图谱

```python
# 复杂的知识关系
kg_hg = HypergraphDB()

# 多元关系：谁在何时何地做了什么
kg_hg.add_e(("爱因斯坦", "相对论", "1905年", "瑞士"), {
    "relation": "发现",
    "impact": "革命性",
    "field": "物理学"
})
```

## 超图分析

### 中心性度量

```python
def hypergraph_centrality(hg, vertex):
    """计算超图中顶点的中心性"""
    # 基于度数的中心性
    degree_centrality = hg.degree_v(vertex)
    
    # 基于超边大小的加权中心性
    weighted_centrality = 0
    for edge in hg.nbr_e_of_v(vertex):
        edge_size = hg.degree_e(edge)
        weighted_centrality += 1.0 / edge_size  # 大团队中的影响力更分散
    
    return {
        "degree": degree_centrality,
        "weighted": weighted_centrality
    }
```

### 社区检测

```python
def find_communities(hg):
    """基于超边的简单社区检测"""
    communities = []
    
    for edge in hg.all_e:
        members = hg.nbr_v_of_e(edge)
        edge_info = hg.e(edge)
        
        communities.append({
            "members": list(members),
            "size": len(members),
            "metadata": edge_info
        })
    
    return communities
```

## 超图 vs 传统图的选择

### 选择超图的情况

- ✅ **群体关系**: 需要表示多方参与的关系
- ✅ **原子性**: 关系的完整性很重要
- ✅ **简化建模**: 减少边的数量和复杂性
- ✅ **语义保持**: 需要保持关系的原始语义

### 选择传统图的情况

- ✅ **二元关系**: 主要是成对的关系
- ✅ **成熟算法**: 需要使用大量现有的图算法
- ✅ **性能要求**: 对计算效率有严格要求
- ✅ **工具支持**: 需要使用现有的图数据库

## 超图理论基础

### 对偶超图

每个超图都有一个对偶超图，其中：
- 原超图的顶点变成对偶超图的超边
- 原超图的超边变成对偶超图的顶点

```python
def create_dual_hypergraph(original_hg):
    """创建对偶超图"""
    dual_hg = HypergraphDB()
    
    # 原超图的每条超边变成对偶超图的一个顶点
    for edge in original_hg.all_e:
        edge_str = str(edge)
        edge_data = original_hg.e(edge)
        dual_hg.add_v(edge_str, edge_data)
    
    # 原超图的每个顶点变成对偶超图的一条超边
    for vertex in original_hg.all_v:
        incident_edges = original_hg.nbr_e_of_v(vertex)
        edge_strs = [str(e) for e in incident_edges]
        vertex_data = original_hg.v(vertex)
        dual_hg.add_e(tuple(edge_strs), vertex_data)
    
    return dual_hg
```

### 超图的矩阵表示

超图可以用关联矩阵表示，其中行代表顶点，列代表超边：

```python
import numpy as np

def hypergraph_incidence_matrix(hg):
    """生成超图的关联矩阵"""
    vertices = list(hg.all_v)
    edges = list(hg.all_e)
    
    matrix = np.zeros((len(vertices), len(edges)))
    
    for j, edge in enumerate(edges):
        edge_vertices = hg.nbr_v_of_e(edge)
        for vertex in edge_vertices:
            i = vertices.index(vertex)
            matrix[i, j] = 1
    
    return matrix, vertices, edges
```

## 下一步

现在您已经了解了超图的基础概念，您可以：

- **[查看实际示例](../examples/basic-usage.zh.md)**: 学习如何在实际场景中应用超图
- **[探索 API](../api/index.zh.md)**: 了解所有可用的方法和功能
- **[可视化您的数据](../visualization/index.zh.md)**: 使用交互式工具探索超图结构

超图为复杂关系建模提供了强大而自然的工具！🎯
