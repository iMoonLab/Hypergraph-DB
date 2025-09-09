# 超图可视化示例

本指南提供了使用 Hypergraph-DB 内置可视化功能的全面示例。

## ⚡ 重要提示：代码执行顺序

在使用可视化功能时，请注意以下代码执行顺序，确保能看到完整的分析结果：

```python
# ✅ 推荐的代码组织方式
# 1. 创建数据
hg = HypergraphDB()
hg.add_v(...)
hg.add_e(...)

# 2. 先进行分析（在可视化之前）
print("分析结果：")
print(f"网络规模：{hg.num_v} 顶点，{hg.num_e} 边")
# 其他分析...

# 3. 最后启动可视化（用户按Ctrl+C后程序结束）
print("启动可视化...")
hg.draw()  # 阻塞直到用户按Ctrl+C
```

```python
# ❌ 避免的代码组织方式
hg.draw()  # 用户按Ctrl+C后程序直接退出
print("这些分析结果永远不会显示")  # 永远不会执行
```

---

## 🎯 示例 1：社交网络分析

让我们创建并可视化一个社交网络，其中朋友群体一起参与各种活动。

```python
from hyperdb import HypergraphDB

# 创建社交网络超图
social_network = HypergraphDB()

# 添加人员作为顶点
people = {
    "alice": {"name": "Alice", "age": 25, "city": "纽约", "interests": ["阅读", "音乐"]},
    "bob": {"name": "Bob", "age": 27, "city": "旧金山", "interests": ["运动", "旅行"]},
    "charlie": {"name": "Charlie", "age": 23, "city": "波士顿", "interests": ["编程", "游戏"]},
    "diana": {"name": "Diana", "age": 26, "city": "西雅图", "interests": ["艺术", "摄影"]},
    "eve": {"name": "Eve", "age": 24, "city": "奥斯汀", "interests": ["音乐", "烹饪"]},
    "frank": {"name": "Frank", "age": 28, "city": "丹佛", "interests": ["徒步", "旅行"]}
}

for person_id, info in people.items():
    social_network.add_v(person_id, info)

# 添加社交活动作为超边（连接朋友群体）
activities = [
    # 小型聚会
    (("alice", "bob"), {
        "activity": "咖啡聚会",
        "date": "2024-01-15",
        "location": "中央公园",
        "duration": 2
    }),
    
    # 中型群体活动
    (("alice", "charlie", "eve"), {
        "activity": "音乐会",
        "date": "2024-01-20",
        "location": "麦迪逊广场花园",
        "duration": 4
    }),
    
    # 大型群体活动
    (("bob", "diana", "frank", "eve"), {
        "activity": "徒步旅行",
        "date": "2024-02-01",
        "location": "约塞米蒂国家公园",
        "duration": 48
    }),
    
    # 全员聚会
    (("alice", "bob", "charlie", "diana", "eve", "frank"), {
        "activity": "生日派对",
        "date": "2024-02-14",
        "location": "Alice的公寓",
        "duration": 6
    })
]

for participants, activity_info in activities:
    social_network.add_e(participants, activity_info)

# 先进行分析，再可视化
print("📊 网络分析结果：")
print("=" * 40)

# 分析网络
print(f"👥 网络规模：{social_network.num_v} 人，{social_network.num_e} 项活动")

# 找到最活跃的人
most_social = max(social_network.all_v, key=lambda v: social_network.degree_v(v))
print(f"🌟 最活跃的人：{social_network.v(most_social)['name']} "
      f"({social_network.degree_v(most_social)} 项活动)")

# 显示所有参与者的活动数量
print("\n👥 所有参与者活动统计：")
for person_id in social_network.all_v:
    person_info = social_network.v(person_id)
    activity_count = social_network.degree_v(person_id)
    print(f"  • {person_info['name']}: {activity_count} 项活动")

print("\n" + "=" * 40)
print("🎨 启动可视化（按 Ctrl+C 关闭可视化窗口）")
social_network.draw()
```

## 🧬 示例 2：科学合作网络

可视化计算生物学中的研究合作：

