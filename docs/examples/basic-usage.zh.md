# 基础用法示例

本页面提供了在常见场景中使用 Hypergraph-DB 的实用示例。

## 示例 1: 学术合作网络

建模学者之间的研究合作关系：

```python
from hyperdb import HypergraphDB

# 创建超图
hg = HypergraphDB()

# 添加研究人员作为顶点
researchers = {
    "alice": {"name": "张爱丽博士", "field": "机器学习", "university": "清华大学"},
    "bob": {"name": "王博文教授", "field": "自然语言处理", "university": "北京大学"},
    "charlie": {"name": "李查理研究员", "field": "计算机视觉", "university": "中科院"},
    "diana": {"name": "陈黛安副教授", "field": "机器人学", "university": "复旦大学"},
    "eve": {"name": "刘伊芙讲师", "field": "理论计算机", "university": "上海交大"}
}

for researcher_id, info in researchers.items():
    hg.add_v(researcher_id, info)

# 添加论文作为超边（连接所有共同作者）
papers = [
    (("alice", "bob"), {
        "title": "深度学习在自然语言理解中的应用",
        "year": 2023,
        "venue": "AAAI",
        "citations": 45
    }),
    (("alice", "charlie"), {
        "title": "视觉-语言模型在场景理解中的应用",
        "year": 2023,
        "venue": "CVPR",
        "citations": 38
    }),
    (("bob", "charlie", "diana"), {
        "title": "自主系统的多模态人工智能",
        "year": 2024,
        "venue": "NeurIPS",
        "citations": 12
    }),
    (("alice", "bob", "charlie", "eve"), {
        "title": "现代人工智能的理论基础",
        "year": 2024,
        "venue": "JMLR",
        "citations": 28
    })
]

for authors, paper_info in papers:
    hg.add_e(authors, paper_info)

# 分析网络
print(f"学术网络包含 {hg.num_v} 位研究人员和 {hg.num_e} 篇合作论文")

# 找出最活跃的研究人员
most_collaborative = max(hg.all_v, key=lambda v: hg.degree_v(v))
print(f"最活跃的研究人员: {hg.v(most_collaborative)['name']} "
      f"({hg.degree_v(most_collaborative)} 篇论文)")

# 找出最大的合作项目
largest_paper = max(hg.all_e, key=lambda e: hg.degree_e(e))
num_authors = hg.degree_e(largest_paper)
print(f"最大合作项目: {num_authors} 位作者")

# 可视化网络
hg.draw()
```

## 示例 2: 电子商务推荐系统

建模购物模式和产品关系：

```python
from hyperdb import HypergraphDB
from collections import defaultdict

# 创建电商超图
hg = HypergraphDB()

# 添加产品作为顶点
products = {
    "laptop_1": {"name": "游戏笔记本", "category": "电脑", "price": 8999},
    "mouse_1": {"name": "游戏鼠标", "category": "配件", "price": 299},
    "keyboard_1": {"name": "机械键盘", "category": "配件", "price": 599},
    "monitor_1": {"name": "4K显示器", "category": "配件", "price": 2199},
    "headset_1": {"name": "游戏耳机", "category": "配件", "price": 799},
    "phone_1": {"name": "智能手机", "category": "手机", "price": 4999}
}

for product_id, info in products.items():
    hg.add_v(product_id, info)

# 添加购物会话作为超边（在同一订单中购买的产品）
shopping_sessions = [
    (("laptop_1", "mouse_1", "keyboard_1"), {"user": "用户A", "date": "2024-01-15", "total": 9897}),
    (("laptop_1", "monitor_1"), {"user": "用户B", "date": "2024-01-16", "total": 11198}),
    (("mouse_1", "keyboard_1", "headset_1"), {"user": "用户C", "date": "2024-01-17", "total": 1697}),
    (("phone_1", "headset_1"), {"user": "用户D", "date": "2024-01-18", "total": 5798}),
    (("laptop_1", "mouse_1", "keyboard_1", "monitor_1"), {"user": "用户E", "date": "2024-01-19", "total": 12496})
]

for products_in_session, session_info in shopping_sessions:
    hg.add_e(products_in_session, session_info)

# 商品推荐功能
def find_frequently_bought_together(product_id, min_frequency=1):
    """找出经常与给定产品一起购买的商品"""
    sessions_with_product = hg.nbr_e_of_v(product_id)
    
    # 统计共现次数
    co_occurrence = defaultdict(int)
    for session in sessions_with_product:
        other_products = hg.nbr_v_of_e(session) - {product_id}
        for other_product in other_products:
            co_occurrence[other_product] += 1
    
    # 过滤最小频率
    recommendations = {product: count for product, count in co_occurrence.items() 
                      if count >= min_frequency}
    
    # 按频率排序
    return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

# 生成推荐
laptop_recommendations = find_frequently_bought_together("laptop_1")
print("与游戏笔记本经常一起购买的产品:")
for product, frequency in laptop_recommendations:
    product_name = hg.v(product)["name"]
    print(f"  {product_name}: {frequency} 次")

# 找出最受欢迎的产品类别
category_popularity = defaultdict(int)
for edge in hg.all_e:
    products_in_session = hg.nbr_v_of_e(edge)
    for product in products_in_session:
        category = hg.v(product)["category"]
        category_popularity[category] += 1

print("\n产品类别受欢迎程度:")
for category, count in sorted(category_popularity.items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count} 次购买")

# 可视化购物网络
hg.draw()
```

