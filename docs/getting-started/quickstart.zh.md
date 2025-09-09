# 快速开始指南

本指南将在几分钟内帮助您开始使用 Hypergraph-DB！

## 安装

首先，安装 Hypergraph-DB：

```bash
pip install hypergraph-db
```

## 您的第一个超图

让我们创建一个简单的超图来表示包含群体活动的社交网络：

```python
from hyperdb import HypergraphDB

# 创建新的超图数据库
hg = HypergraphDB()

# 添加一些人作为顶点
hg.add_v(1, {"name": "Alice", "age": 30, "city": "北京"})
hg.add_v(2, {"name": "Bob", "age": 24, "city": "上海"})
hg.add_v(3, {"name": "Charlie", "age": 28, "city": "深圳"})
hg.add_v(4, {"name": "David", "age": 35, "city": "广州"})

print(f"已添加 {hg.num_v} 个顶点")
```

## 添加关系

现在让我们添加一些关系（超边）：

```python
# 二元关系
hg.add_e((1, 2), {"relation": "朋友", "since": "2020"})
hg.add_e((2, 3), {"relation": "同事", "company": "科技公司"})

# 群体关系（超图的威力所在！）
hg.add_e((1, 2, 3), {"relation": "学习小组", "subject": "机器学习"})
hg.add_e((1, 3, 4), {"relation": "项目团队", "project": "网页应用"})

print(f"已添加 {hg.num_e} 条超边")
```

## 基本查询

使用简单查询探索您的超图：

```python
# 获取所有顶点和超边
print("所有顶点:", list(hg.all_v))
print("所有超边:", list(hg.all_e))

# 查询特定顶点的信息
alice_info = hg.v(1)
print(f"Alice 的信息: {alice_info}")

# 查询特定超边的信息
friendship = hg.e((1, 2))
print(f"友谊关系: {friendship}")

# 获取顶点的度数（连接的超边数量）
alice_degree = hg.degree_v(1)
print(f"Alice 的度数: {alice_degree}")

# 获取顶点的邻居
alice_neighbors = hg.nbr_v(1)
print(f"Alice 的邻居: {alice_neighbors}")
```

## 高级查询

```python
# 查找 Alice 参与的所有超边
alice_edges = hg.nbr_e_of_v(1)
print(f"Alice 参与的超边: {alice_edges}")

# 查找特定超边中的所有顶点
study_group_members = hg.nbr_v_of_e((1, 2, 3))
print(f"学习小组成员: {study_group_members}")

# 检查顶点或超边是否存在
has_alice = hg.has_v(1)
has_friendship = hg.has_e((1, 2))
print(f"Alice 存在: {has_alice}, 友谊关系存在: {has_friendship}")
```

## 数据操作

```python
# 更新顶点数据
hg.update_v(1, {"age": 31, "job": "工程师"})
print(f"更新后的 Alice 信息: {hg.v(1)}")

# 更新超边数据
hg.update_e((1, 2), {"relation": "好朋友", "strength": 0.9})
print(f"更新后的友谊关系: {hg.e((1, 2))}")

# 移除顶点（会自动移除相关的超边）
hg.remove_v(4)
print(f"移除 David 后的顶点数: {hg.num_v}")
print(f"移除 David 后的超边数: {hg.num_e}")
```

## 可视化

Hypergraph-DB 提供内置的 Web 可视化功能：

```python
# 启动交互式可视化
hg.draw()
```

这将：
1. 启动本地 Web 服务器
2. 自动打开浏览器
3. 显示您的超图的交互式可视化

## 持久化

保存和加载您的超图：

```python
# 保存到文件
hg.save("my_social_network.hgdb")

# 加载现有的超图
new_hg = HypergraphDB("my_social_network.hgdb")
print(f"加载的超图包含 {new_hg.num_v} 个顶点和 {new_hg.num_e} 条超边")
```

## 完整示例

这里有一个完整的示例，展示了创建、查询和可视化超图的完整工作流程：

```python
from hyperdb import HypergraphDB

# 创建学术合作网络
academic_network = HypergraphDB()

# 添加研究人员
researchers = [
    (1, {"name": "张教授", "field": "机器学习", "university": "清华大学"}),
    (2, {"name": "李博士", "field": "自然语言处理", "university": "北京大学"}),
    (3, {"name": "王研究员", "field": "计算机视觉", "university": "中科院"}),
    (4, {"name": "陈副教授", "field": "数据挖掘", "university": "复旦大学"}),
    (5, {"name": "刘讲师", "field": "深度学习", "university": "上海交大"})
]

for researcher_id, info in researchers:
    academic_network.add_v(researcher_id, info)

# 添加合作关系（论文合著）
collaborations = [
    ((1, 2), {"paper": "深度学习在NLP中的应用", "year": 2023, "venue": "AAAI"}),
    ((1, 3), {"paper": "多模态学习框架", "year": 2023, "venue": "CVPR"}),
    ((2, 4, 5), {"paper": "大规模文本挖掘技术", "year": 2024, "venue": "KDD"}),
    ((1, 2, 3, 4), {"paper": "人工智能综述", "year": 2024, "venue": "Nature"})
]

for authors, paper_info in collaborations:
    academic_network.add_e(authors, paper_info)

# 分析网络
print(f"学术网络包含 {academic_network.num_v} 位研究人员和 {academic_network.num_e} 篇合作论文")

# 找出最活跃的研究人员
most_active = max(academic_network.all_v, 
                  key=lambda v: academic_network.degree_v(v))
most_active_info = academic_network.v(most_active)
print(f"最活跃的研究人员: {most_active_info['name']} "
      f"({academic_network.degree_v(most_active)} 篇论文)")

# 分析合作模式
print("\n合作分析:")
for edge in academic_network.all_e:
    paper_info = academic_network.e(edge)
    authors = academic_network.nbr_v_of_e(edge)
    author_names = [academic_network.v(author)['name'] for author in authors]
    print(f"  {paper_info['paper']}: {', '.join(author_names)}")

# 启动可视化
academic_network.draw(port=8080)
print("学术合作网络可视化已启动，请访问 http://localhost:8080")
```

## 下一步

现在您已经了解了基础知识，您可以：

- **[查看更多示例](../examples/basic-usage.zh.md)**: 实用的使用案例
- **[学习超图理论](hypergraph-basics.zh.md)**: 理解超图的概念和应用
- **[探索 API](../api/index.zh.md)**: 完整的方法参考
- **[可视化指南](../visualization/index.zh.md)**: 高级可视化功能

## 小贴士

1. **命名约定**: 使用有意义的顶点 ID 和描述性的属性名
2. **数据组织**: 将相关属性组织在字典中以便查询
3. **性能**: 对于大型超图，考虑批量操作而不是逐个添加
4. **可视化**: 使用过滤功能来聚焦于超图的特定部分
5. **持久化**: 定期保存重要的超图数据

祝您使用 Hypergraph-DB 愉快！🎉