```python
from hyperdb import HypergraphDB

# 创建研究合作超图
research_network = HypergraphDB()

# 添加研究者作为顶点
researchers = {
    "dr_smith": {
        "name": "Dr. Sarah Smith",
        "field": "生物信息学",
        "institution": "MIT",
        "h_index": 45,
        "experience": 15
    },
    "dr_jones": {
        "name": "Dr. Michael Jones", 
        "field": "机器学习",
        "institution": "斯坦福",
        "h_index": 38,
        "experience": 12
    },
    "dr_garcia": {
        "name": "Dr. Maria Garcia",
        "field": "基因组学",
        "institution": "哈佛",
        "h_index": 52,
        "experience": 18
    },
    "dr_chen": {
        "name": "Dr. Wei Chen",
        "field": "系统生物学",
        "institution": "UCSF",
        "h_index": 41,
        "experience": 14
    },
    "dr_taylor": {
        "name": "Dr. James Taylor",
        "field": "计算化学",
        "institution": "加州理工",
        "h_index": 36,
        "experience": 10
    }
}

for researcher_id, info in researchers.items():
    research_network.add_v(researcher_id, info)

# 添加研究论文作为超边
publications = [
    # 双人合作
    (("dr_smith", "dr_jones"), {
        "title": "蛋白质结构预测的深度学习",
        "journal": "Nature Biotechnology",
        "year": 2023,
        "citations": 127,
        "impact_factor": 46.9
    }),
    
    # 三人合作
    (("dr_garcia", "dr_chen", "dr_taylor"), {
        "title": "疾病预测的多组学整合",
        "journal": "Cell",
        "year": 2023,
        "citations": 98,
        "impact_factor": 66.9
    }),
    
    # 大型合作
    (("dr_smith", "dr_jones", "dr_garcia", "dr_chen"), {
        "title": "AI驱动的药物发现管道",
        "journal": "Science",
        "year": 2024,
        "citations": 45,
        "impact_factor": 56.9
    }),
    
    # 跨机构大合作
    (("dr_smith", "dr_jones", "dr_garcia", "dr_chen", "dr_taylor"), {
        "title": "个性化医学的未来",
        "journal": "Nature Reviews Drug Discovery",
        "year": 2024,
        "citations": 23,
        "impact_factor": 112.3
    })
]

for authors, paper_info in publications:
    research_network.add_e(authors, paper_info)

# 先进行研究影响力分析
print("� 研究合作网络分析结果：")
print("=" * 50)

# 基础网络统计
print(f"� 网络规模：{research_network.num_v} 位研究者，{research_network.num_e} 篇论文")

# 找到最合作的研究者
most_collaborative = max(research_network.all_v, 
                        key=lambda v: research_network.degree_v(v))
researcher_info = research_network.v(most_collaborative)
print(f"🤝 最合作的研究者：{researcher_info['name']} "
      f"({research_network.degree_v(most_collaborative)} 篇论文)")

# 找到最高影响力的论文
highest_impact = max(research_network.all_e, 
                    key=lambda e: research_network.e(e)['impact_factor'])
impact_factor = research_network.e(highest_impact)['impact_factor']
print(f"⭐ 最高影响力论文：影响因子 {impact_factor}")

# 显示每位研究者的详细信息
print("\n👨‍🔬 研究者合作统计：")
for researcher_id in research_network.all_v:
    info = research_network.v(researcher_id)
    collab_count = research_network.degree_v(researcher_id)
    print(f"  • {info['name']} ({info['institution']})")
    print(f"    领域: {info['field']}, H指数: {info['h_index']}, 合作论文: {collab_count}")

print("\n" + "=" * 50)
print("🔬 启动研究网络可视化（按 Ctrl+C 关闭）")
research_network.draw()
```

## 🛒 示例 3：电商购买模式

分析客户购买行为和产品关系：

