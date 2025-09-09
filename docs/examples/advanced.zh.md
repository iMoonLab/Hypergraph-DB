# 高级示例

本页展示了 Hypergraph-DB 的高级使用模式和复杂应用。

## 高级模式 1：时态超图

建模随时间演化的关系：

```python
from hyperdb import HypergraphDB
from datetime import datetime, timedelta
import json

class TemporalHypergraph(HypergraphDB):
    """扩展的 HypergraphDB，具有时态功能。"""
    
    def add_temporal_edge(self, vertices, start_time, end_time=None, **kwargs):
        """添加具有时间信息的超边。"""
        edge_attr = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat() if end_time else None,
            "active": end_time is None or datetime.now() <= end_time,
            **kwargs
        }
        return self.add_e(vertices, edge_attr)
    
    def get_active_edges_at_time(self, timestamp):
        """获取在特定时间活跃的所有边。"""
        active_edges = []
        for edge_id in self.all_e:
            edge_data = self.e[edge_id]
            start = datetime.fromisoformat(edge_data["start_time"])
            end = datetime.fromisoformat(edge_data["end_time"]) if edge_data["end_time"] else datetime.now()
            
            if start <= timestamp <= end:
                active_edges.append(edge_id)
        return active_edges
    
    def get_edge_timeline(self, vertex_id):
        """获取涉及某个顶点的所有边的时间线。"""
        timeline = []
        for edge_id in self.N_e(vertex_id):
            edge_data = self.e[edge_id]
            timeline.append({
                "edge_id": edge_id,
                "vertices": list(self.N_v_of_e(edge_id)),
                "start": edge_data["start_time"],
                "end": edge_data["end_time"],
                "duration_days": self._calculate_duration(edge_data)
            })
        return sorted(timeline, key=lambda x: x["start"])
    
    def _calculate_duration(self, edge_data):
        """计算边的持续时间（天数）。"""
        start = datetime.fromisoformat(edge_data["start_time"])
        end = datetime.fromisoformat(edge_data["end_time"]) if edge_data["end_time"] else datetime.now()
        return (end - start).days

# 示例：学术合作网络随时间演化
temporal_hg = TemporalHypergraph()

# 添加研究人员
researchers = ["alice", "bob", "charlie", "diana", "eve"]
for researcher in researchers:
    temporal_hg.add_v(researcher, {"name": researcher.title(), "type": "researcher"})

# 添加时态合作关系
base_date = datetime(2020, 1, 1)

# 早期合作
temporal_hg.add_temporal_edge(
    ("alice", "bob"), 
    base_date, 
    base_date + timedelta(days=180),
    project="深度学习基础",
    type="research"
)

# 扩展合作
temporal_hg.add_temporal_edge(
    ("alice", "bob", "charlie"), 
    base_date + timedelta(days=90),
    base_date + timedelta(days=365),
    project="高级AI系统",
    type="research"
)

# 大团队组建
temporal_hg.add_temporal_edge(
    ("alice", "bob", "charlie", "diana", "eve"), 
    base_date + timedelta(days=200),
    base_date + timedelta(days=500),
    project="AI for Social Good",
    type="research",
    funding="NSF Grant"
)

# 持续合作
temporal_hg.add_temporal_edge(
    ("charlie", "diana"), 
    base_date + timedelta(days=300),
    project="可持续AI研究",
    type="research"
)

print("时态超图示例创建完成！")
```

## 高级模式 2：多层超图

构建具有不同关系层的复杂网络：