## 示例 3: 社交网络分析

建模群体互动和多方关系：

```python
# 创建社交网络超图
social_hg = HypergraphDB()

# 添加人员
people = {
    "alice": {"name": "爱丽丝", "age": 28, "city": "北京", "interests": ["读书", "旅行", "摄影"]},
    "bob": {"name": "鲍勃", "age": 32, "city": "上海", "interests": ["运动", "音乐", "编程"]},
    "charlie": {"name": "查理", "age": 25, "city": "深圳", "interests": ["游戏", "动漫", "美食"]},
    "diana": {"name": "黛安", "age": 30, "city": "杭州", "interests": ["艺术", "设计", "旅行"]},
    "eve": {"name": "伊芙", "age": 27, "city": "成都", "interests": ["美食", "音乐", "健身"]}
}

for person_id, info in people.items():
    social_hg.add_v(person_id, info)

# 添加群体活动作为超边
group_activities = [
    (("alice", "bob"), {"activity": "咖啡聊天", "date": "2024-01-10", "location": "星巴克"}),
    (("alice", "diana"), {"activity": "美术馆参观", "date": "2024-01-12", "location": "国家美术馆"}),
    (("bob", "charlie", "eve"), {"activity": "健身房", "date": "2024-01-15", "location": "24小时健身"}),
    (("alice", "charlie", "diana"), {"activity": "摄影外拍", "date": "2024-01-18", "location": "颐和园"}),
    (("bob", "diana", "eve", "charlie"), {"activity": "聚餐", "date": "2024-01-20", "location": "川菜馆"})
]

for participants, activity_info in group_activities:
    social_hg.add_e(participants, activity_info)

# 社交网络分析
print(f"社交网络包含 {social_hg.num_v} 个人和 {social_hg.num_e} 个群体活动")

# 找出最社交的人（最高度数）
most_social = max(social_hg.all_v, key=lambda v: social_hg.degree_v(v))
print(f"最社交的人: {social_hg.v(most_social)['name']} "
      f"(参与 {social_hg.degree_v(most_social)} 个活动)")

# 分析群体规模
group_sizes = [social_hg.degree_e(e) for e in social_hg.all_e]
avg_group_size = sum(group_sizes) / len(group_sizes)
print(f"平均群体规模: {avg_group_size:.1f}")
print(f"最大群体: {max(group_sizes)} 人")

# 找出兴趣相似的社区
print("\n基于共同活动的社区:")
for edge in social_hg.all_e:
    if social_hg.degree_e(edge) >= 3:  # 至少3人的群体
        participants = social_hg.nbr_v_of_e(edge)
        activity = social_hg.e(edge)
        
        # 找出共同兴趣
        if len(participants) > 1:
            common_interests = set(social_hg.v(list(participants)[0])["interests"])
            for person in participants:
                common_interests &= set(social_hg.v(person)["interests"])
            
            if common_interests:
                print(f"  {activity['activity']}: {len(participants)} 人，共同兴趣: {', '.join(common_interests)}")

# 找出社交桥梁（连接不同群体的人）
print("\n社交桥梁:")
for person in social_hg.all_v:
    person_groups = social_hg.nbr_e_of_v(person)
    if len(person_groups) >= 2:
        # 检查是否连接了不同的群体
        unique_groups = set()
        for group1 in person_groups:
            for group2 in person_groups:
                if group1 != group2:
                    # 检查两个群体是否有其他共同成员
                    group1_members = social_hg.nbr_v_of_e(group1) - {person}
                    group2_members = social_hg.nbr_v_of_e(group2) - {person}
                    if not group1_members.intersection(group2_members):
                        unique_groups.add((group1, group2))
        
        if unique_groups:
            name = social_hg.v(person)["name"]
            num_groups = social_hg.degree_v(person)
            print(f"  {name} (连接 {num_groups} 个群体)")

# 可视化社交网络
social_hg.draw()
```

## 示例 4: 知识图谱

建模复杂的知识关系：