```python
from hyperdb import HypergraphDB

# 创建电商超图
ecommerce = HypergraphDB()

# 添加产品作为顶点
products = {
    "laptop": {"name": "游戏笔记本", "category": "电子产品", "price": 1299.99, "rating": 4.5},
    "mouse": {"name": "无线鼠标", "category": "电子产品", "price": 49.99, "rating": 4.3},
    "keyboard": {"name": "机械键盘", "category": "电子产品", "price": 129.99, "rating": 4.6},
    "monitor": {"name": "4K显示器", "category": "电子产品", "price": 399.99, "rating": 4.4},
    "headset": {"name": "游戏耳机", "category": "电子产品", "price": 89.99, "rating": 4.2},
    "desk": {"name": "升降桌", "category": "家具", "price": 299.99, "rating": 4.1},
    "chair": {"name": "人体工学椅", "category": "家具", "price": 249.99, "rating": 4.7},
    "lamp": {"name": "LED台灯", "category": "家具", "price": 79.99, "rating": 4.0}
}

for product_id, info in products.items():
    ecommerce.add_v(product_id, info)

# 添加购物篮作为超边
purchase_baskets = [
    # 游戏装备购买
    (("laptop", "mouse", "keyboard", "headset"), {
        "customer_id": "cust_001",
        "purchase_date": "2024-01-15",
        "total_amount": 1569.96,
        "customer_type": "游戏爱好者"
    }),
    
    # 办公设备购买
    (("monitor", "desk", "chair", "lamp"), {
        "customer_id": "cust_002", 
        "purchase_date": "2024-01-18",
        "total_amount": 929.96,
        "customer_type": "远程工作者"
    }),
    
    # 简单游戏设备
    (("mouse", "keyboard", "headset"), {
        "customer_id": "cust_003",
        "purchase_date": "2024-01-20",
        "total_amount": 269.97,
        "customer_type": "预算游戏玩家"
    }),
    
    # 豪华工作区
    (("laptop", "monitor", "desk", "chair", "lamp"), {
        "customer_id": "cust_004",
        "purchase_date": "2024-01-25",
        "total_amount": 2229.95,
        "customer_type": "专业人士"
    }),
    
    # 仅配件
    (("mouse", "lamp"), {
        "customer_id": "cust_005",
        "purchase_date": "2024-01-28",
        "total_amount": 129.98,
        "customer_type": "休闲买家"
    })
]

for products_in_basket, purchase_info in purchase_baskets:
    ecommerce.add_e(products_in_basket, purchase_info)

# 先进行购物篮分析
print("� 电商购买模式分析结果：")
print("=" * 45)

# 基础统计
print(f"🛍️ 商城概况：{ecommerce.num_v} 种产品，{ecommerce.num_e} 次购买")

# 找到最受欢迎的产品
most_popular = max(ecommerce.all_v, key=lambda v: ecommerce.degree_v(v))
product_info = ecommerce.v(most_popular)
print(f"🏆 最受欢迎产品：{product_info['name']} "
      f"({ecommerce.degree_v(most_popular)} 次购买)")

# 找到最大购买
largest_purchase = max(ecommerce.all_e, key=lambda e: len(ecommerce.e_v(e)))
num_items = len(ecommerce.e_v(largest_purchase))
purchase_info = ecommerce.e(largest_purchase)
print(f"💰 最大购买：{num_items} 件商品，${purchase_info['total_amount']:.2f}")

# 显示产品购买频次
print(f"\n📈 产品购买频次排行：")
products_by_popularity = sorted(ecommerce.all_v, 
                               key=lambda v: ecommerce.degree_v(v), 
                               reverse=True)
for i, product_id in enumerate(products_by_popularity, 1):
    info = ecommerce.v(product_id)
    purchases = ecommerce.degree_v(product_id)
    print(f"  {i}. {info['name']} - {purchases} 次购买 (${info['price']})")

# 分析客户类型
print(f"\n👥 客户类型分析：")
customer_types = {}
for edge_id in ecommerce.all_e:
    edge_data = ecommerce.e(edge_id)
    customer_type = edge_data.get('customer_type', '未知')
    if customer_type not in customer_types:
        customer_types[customer_type] = 0
    customer_types[customer_type] += 1

for customer_type, count in customer_types.items():
    print(f"  • {customer_type}: {count} 次购买")

print("\n" + "=" * 45)
print("🛒 启动购买模式可视化（按 Ctrl+C 关闭）")
ecommerce.draw()
```

## 🎨 可视化定制技巧

### 1. **按属性颜色编码**

可视化会根据顶点和超边的属性自动使用不同的颜色。

### 2. **尺寸表示**