```python
class MultilayerHypergraph:
    """多层超图实现。"""
    
    def __init__(self):
        self.layers = {}
        self.interlayer_edges = []
        
    def add_layer(self, layer_name, layer_type="default"):
        """添加新的网络层。"""
        self.layers[layer_name] = {
            "graph": HypergraphDB(),
            "type": layer_type,
            "properties": {}
        }
    
    def add_vertex_to_layer(self, layer_name, vertex_id, **kwargs):
        """向特定层添加顶点。"""
        if layer_name not in self.layers:
            self.add_layer(layer_name)
        self.layers[layer_name]["graph"].add_v(vertex_id, kwargs)
    
    def add_edge_to_layer(self, layer_name, vertices, **kwargs):
        """向特定层添加边。"""
        if layer_name not in self.layers:
            self.add_layer(layer_name)
        return self.layers[layer_name]["graph"].add_e(vertices, kwargs)
    
    def add_interlayer_connection(self, vertex_id, layer1, layer2, **kwargs):
        """在层间添加连接。"""
        connection = {
            "vertex": vertex_id,
            "layers": [layer1, layer2],
            "properties": kwargs
        }
        self.interlayer_edges.append(connection)
    
    def get_multilayer_neighbors(self, vertex_id, include_interlayer=True):
        """获取多层邻居。"""
        neighbors = {}
        
        # 层内邻居
        for layer_name, layer_data in self.layers.items():
            if vertex_id in layer_data["graph"].all_v:
                layer_neighbors = list(layer_data["graph"].nbr_v(vertex_id))
                if layer_neighbors:
                    neighbors[layer_name] = layer_neighbors
        
        # 层间邻居
        if include_interlayer:
            interlayer_neighbors = []
            for connection in self.interlayer_edges:
                if connection["vertex"] == vertex_id:
                    interlayer_neighbors.extend(connection["layers"])
            if interlayer_neighbors:
                neighbors["interlayer"] = interlayer_neighbors
        
        return neighbors

# 示例：社交媒体多层网络
multilayer_net = MultilayerHypergraph()

# 创建不同的社交层
multilayer_net.add_layer("twitter", "social_media")
multilayer_net.add_layer("linkedin", "professional")
multilayer_net.add_layer("github", "collaboration")

# 在不同层添加用户
users = ["alice", "bob", "charlie", "diana"]

for user in users:
    multilayer_net.add_vertex_to_layer("twitter", user, platform="twitter")
    multilayer_net.add_vertex_to_layer("linkedin", user, platform="linkedin")
    multilayer_net.add_vertex_to_layer("github", user, platform="github")

# 添加层内连接
# Twitter 关注关系
multilayer_net.add_edge_to_layer("twitter", ("alice", "bob"), type="follow")
multilayer_net.add_edge_to_layer("twitter", ("bob", "charlie"), type="follow")

# LinkedIn 职业网络
multilayer_net.add_edge_to_layer("linkedin", ("alice", "diana"), type="connection")
multilayer_net.add_edge_to_layer("linkedin", ("bob", "diana"), type="connection")

# GitHub 协作
multilayer_net.add_edge_to_layer("github", ("alice", "bob", "charlie"), type="repository", name="ai-project")

# 添加层间连接（同一用户在不同平台）
for user in users:
    multilayer_net.add_interlayer_connection(user, "twitter", "linkedin")
    multilayer_net.add_interlayer_connection(user, "linkedin", "github")

print("多层超图示例创建完成！")
```

## 高级模式 3：动态图分析

分析图的演化模式和动态特性：

```python
class DynamicHypergraphAnalyzer:
    """动态超图分析器。"""
    
    def __init__(self):
        self.snapshots = {}
        self.metrics_timeline = {}
    
    def add_snapshot(self, timestamp, hypergraph):
        """添加图的快照。"""
        self.snapshots[timestamp] = hypergraph.copy() if hasattr(hypergraph, 'copy') else hypergraph
        self.update_metrics(timestamp, hypergraph)
    
    def update_metrics(self, timestamp, hg):
        """更新图度量指标。"""
        metrics = {
            "vertex_count": len(hg.v_list()),
            "edge_count": len(hg.e_list()),
            "density": self.calculate_density(hg),
            "max_degree": max([hg.degree_v(v) for v in hg.v_list()]) if hg.v_list() else 0,
            "avg_degree": sum([hg.degree_v(v) for v in hg.v_list()]) / len(hg.v_list()) if hg.v_list() else 0
        }
        self.metrics_timeline[timestamp] = metrics
    
    def calculate_density(self, hg):
        """计算图密度。"""
        vertices = hg.v_list()
        edges = hg.e_list()
        if len(vertices) < 2:
            return 0
        max_possible_edges = 2 ** len(vertices) - len(vertices) - 1
        return len(edges) / max_possible_edges if max_possible_edges > 0 else 0
    
    def detect_growth_patterns(self):
        """检测增长模式。"""
        timestamps = sorted(self.metrics_timeline.keys())
        patterns = {}
        
        for metric in ["vertex_count", "edge_count", "density"]:
            values = [self.metrics_timeline[t][metric] for t in timestamps]
            if len(values) > 1:
                growth_rates = []
                for i in range(1, len(values)):
                    if values[i-1] > 0:
                        rate = (values[i] - values[i-1]) / values[i-1]
                        growth_rates.append(rate)
                
                if growth_rates:
                    patterns[metric] = {
                        "avg_growth_rate": sum(growth_rates) / len(growth_rates),
                        "trend": "increasing" if growth_rates[-1] > 0 else "decreasing",
                        "volatility": max(growth_rates) - min(growth_rates)
                    }
        
        return patterns
    
    def find_structural_changes(self):
        """寻找结构变化点。"""
        timestamps = sorted(self.snapshots.keys())
        changes = []
        
        for i in range(1, len(timestamps)):
            prev_hg = self.snapshots[timestamps[i-1]]
            curr_hg = self.snapshots[timestamps[i]]
            
            # 检测新增和删除的顶点
            prev_vertices = set(prev_hg.v_list())
            curr_vertices = set(curr_hg.v_list())
            
            added_vertices = curr_vertices - prev_vertices
            removed_vertices = prev_vertices - curr_vertices
            
            if added_vertices or removed_vertices:
                changes.append({
                    "timestamp": timestamps[i],
                    "added_vertices": len(added_vertices),
                    "removed_vertices": len(removed_vertices),
                    "vertex_details": {
                        "added": list(added_vertices),
                        "removed": list(removed_vertices)
                    }
                })
        
        return changes

# 示例：科研合作网络的动态分析
analyzer = DynamicHypergraphAnalyzer()

# 模拟一年的网络演化
base_date = datetime(2023, 1, 1)
current_hg = HypergraphDB()

# 初始状态
current_hg.add_v("alice", {"type": "researcher", "field": "AI"})
current_hg.add_v("bob", {"type": "researcher", "field": "ML"})
current_hg.add_e(("alice", "bob"), {"type": "collaboration", "project": "initial"})

analyzer.add_snapshot(base_date, current_hg)

# 模拟月度变化
for month in range(1, 13):
    snapshot_date = base_date + timedelta(days=30*month)
    
    # 添加新研究者（概率性）
    if month % 3 == 0:  # 每三个月添加新人
        new_researcher = f"researcher_{month}"
        current_hg.add_v(new_researcher, {
            "type": "researcher", 
            "field": "interdisciplinary",
            "join_month": month
        })
        
        # 新人与现有研究者建立合作
        existing_researchers = [v for v in current_hg.v_list() if v != new_researcher]
        if len(existing_researchers) >= 2:
            # 创建三方合作
            collaboration = existing_researchers[:2] + [new_researcher]
            current_hg.add_e(collaboration, {
                "type": "collaboration",
                "project": f"project_month_{month}",
                "start_month": month
            })
    
    analyzer.add_snapshot(snapshot_date, current_hg)

# 分析结果
growth_patterns = analyzer.detect_growth_patterns()
structural_changes = analyzer.find_structural_changes()

print("网络增长模式：")
for metric, pattern in growth_patterns.items():
    print(f"  {metric}: 平均增长率 {pattern['avg_growth_rate']:.3f}, 趋势 {pattern['trend']}")

print(f"\n检测到 {len(structural_changes)} 个结构变化点")
```

