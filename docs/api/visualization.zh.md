# 可视化

Hypergraph-DB 通过基于 Web 的交互式显示提供内置的可视化功能。

## HypergraphViewer 类

`HypergraphViewer` 类提供了超图的 Web 可视化功能。

## 使用示例

```python
from hyperdb import HypergraphDB

# 创建并填充超图
hg = HypergraphDB()
hg.add_v(1, {"name": "Alice"})
hg.add_v(2, {"name": "Bob"})
hg.add_v(3, {"name": "Charlie"})

hg.add_e((1, 2), {"relation": "朋友"})
hg.add_e((1, 2, 3), {"relation": "团队"})

# 可视化 - 在浏览器中打开
hg.draw()
```

## 可视化特性

- **交互式显示**: 点击和拖拽来探索超图结构
- **顶点信息**: 悬停在顶点上查看其属性
- **超边可视化**: 多路连接的可视化表示
- **基于 Web**: 在您的默认网页浏览器中运行
- **实时更新**: 反映当前超图状态

## 自定义

可以通过修改位于以下位置的 HTML 模板来自定义可视化：
```
hyperdb/templates/hypergraph_viewer.html
```

### 可用选项

调用 `draw()` 时，您可以指定：

- `port`: Web 服务器的端口号（默认：8080）
- `open_browser`: 是否自动打开浏览器（默认：True）

```python
# 使用自定义端口
hg.draw(port=9000)

# 不自动打开浏览器
hg.draw(open_browser=False)
```

## 技术细节

可视化系统：

1. **转换**超图数据为 JSON 格式
2. **生成**嵌入数据和 D3.js 可视化的 HTML
3. **启动**本地 Web 服务器
4. **打开**默认浏览器中的可视化

可视化使用：
- **D3.js** 进行交互式图形
- **本地 HTTP 服务器** 提供内容服务
- **JSON 数据嵌入** 实现高效数据传输

## 故障排除

### 常见问题

**端口已被使用：**
```python
# 尝试不同的端口
hg.draw(port=8081)
```

**浏览器未打开：**
- 手动导航到 `http://localhost:8080`（或您指定的端口）
- 检查防火墙设置

**可视化显示为空：**
- 确保您的超图有顶点和边
- 检查浏览器控制台中的 JavaScript 错误

### 性能考虑

- 大型超图（>1000个顶点）可能渲染缓慢
- 对于非常大的数据集，考虑过滤或采样
- 可视化会将所有数据加载到浏览器内存中

## 未来增强

计划中的改进包括：

- **导出功能**（PNG、SVG、PDF）
- **布局算法** 实现更好的可视化
- **过滤选项** 用于大型图
- **自定义样式** 和主题
- **交互式编辑** 功能