- **顶点大小**：通常表示度数（连接数）
- **超边粗细**：表示连接的顶点数量

### 3. **交互功能**

- **悬停**：查看顶点和超边的详细信息
- **点击**：选择元素以突出显示相关组件
- **拖拽**：重新排列布局以获得更好的视图
- **缩放**：使用鼠标滚轮进行缩放

### 4. **布局算法**

可视化默认使用力导向布局，特点：
- 将相关顶点聚集在一起
- 最小化边的交叉
- 创建美观的排列

### 5. **跨平台兼容性** 🆕

#### Windows 用户注意事项

在 Windows 系统上使用 `draw()` 函数时，我们已经优化了 Ctrl+C 处理：

```python
# 基本用法（阻塞模式）
hg.draw()  # 按 Ctrl+C 停止服务器

# 非阻塞模式（推荐用于脚本和自动化）
viewer = hg.draw(blocking=False)
# 执行其他操作...
viewer.stop_server()  # 手动停止服务器
```

#### 平台差异

| 操作系统 | Ctrl+C 行为 | 推荐使用方式 |
|---------|------------|-------------|
| **Windows** | ✅ 优化后正常工作 | 两种模式均可 |
| **macOS/Linux** | ✅ 原生支持良好 | 默认阻塞模式 |

#### 使用建议

```python
# 1. 交互式探索（推荐阻塞模式）
hg.draw(port=8080, blocking=True)

# 2. 脚本自动化（推荐非阻塞模式）
viewer = hg.draw(port=8080, blocking=False)
# 执行其他分析...
time.sleep(30)  # 让用户有时间查看
viewer.stop_server()

# 3. Jupyter Notebook 中使用
viewer = hg.draw(blocking=False)  # 不阻塞单元格执行
```

## 🔍 通过可视化进行分析

### 识别模式

1. **集群**：紧密连接的顶点群
2. **中心节点**：有很多连接的顶点（高度数）
3. **桥梁**：连接不同集群的超边
4. **异常值**：孤立或很少连接的顶点

### 网络指标可视化

```python
# 示例：通过可视化分析网络中心性
def analyze_network_visually(hg):
    print("🎯 网络分析：")
    
    # 度分布
    degrees = [hg.degree_v(v) for v in hg.all_v]
    print(f"📊 平均度数：{sum(degrees)/len(degrees):.2f}")
    
    # 中心节点识别
    hubs = [v for v in hg.all_v if hg.degree_v(v) > sum(degrees)/len(degrees)]
    print(f"🌟 网络中心节点：{len(hubs)} 个顶点")
    
    # 超边大小分布
    edge_sizes = [hg.degree_e(e) for e in hg.all_e]
    print(f"🔗 平均超边大小：{sum(edge_sizes)/len(edge_sizes):.2f}")
    
    # 带分析的可视化
    hg.draw()

# 应用于上述任何示例
analyze_network_visually(social_network)
```

## 🚀 高级可视化技术

### 动态可视化

对于时间序列数据，您可以创建多个快照：

```python
# 示例：演化的社交网络
def create_network_snapshots(base_network, time_periods):
    snapshots = []
    for period in time_periods:
        # 为每个时间段创建过滤的网络
        period_network = HypergraphDB()
        
        # 添加顶点（人员不变）
        for v in base_network.all_v:
            period_network.add_v(v, base_network.v(v))
        
        # 只添加此时间段的超边
        for e in base_network.all_e:
            edge_data = base_network.e(e)
            if edge_data.get('date', '') >= period['start'] and edge_data.get('date', '') <= period['end']:
                period_network.add_e(base_network.e_v(e), edge_data)
        
        snapshots.append((period['name'], period_network))
    
    return snapshots

# 创建季度快照
quarters = [
    {"name": "2024年第一季度", "start": "2024-01-01", "end": "2024-03-31"},
    {"name": "2024年第二季度", "start": "2024-04-01", "end": "2024-06-30"}
]

# 可视化演化
for quarter_name, network in create_network_snapshots(social_network, quarters):
    print(f"📅 {quarter_name}：")
    network.draw()
```

这种可视化方法帮助您理解超图数据中复杂关系的结构和演化！