## 高级模式 4：图神经网络集成

将超图与深度学习模型结合：

```python
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch 未安装，跳过神经网络示例")

if TORCH_AVAILABLE:
    class HypergraphGNN(nn.Module):
        """超图图神经网络。"""
        
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(HypergraphGNN, self).__init__()
            self.input_dim = input_dim
            self.hidden_dim = hidden_dim
            self.output_dim = output_dim
            
            # 顶点特征变换
            self.vertex_transform = nn.Linear(input_dim, hidden_dim)
            
            # 超边聚合
            self.edge_aggregation = nn.Linear(hidden_dim, hidden_dim)
            
            # 输出层
            self.output_layer = nn.Linear(hidden_dim, output_dim)
            
            # 激活函数
            self.activation = nn.ReLU()
            self.dropout = nn.Dropout(0.2)
        
        def forward(self, vertex_features, incidence_matrix):
            """前向传播。
            
            Args:
                vertex_features: [num_vertices, input_dim]
                incidence_matrix: [num_vertices, num_edges]
            """
            # 顶点特征变换
            h_vertices = self.activation(self.vertex_transform(vertex_features))
            h_vertices = self.dropout(h_vertices)
            
            # 超边聚合
            # 从顶点到超边：聚合连接到每个超边的顶点特征
            h_edges = torch.matmul(incidence_matrix.t(), h_vertices)  # [num_edges, hidden_dim]
            h_edges = self.activation(self.edge_aggregation(h_edges))
            
            # 从超边回到顶点：聚合每个顶点连接的超边特征
            h_vertices_updated = torch.matmul(incidence_matrix, h_edges)  # [num_vertices, hidden_dim]
            h_vertices_updated = self.activation(h_vertices_updated)
            
            # 输出预测
            output = self.output_layer(h_vertices_updated)
            return output
    
    class HypergraphGNNIntegration:
        """超图与GNN集成。"""
        
        def __init__(self, hypergraph):
            self.hg = hypergraph
            self.model = None
            self.vertex_to_idx = {}
            self.edge_to_idx = {}
        
        def prepare_data(self, vertex_features_dict):
            """准备训练数据。"""
            vertices = list(self.hg.v_list())
            edges = list(self.hg.e_list())
            
            # 创建索引映射
            self.vertex_to_idx = {v: i for i, v in enumerate(vertices)}
            self.edge_to_idx = {e: i for i, e in enumerate(edges)}
            
            # 准备顶点特征矩阵
            vertex_features = []
            for vertex in vertices:
                if vertex in vertex_features_dict:
                    vertex_features.append(vertex_features_dict[vertex])
                else:
                    # 默认特征
                    vertex_features.append([1.0] * len(list(vertex_features_dict.values())[0]))
            
            vertex_features = torch.FloatTensor(vertex_features)
            
            # 准备邻接矩阵（顶点-超边）
            incidence_matrix = torch.zeros(len(vertices), len(edges))
            for edge_idx, edge_id in enumerate(edges):
                connected_vertices = self.hg.N_v_of_e(edge_id)
                for vertex in connected_vertices:
                    vertex_idx = self.vertex_to_idx[vertex]
                    incidence_matrix[vertex_idx, edge_idx] = 1.0
            
            return vertex_features, incidence_matrix
        
        def train_model(self, vertex_features_dict, labels_dict, epochs=100):
            """训练模型。"""
            vertex_features, incidence_matrix = self.prepare_data(vertex_features_dict)
            
            # 准备标签
            vertices = list(self.hg.v_list())
            labels = []
            for vertex in vertices:
                if vertex in labels_dict:
                    labels.append(labels_dict[vertex])
                else:
                    labels.append(0)  # 默认标签
            labels = torch.LongTensor(labels)
            
            # 初始化模型
            input_dim = vertex_features.shape[1]
            hidden_dim = 64
            output_dim = len(set(labels.tolist()))
            
            self.model = HypergraphGNN(input_dim, hidden_dim, output_dim)
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
            criterion = nn.CrossEntropyLoss()
            
            # 训练循环
            for epoch in range(epochs):
                optimizer.zero_grad()
                output = self.model(vertex_features, incidence_matrix)
                loss = criterion(output, labels)
                loss.backward()
                optimizer.step()
                
                if epoch % 20 == 0:
                    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
        
        def predict(self, vertex_features_dict):
            """预测。"""
            if self.model is None:
                raise ValueError("模型尚未训练")
            
            vertex_features, incidence_matrix = self.prepare_data(vertex_features_dict)
            
            with torch.no_grad():
                output = self.model(vertex_features, incidence_matrix)
                predictions = F.softmax(output, dim=1)
            
            return predictions.numpy()

    # 示例：学术论文分类
    paper_hg = HypergraphDB()
    
    # 添加论文（顶点）
    papers = {
        "paper1": {"title": "Deep Learning Survey", "venue": "Nature"},
        "paper2": {"title": "Graph Neural Networks", "venue": "ICML"},
        "paper3": {"title": "Hypergraph Learning", "venue": "NIPS"},
        "paper4": {"title": "Reinforcement Learning", "venue": "JMLR"}
    }
    
    for paper_id, info in papers.items():
        paper_hg.add_v(paper_id, info)
    
    # 添加共同作者关系（超边）
    paper_hg.add_e(("paper1", "paper2"), {"type": "shared_author", "author": "Alice"})
    paper_hg.add_e(("paper2", "paper3"), {"type": "shared_author", "author": "Bob"})
    paper_hg.add_e(("paper1", "paper3", "paper4"), {"type": "shared_topic", "topic": "AI"})
    
    # 准备特征（这里使用简化的特征）
    paper_features = {
        "paper1": [1.0, 0.8, 0.3],  # [技术性, 影响因子, 新颖性]
        "paper2": [0.9, 0.7, 0.8],
        "paper3": [0.8, 0.6, 0.9],
        "paper4": [0.7, 0.9, 0.4]
    }
    
    # 准备标签（论文类别）
    paper_labels = {
        "paper1": 0,  # 综述
        "paper2": 1,  # 方法
        "paper3": 1,  # 方法
        "paper4": 1   # 方法
    }
    
    # 训练模型
    gnn_integration = HypergraphGNNIntegration(paper_hg)
    gnn_integration.train_model(paper_features, paper_labels, epochs=50)
    
    # 预测
    predictions = gnn_integration.predict(paper_features)
    print("论文分类预测结果：")
    for i, paper_id in enumerate(papers.keys()):
        pred_class = predictions[i].argmax()
        confidence = predictions[i].max()
        print(f"  {paper_id}: 类别 {pred_class} (置信度: {confidence:.3f})")

print("\n所有高级示例完成！")
```

这些高级示例展示了 Hypergraph-DB 的强大功能，包括：

1. **时态分析**：处理随时间演化的复杂关系
2. **多层网络**：建模不同类型的关系层
3. **动态分析**：跟踪和分析网络演化模式
4. **深度学习集成**：结合图神经网络进行预测和分类

这些模式可以应用于各种复杂的实际场景，如社交网络分析、科研合作网络、生物网络分析等。