```python
# 创建知识图谱超图
kg = HypergraphDB()

# 添加实体
entities = {
    "einstein": {"name": "阿尔伯特·爱因斯坦", "type": "人物", "birth_year": 1879},
    "relativity": {"name": "相对论", "type": "理论", "year": 1905},
    "nobel_prize": {"name": "诺贝尔物理学奖", "type": "奖项", "year": 1921},
    "princeton": {"name": "普林斯顿大学", "type": "机构", "founded": 1746},
    "photoelectric": {"name": "光电效应", "type": "现象", "discovery": 1905},
    "quantum": {"name": "量子力学", "type": "理论", "era": "20世纪初"}
}

for entity_id, info in entities.items():
    kg.add_v(entity_id, info)

# 添加复杂关系作为超边
knowledge_relations = [
    (("einstein", "relativity"), {"relation": "提出", "year": 1905, "impact": "革命性"}),
    (("einstein", "nobel_prize", "photoelectric"), {"relation": "因...获得", "year": 1921}),
    (("einstein", "princeton"), {"relation": "任职于", "period": "1933-1955"}),
    (("relativity", "quantum", "einstein"), {"relation": "理论贡献", "field": "现代物理学"}),
    (("photoelectric", "quantum"), {"relation": "理论基础", "contribution": "量子概念"})
]

for vertices, relation_info in knowledge_relations.items():
    kg.add_e(vertices, relation_info)

# 知识图谱分析
print(f"知识图谱包含 {kg.num_v} 个实体和 {kg.num_e} 个关系")

# 找出最重要的实体（最高度数）
most_important = max(kg.all_v, key=lambda v: kg.degree_v(v))
entity_info = kg.v(most_important)
print(f"最重要的实体: {entity_info['name']} ({entity_info['type']})")

# 分析获奖信息
print("\n获奖信息:")
for edge in kg.all_e:
    edge_info = kg.e(edge)
    if "nobel_prize" in kg.nbr_v_of_e(edge):
        winner = [e for e in kg.nbr_v_of_e(edge) if e != "nobel_prize"][0]
        winner_info = kg.v(winner)
        print(f"  {winner_info['name']} 于 {edge_info['year']} 年获得诺贝尔奖")

# 理论发展关系
print("\n理论发展:")
for edge in kg.all_e:
    if kg.degree_e(edge) >= 3:  # 多元关系
        entities_in_relation = kg.nbr_v_of_e(edge)
        theory_entities = [e for e in entities_in_relation if kg.v(e)['type'] == 'theory']
        
        if len(theory_entities) >= 2:
            theory_name = kg.v(theory_entities[0])['name']
            developer_names = [kg.v(dev)['name'] for dev in entities_in_relation if kg.v(dev)['type'] == 'person']
            print(f"  {theory_name}: {', '.join(developer_names)}")

# 可视化知识图谱
kg.draw()
```

## 有效使用技巧

### 1. 选择有意义的 ID
```python
# 好的: 描述性 ID
hg.add_v("user_alice_chen", {"name": "陈爱丽丝"})

# 不好的: 无意义的数字
hg.add_v(12345, {"name": "陈爱丽丝"})
```

### 2. 结构化数据属性
```python
# 好的: 结构化属性
hg.add_v("researcher_001", {
    "personal": {"name": "张三", "age": 35},
    "academic": {"field": "AI", "university": "清华"},
    "contact": {"email": "zhang@example.com"}
})
```

### 3. 有意义的超边数据
```python
# 好的: 丰富的超边信息
hg.add_e(("alice", "bob", "charlie"), {
    "event": "项目会议",
    "project": "移动应用开发",
    "date": "2024-01-15",
    "duration": "2小时",
    "outcome": "确定技术方案"
})
```

### 4. 一致的数据格式
```python
# 确保同类数据格式一致
date_format = "%Y-%m-%d"
for event_data in events:
    hg.add_e(event_data["participants"], {
        "date": event_data["date"].strftime(date_format),
        "type": event_data["type"]
    })
```

### 5. 批量操作提升性能
```python
# 好的: 批量操作
vertices_to_add = [
    ("v1", {"name": "顶点1"}),
    ("v2", {"name": "顶点2"}),
    # ... 更多顶点
]

for vertex_id, vertex_data in vertices_to_add:
    hg.add_v(vertex_id, vertex_data)
```

## 下一步

现在您已经看到了基本用法，您可以：

- **[探索高级功能](advanced.zh.md)**: 复杂分析和算法
- **[学习 API 详细信息](../api/index.zh.md)**: 深入了解所有方法
- **[可视化指南](../visualization/index.zh.md)**: 创建令人印象深刻的可视化

祝您使用 Hypergraph-DB 愉快！🚀
