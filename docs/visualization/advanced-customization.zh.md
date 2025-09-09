# 高级定制指南

本指南将深入探讨 Hypergraph-DB 可视化的高级定制功能，帮助您创建独特且专业的超图可视化效果。

## 高级样式系统

### 🎨 动态样式引擎

#### 基于数据的样式映射
```javascript
class StyleMapper {
    constructor(visualization) {
        this.viz = visualization;
        this.mappings = new Map();
    }
    
    // 创建样式映射规则
    createMapping(property, attribute, scale) {
        const mapping = {
            property,    // 视觉属性 (color, size, opacity)
            attribute,   // 数据属性 (degree, weight, type)
            scale        // 缩放函数
        };
        
        this.mappings.set(property, mapping);
        return this;
    }
    
    // 应用样式映射
    applyMappings(elements) {
        elements.forEach(element => {
            this.mappings.forEach((mapping, property) => {
                const value = element.data[mapping.attribute];
                const mappedValue = mapping.scale(value);
                element.style[property] = mappedValue;
            });
        });
    }
}

// 使用示例
const mapper = new StyleMapper(visualization);

// 根据度数映射节点大小
mapper.createMapping('size', 'degree', 
    d3.scaleLinear().domain([1, 20]).range([5, 30])
);

// 根据类型映射节点颜色
mapper.createMapping('color', 'type', 
    d3.scaleOrdinal()
      .domain(['researcher', 'institution', 'paper'])
      .range(['#e74c3c', '#3498db', '#2ecc71'])
);

// 根据权重映射边透明度
mapper.createMapping('opacity', 'weight',
    d3.scaleLinear().domain([0, 1]).range([0.3, 1.0])
);
```

#### 条件样式系统
```javascript
class ConditionalStyles {
    constructor() {
        this.rules = [];
    }
    
    addRule(condition, styles) {
        this.rules.push({ condition, styles });
        return this;
    }
    
    applyRules(element) {
        let appliedStyles = {};
        
        this.rules.forEach(rule => {
            if (rule.condition(element)) {
                Object.assign(appliedStyles, rule.styles);
            }
        });
        
        return appliedStyles;
    }
}

// 创建条件样式规则
const conditionalStyles = new ConditionalStyles()
    .addRule(
        element => element.degree > 10,
        { size: 25, color: '#e74c3c', strokeWidth: 3 }
    )
    .addRule(
        element => element.type === 'important',
        { glow: true, pulsate: true }
    )
    .addRule(
        element => element.selected,
        { stroke: '#f39c12', strokeWidth: 4 }
    );
```

### 🌈 渐变和纹理

#### SVG 渐变定义
```javascript
function createGradients(svg) {
    const defs = svg.append('defs');
    
    // 径向渐变
    const radialGradient = defs.append('radialGradient')
        .attr('id', 'node-gradient')
        .attr('cx', '30%')
        .attr('cy', '30%');
    
    radialGradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#ffffff')
        .attr('stop-opacity', 0.8);
    
    radialGradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', '#3498db')
        .attr('stop-opacity', 1);
    
    // 线性渐变
    const linearGradient = defs.append('linearGradient')
        .attr('id', 'edge-gradient')
        .attr('x1', '0%').attr('y1', '0%')
        .attr('x2', '100%').attr('y2', '0%');
    
    linearGradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#e74c3c')
        .attr('stop-opacity', 0.8);
    
    linearGradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', '#9b59b6')
        .attr('stop-opacity', 0.8);
}

// 应用渐变
nodes.style('fill', 'url(#node-gradient)');
edges.style('stroke', 'url(#edge-gradient)');
```

#### 纹理模式
```javascript
function createPatterns(svg) {
    const defs = svg.select('defs');
    
    // 创建点状纹理
    const dotPattern = defs.append('pattern')
        .attr('id', 'dots')
        .attr('patternUnits', 'userSpaceOnUse')
        .attr('width', 10)
        .attr('height', 10);
    
    dotPattern.append('circle')
        .attr('cx', 5)
        .attr('cy', 5)
        .attr('r', 2)
        .attr('fill', '#34495e')
        .attr('opacity', 0.3);
    
    // 创建条纹纹理
    const stripePattern = defs.append('pattern')
        .attr('id', 'stripes')
        .attr('patternUnits', 'userSpaceOnUse')
        .attr('width', 8)
        .attr('height', 8)
        .attr('patternTransform', 'rotate(45)');
    
    stripePattern.append('rect')
        .attr('width', 4)
        .attr('height', 8)
        .attr('fill', '#ecf0f1');
    
    stripePattern.append('rect')
        .attr('x', 4)
        .attr('width', 4)
        .attr('height', 8)
        .attr('fill', '#bdc3c7');
}
```

## 高级动画系统

### 🎬 关键帧动画

#### 复杂过渡动画
```javascript
class AnimationEngine {
    constructor() {
        this.animations = new Map();
        this.timeline = gsap.timeline();
    }
    
    // 创建节点出现动画
    animateNodeEntry(nodes) {
        return gsap.fromTo(nodes.nodes(), 
            {
                scale: 0,
                opacity: 0,
                rotation: 180
            },
            {
                scale: 1,
                opacity: 1,
                rotation: 0,
                duration: 0.8,
                ease: "back.out(1.7)",
                stagger: 0.1
            }
        );
    }
    
    // 创建边绘制动画
    animateEdgeDrawing(edges) {
        // 设置初始路径长度为0
        edges.each(function() {
            const pathLength = this.getTotalLength();
            d3.select(this)
                .attr('stroke-dasharray', pathLength)
                .attr('stroke-dashoffset', pathLength);
        });
        
        // 动画绘制路径
        return gsap.to(edges.nodes(), {
            strokeDashoffset: 0,
            duration: 1.5,
            ease: "power2.inOut",
            stagger: 0.05
        });
    }
    
    // 创建力引导布局动画
    animateLayoutTransition(nodes, newPositions) {
        const tween = gsap.to({}, {
            duration: 2,
            ease: "power2.inOut",
            onUpdate: function() {
                const progress = this.progress();
                nodes.each(function(d, i) {
                    const startPos = { x: d.x, y: d.y };
                    const endPos = newPositions[i];
                    
                    d.x = startPos.x + (endPos.x - startPos.x) * progress;
                    d.y = startPos.y + (endPos.y - startPos.y) * progress;
                    
                    d3.select(this)
                        .attr('transform', `translate(${d.x}, ${d.y})`);
                });
            }
        });
        
        return tween;
    }
}
```

#### 交互式动画反馈
```javascript
class InteractionAnimations {
    // 鼠标悬停效果
    static setupHoverEffects(elements) {
        elements
            .on('mouseenter', function(event, d) {
                gsap.to(this, {
                    scale: 1.2,
                    duration: 0.2,
                    ease: "power2.out"
                });
                
                // 添加发光效果
                gsap.to(this, {
                    filter: 'drop-shadow(0 0 10px rgba(52, 152, 219, 0.8))',
                    duration: 0.2
                });
            })
            .on('mouseleave', function(event, d) {
                gsap.to(this, {
                    scale: 1,
                    filter: 'none',
                    duration: 0.2,
                    ease: "power2.out"
                });
            });
    }
    
    // 点击反馈动画
    static setupClickEffects(elements) {
        elements.on('click', function(event, d) {
            // 创建涟漪效果
            const ripple = d3.select(this.parentNode)
                .append('circle')
                .attr('class', 'ripple')
                .attr('cx', d.x)
                .attr('cy', d.y)
                .attr('r', 0)
                .style('fill', 'none')
                .style('stroke', '#3498db')
                .style('stroke-width', 2)
                .style('opacity', 1);
            
            gsap.to(ripple.node(), {
                attr: { r: 50 },
                opacity: 0,
                duration: 0.6,
                ease: "power2.out",
                onComplete: () => ripple.remove()
            });
        });
    }
}
```

### 🌊 物理动画

#### 粒子系统
```javascript
class ParticleSystem {
    constructor(canvas, count = 100) {
        this.canvas = canvas;
        this.particles = [];
        this.createParticles(count);
    }
    
    createParticles(count) {
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                radius: Math.random() * 3 + 1,
                opacity: Math.random() * 0.5 + 0.2,
                color: d3.interpolateViridis(Math.random())
            });
        }
    }
    
    update() {
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // 边界反弹
            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.vx *= -1;
            }
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.vy *= -1;
            }
            
            // 重力和摩擦
            particle.vy += 0.01; // 重力
            particle.vx *= 0.99; // 摩擦
            particle.vy *= 0.99;
        });
    }
    
    render(context) {
        this.particles.forEach(particle => {
            context.globalAlpha = particle.opacity;
            context.fillStyle = particle.color;
            context.beginPath();
            context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            context.fill();
        });
    }
}
```

## 3D 可视化

### 🌐 WebGL 集成

#### Three.js 基础设置
```javascript
class Hypergraph3D {
    constructor(container) {
        this.container = container;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, 
            window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        
        this.init();
    }
    
    init() {
        // 设置渲染器
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0xffffff);
        this.container.appendChild(this.renderer.domElement);
        
        // 设置相机位置
        this.camera.position.set(0, 0, 100);
        
        // 添加光源
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 50);
        this.scene.add(directionalLight);
        
        this.animate();
    }
    
    createNode(data) {
        const geometry = new THREE.SphereGeometry(data.size || 5, 32, 32);
        const material = new THREE.MeshLambertMaterial({ 
            color: data.color || 0x3498db 
        });
        const mesh = new THREE.Mesh(geometry, material);
        
        mesh.position.set(data.x || 0, data.y || 0, data.z || 0);
        mesh.userData = data;
        
        this.scene.add(mesh);
        return mesh;
    }
    
    createEdge(source, target, data) {
        const geometry = new THREE.BufferGeometry();
        const vertices = new Float32Array([
            source.x, source.y, source.z,
            target.x, target.y, target.z
        ]);
        
        geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
        
        const material = new THREE.LineBasicMaterial({ 
            color: data.color || 0x95a5a6,
            linewidth: data.width || 1
        });
        
        const line = new THREE.Line(geometry, material);
        line.userData = data;
        
        this.scene.add(line);
        return line;
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}
```

#### 3D 布局算法
```javascript
class ForceDirected3D {
    constructor(nodes, edges) {
        this.nodes = nodes;
        this.edges = edges;
        this.alpha = 0.3;
        this.alphaDecay = 0.02;
    }
    
    step() {
        // 斥力计算
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const nodeA = this.nodes[i];
                const nodeB = this.nodes[j];
                
                const dx = nodeB.x - nodeA.x;
                const dy = nodeB.y - nodeA.y;
                const dz = nodeB.z - nodeA.z;
                
                const distance = Math.sqrt(dx*dx + dy*dy + dz*dz) + 0.01;
                const force = -50 / (distance * distance);
                
                const fx = (dx / distance) * force;
                const fy = (dy / distance) * force;
                const fz = (dz / distance) * force;
                
                nodeA.vx -= fx;
                nodeA.vy -= fy;
                nodeA.vz -= fz;
                nodeB.vx += fx;
                nodeB.vy += fy;
                nodeB.vz += fz;
            }
        }
        
        // 引力计算
        this.edges.forEach(edge => {
            const source = edge.source;
            const target = edge.target;
            
            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dz = target.z - source.z;
            
            const distance = Math.sqrt(dx*dx + dy*dy + dz*dz);
            const force = distance * 0.01;
            
            const fx = (dx / distance) * force;
            const fy = (dy / distance) * force;
            const fz = (dz / distance) * force;
            
            source.vx += fx;
            source.vy += fy;
            source.vz += fz;
            target.vx -= fx;
            target.vy -= fy;
            target.vz -= fz;
        });
        
        // 位置更新
        this.nodes.forEach(node => {
            node.vx *= 0.9; // 阻尼
            node.vy *= 0.9;
            node.vz *= 0.9;
            
            node.x += node.vx * this.alpha;
            node.y += node.vy * this.alpha;
            node.z += node.vz * this.alpha;
        });
        
        this.alpha *= (1 - this.alphaDecay);
    }
}
```

## 自定义布局算法

### 🧠 机器学习驱动布局

#### t-SNE 布局
```javascript
class TSNELayout {
    constructor(nodes, options = {}) {
        this.nodes = nodes;
        this.perplexity = options.perplexity || 30;
        this.learningRate = options.learningRate || 200;
        this.maxIterations = options.maxIterations || 1000;
        
        this.similarities = this.computeSimilarities();
        this.positions = this.initializePositions();
    }
    
    computeSimilarities() {
        const n = this.nodes.length;
        const similarities = new Array(n).fill(null).map(() => new Array(n).fill(0));
        
        // 计算节点特征相似度
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (i !== j) {
                    similarities[i][j] = this.featureSimilarity(
                        this.nodes[i], this.nodes[j]
                    );
                }
            }
        }
        
        return similarities;
    }
    
    featureSimilarity(nodeA, nodeB) {
        // 基于节点属性计算相似度
        const features = ['degree', 'betweenness', 'clustering'];
        let similarity = 0;
        
        features.forEach(feature => {
            const diff = Math.abs((nodeA[feature] || 0) - (nodeB[feature] || 0));
            similarity += Math.exp(-diff);
        });
        
        return similarity / features.length;
    }
    
    initializePositions() {
        return this.nodes.map(() => ({
            x: (Math.random() - 0.5) * 100,
            y: (Math.random() - 0.5) * 100
        }));
    }
    
    run() {
        for (let iter = 0; iter < this.maxIterations; iter++) {
            this.updatePositions();
            
            if (iter % 100 === 0) {
                console.log(`t-SNE iteration ${iter}`);
            }
        }
        
        return this.positions;
    }
    
    updatePositions() {
        const n = this.nodes.length;
        const gradients = new Array(n).fill(null).map(() => ({ x: 0, y: 0 }));
        
        // 计算梯度
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (i !== j) {
                    const dx = this.positions[i].x - this.positions[j].x;
                    const dy = this.positions[i].y - this.positions[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy) + 1e-8;
                    
                    const similarity = this.similarities[i][j];
                    const attraction = similarity / dist;
                    const repulsion = 1 / (dist * dist);
                    
                    const force = attraction - repulsion;
                    
                    gradients[i].x += force * dx / dist;
                    gradients[i].y += force * dy / dist;
                }
            }
        }
        
        // 更新位置
        for (let i = 0; i < n; i++) {
            this.positions[i].x += gradients[i].x * this.learningRate;
            this.positions[i].y += gradients[i].y * this.learningRate;
        }
    }
}
```

#### 层次聚类布局
```javascript
class HierarchicalLayout {
    constructor(nodes, edges) {
        this.nodes = nodes;
        this.edges = edges;
        this.clusters = this.performClustering();
    }
    
    performClustering() {
        // 使用层次聚类算法
        let clusters = this.nodes.map((node, i) => ({
            id: i,
            nodes: [node],
            center: { x: node.x, y: node.y },
            level: 0
        }));
        
        while (clusters.length > 1) {
            const { cluster1, cluster2 } = this.findClosestClusters(clusters);
            const mergedCluster = this.mergeClusters(cluster1, cluster2);
            
            clusters = clusters.filter(c => c !== cluster1 && c !== cluster2);
            clusters.push(mergedCluster);
        }
        
        return clusters[0];
    }
    
    findClosestClusters(clusters) {
        let minDistance = Infinity;
        let closest = { cluster1: null, cluster2: null };
        
        for (let i = 0; i < clusters.length; i++) {
            for (let j = i + 1; j < clusters.length; j++) {
                const distance = this.clusterDistance(clusters[i], clusters[j]);
                if (distance < minDistance) {
                    minDistance = distance;
                    closest = { cluster1: clusters[i], cluster2: clusters[j] };
                }
            }
        }
        
        return closest;
    }
    
    clusterDistance(cluster1, cluster2) {
        const dx = cluster1.center.x - cluster2.center.x;
        const dy = cluster1.center.y - cluster2.center.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
    
    mergeClusters(cluster1, cluster2) {
        const allNodes = [...cluster1.nodes, ...cluster2.nodes];
        const centerX = allNodes.reduce((sum, node) => sum + node.x, 0) / allNodes.length;
        const centerY = allNodes.reduce((sum, node) => sum + node.y, 0) / allNodes.length;
        
        return {
            id: `${cluster1.id}-${cluster2.id}`,
            nodes: allNodes,
            center: { x: centerX, y: centerY },
            level: Math.max(cluster1.level, cluster2.level) + 1,
            children: [cluster1, cluster2]
        };
    }
    
    generateLayout() {
        return this.layoutCluster(this.clusters, 0, 0, 400);
    }
    
    layoutCluster(cluster, centerX, centerY, radius) {
        if (cluster.nodes.length === 1) {
            cluster.nodes[0].x = centerX;
            cluster.nodes[0].y = centerY;
            return;
        }
        
        if (cluster.children) {
            const angleStep = (2 * Math.PI) / cluster.children.length;
            
            cluster.children.forEach((child, i) => {
                const angle = i * angleStep;
                const childX = centerX + Math.cos(angle) * radius * 0.5;
                const childY = centerY + Math.sin(angle) * radius * 0.5;
                
                this.layoutCluster(child, childX, childY, radius * 0.5);
            });
        }
    }
}
```

## 交互式数据探索

### 🔍 多维数据过滤

#### 动态过滤器组件
```javascript
class MultiDimensionalFilter {
    constructor(data, container) {
        this.data = data;
        this.container = container;
        this.filters = new Map();
        this.callbacks = [];
        
        this.createFilterUI();
    }
    
    createFilterUI() {
        const filterPanel = d3.select(this.container)
            .append('div')
            .attr('class', 'filter-panel');
        
        // 分析数据属性
        const attributes = this.analyzeAttributes();
        
        attributes.forEach(attr => {
            this.createAttributeFilter(filterPanel, attr);
        });
    }
    
    analyzeAttributes() {
        const attributes = [];
        const sample = this.data[0];
        
        Object.keys(sample).forEach(key => {
            const values = this.data.map(d => d[key]);
            const uniqueValues = [...new Set(values)];
            
            const attribute = {
                name: key,
                type: this.detectType(values),
                values: uniqueValues,
                min: Math.min(...values.filter(v => typeof v === 'number')),
                max: Math.max(...values.filter(v => typeof v === 'number'))
            };
            
            attributes.push(attribute);
        });
        
        return attributes;
    }
    
    createAttributeFilter(panel, attribute) {
        const filterGroup = panel.append('div')
            .attr('class', 'filter-group');
        
        filterGroup.append('label')
            .text(attribute.name);
        
        if (attribute.type === 'categorical') {
            this.createCategoricalFilter(filterGroup, attribute);
        } else if (attribute.type === 'numerical') {
            this.createNumericalFilter(filterGroup, attribute);
        } else if (attribute.type === 'temporal') {
            this.createTemporalFilter(filterGroup, attribute);
        }
    }
    
    createCategoricalFilter(container, attribute) {
        const checkboxGroup = container.append('div')
            .attr('class', 'checkbox-group');
        
        const checkboxes = checkboxGroup.selectAll('.checkbox')
            .data(attribute.values)
            .enter()
            .append('label')
            .attr('class', 'checkbox');
        
        checkboxes.append('input')
            .attr('type', 'checkbox')
            .attr('checked', true)
            .on('change', (event, d) => {
                this.updateFilter(attribute.name, d, event.target.checked);
            });
        
        checkboxes.append('span')
            .text(d => d);
    }
    
    createNumericalFilter(container, attribute) {
        const sliderContainer = container.append('div')
            .attr('class', 'slider-container');
        
        const slider = sliderContainer.append('input')
            .attr('type', 'range')
            .attr('min', attribute.min)
            .attr('max', attribute.max)
            .attr('value', attribute.max)
            .attr('step', (attribute.max - attribute.min) / 100)
            .on('input', (event) => {
                this.updateFilter(attribute.name, 'max', +event.target.value);
            });
        
        sliderContainer.append('span')
            .attr('class', 'slider-value')
            .text(attribute.max);
    }
    
    updateFilter(attribute, value, enabled) {
        if (!this.filters.has(attribute)) {
            this.filters.set(attribute, new Set());
        }
        
        const filter = this.filters.get(attribute);
        
        if (enabled) {
            filter.add(value);
        } else {
            filter.delete(value);
        }
        
        this.applyFilters();
    }
    
    applyFilters() {
        const filteredData = this.data.filter(item => {
            return Array.from(this.filters.entries()).every(([attr, values]) => {
                if (values.size === 0) return true;
                return values.has(item[attr]);
            });
        });
        
        this.callbacks.forEach(callback => callback(filteredData));
    }
    
    onFilterChange(callback) {
        this.callbacks.push(callback);
    }
}
```

### 📊 实时数据绑定

#### 数据流可视化
```javascript
class RealTimeHypergraph {
    constructor(container) {
        this.container = container;
        this.data = { nodes: [], edges: [] };
        this.updateQueue = [];
        this.isAnimating = false;
        
        this.visualization = new HypergraphVisualization(container);
        this.startUpdateLoop();
    }
    
    // 添加数据更新到队列
    queueUpdate(update) {
        this.updateQueue.push({
            ...update,
            timestamp: Date.now()
        });
    }
    
    // 开始更新循环
    startUpdateLoop() {
        const processUpdates = () => {
            if (this.updateQueue.length > 0 && !this.isAnimating) {
                this.processNextUpdate();
            }
            requestAnimationFrame(processUpdates);
        };
        
        processUpdates();
    }
    
    // 处理下一个更新
    processNextUpdate() {
        if (this.updateQueue.length === 0) return;
        
        this.isAnimating = true;
        const update = this.updateQueue.shift();
        
        switch (update.type) {
            case 'addNode':
                this.animateNodeAddition(update.data);
                break;
            case 'removeNode':
                this.animateNodeRemoval(update.data);
                break;
            case 'addEdge':
                this.animateEdgeAddition(update.data);
                break;
            case 'removeEdge':
                this.animateEdgeRemoval(update.data);
                break;
            case 'updateNode':
                this.animateNodeUpdate(update.data);
                break;
        }
    }
    
    animateNodeAddition(nodeData) {
        // 添加节点到数据
        this.data.nodes.push(nodeData);
        
        // 创建DOM元素
        const node = this.visualization.createNode(nodeData);
        
        // 入场动画
        gsap.fromTo(node, 
            { scale: 0, opacity: 0 },
            { 
                scale: 1, 
                opacity: 1, 
                duration: 0.5,
                ease: "back.out(1.7)",
                onComplete: () => {
                    this.isAnimating = false;
                }
            }
        );
    }
    
    animateNodeRemoval(nodeId) {
        const nodeIndex = this.data.nodes.findIndex(n => n.id === nodeId);
        if (nodeIndex === -1) return;
        
        const node = this.visualization.getNodeElement(nodeId);
        
        // 退场动画
        gsap.to(node, {
            scale: 0,
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => {
                // 移除数据和DOM
                this.data.nodes.splice(nodeIndex, 1);
                node.remove();
                this.isAnimating = false;
            }
        });
    }
    
    // WebSocket 连接实时数据
    connectWebSocket(url) {
        this.ws = new WebSocket(url);
        
        this.ws.onmessage = (event) => {
            const update = JSON.parse(event.data);
            this.queueUpdate(update);
        };
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            // 尝试重连
            setTimeout(() => this.connectWebSocket(url), 5000);
        };
    }
}
```

## 性能优化技术

### ⚡ 虚拟化和LOD

#### 视口裁剪
```javascript
class ViewportCulling {
    constructor(visualization) {
        this.viz = visualization;
        this.viewportBounds = null;
        this.margin = 100; // 视口边距
    }
    
    updateViewportBounds() {
        const transform = this.viz.getTransform();
        const { width, height } = this.viz.getSize();
        
        this.viewportBounds = {
            left: -transform.x / transform.k - this.margin,
            top: -transform.y / transform.k - this.margin,
            right: (-transform.x + width) / transform.k + this.margin,
            bottom: (-transform.y + height) / transform.k + this.margin
        };
    }
    
    isInViewport(element) {
        if (!this.viewportBounds) return true;
        
        const { left, top, right, bottom } = this.viewportBounds;
        
        return element.x >= left && element.x <= right &&
               element.y >= top && element.y <= bottom;
    }
    
    filterVisibleElements(elements) {
        this.updateViewportBounds();
        return elements.filter(element => this.isInViewport(element));
    }
}
```

#### 细节层次控制
```javascript
class LevelOfDetail {
    constructor() {
        this.thresholds = [
            { scale: 0.1, level: 'minimal' },
            { scale: 0.5, level: 'low' },
            { scale: 1.0, level: 'medium' },
            { scale: 2.0, level: 'high' },
            { scale: 5.0, level: 'maximum' }
        ];
    }
    
    getLODLevel(scale) {
        for (let i = this.thresholds.length - 1; i >= 0; i--) {
            if (scale >= this.thresholds[i].scale) {
                return this.thresholds[i].level;
            }
        }
        return 'minimal';
    }
    
    applyLOD(elements, scale) {
        const level = this.getLODLevel(scale);
        
        elements.forEach(element => {
            switch (level) {
                case 'minimal':
                    this.applyMinimalLOD(element);
                    break;
                case 'low':
                    this.applyLowLOD(element);
                    break;
                case 'medium':
                    this.applyMediumLOD(element);
                    break;
                case 'high':
                    this.applyHighLOD(element);
                    break;
                case 'maximum':
                    this.applyMaximumLOD(element);
                    break;
            }
        });
    }
    
    applyMinimalLOD(element) {
        // 最简显示：只显示基本形状
        element.style.display = element.important ? 'block' : 'none';
        element.querySelector('.label').style.display = 'none';
        element.querySelector('.details').style.display = 'none';
    }
    
    applyMaximumLOD(element) {
        // 最详细显示：显示所有细节
        element.style.display = 'block';
        element.querySelector('.label').style.display = 'block';
        element.querySelector('.details').style.display = 'block';
    }
}
```

### 🏃 Web Workers 并行计算

#### 布局计算 Worker
```javascript
// layout-worker.js
class LayoutWorker {
    constructor() {
        self.onmessage = this.handleMessage.bind(this);
    }
    
    handleMessage(event) {
        const { type, data } = event.data;
        
        switch (type) {
            case 'forceLayout':
                this.computeForceLayout(data);
                break;
            case 'clustering':
                this.computeClustering(data);
                break;
        }
    }
    
    computeForceLayout(data) {
        const { nodes, edges, iterations } = data;
        
        for (let i = 0; i < iterations; i++) {
            // 力引导计算
            this.applyForces(nodes, edges);
            
            // 定期报告进度
            if (i % 10 === 0) {
                self.postMessage({
                    type: 'progress',
                    iteration: i,
                    total: iterations
                });
            }
        }
        
        // 返回结果
        self.postMessage({
            type: 'layoutComplete',
            positions: nodes.map(n => ({ id: n.id, x: n.x, y: n.y }))
        });
    }
    
    applyForces(nodes, edges) {
        // 重置力
        nodes.forEach(node => {
            node.fx = 0;
            node.fy = 0;
        });
        
        // 计算斥力
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const nodeA = nodes[i];
                const nodeB = nodes[j];
                
                const dx = nodeB.x - nodeA.x;
                const dy = nodeB.y - nodeA.y;
                const distance = Math.sqrt(dx*dx + dy*dy) + 0.01;
                
                const force = -1000 / (distance * distance);
                const fx = (dx / distance) * force;
                const fy = (dy / distance) * force;
                
                nodeA.fx -= fx;
                nodeA.fy -= fy;
                nodeB.fx += fx;
                nodeB.fy += fy;
            }
        }
        
        // 计算引力
        edges.forEach(edge => {
            const source = nodes.find(n => n.id === edge.source);
            const target = nodes.find(n => n.id === edge.target);
            
            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const distance = Math.sqrt(dx*dx + dy*dy);
            
            const force = distance * 0.01;
            const fx = (dx / distance) * force;
            const fy = (dy / distance) * force;
            
            source.fx += fx;
            source.fy += fy;
            target.fx -= fx;
            target.fy -= fy;
        });
        
        // 更新位置
        nodes.forEach(node => {
            node.x += node.fx * 0.01;
            node.y += node.fy * 0.01;
        });
    }
}

new LayoutWorker();
```

#### 主线程使用 Worker
```javascript
class ParallelLayoutEngine {
    constructor() {
        this.worker = new Worker('layout-worker.js');
        this.worker.onmessage = this.handleWorkerMessage.bind(this);
    }
    
    computeLayout(nodes, edges, callback) {
        this.layoutCallback = callback;
        
        this.worker.postMessage({
            type: 'forceLayout',
            data: {
                nodes: nodes.map(n => ({ 
                    id: n.id, 
                    x: n.x, 
                    y: n.y 
                })),
                edges: edges.map(e => ({ 
                    source: e.source.id, 
                    target: e.target.id 
                })),
                iterations: 500
            }
        });
    }
    
    handleWorkerMessage(event) {
        const { type, data } = event.data;
        
        switch (type) {
            case 'progress':
                console.log(`Layout progress: ${data.iteration}/${data.total}`);
                break;
            case 'layoutComplete':
                this.layoutCallback(data.positions);
                break;
        }
    }
}
```

## 下一步

您现在已经掌握了 Hypergraph-DB 的高级定制技巧！接下来可以：

1. 🚀 将这些技术应用到实际项目中
2. 📖 查看 [API 参考文档](../api/index.zh.md)
3. 💡 探索 [实际应用示例](../examples/basic-usage.zh.md)
4. 🤝 参与 [社区讨论](https://github.com/iMoonLab/Hypergraph-DB/discussions)

创建令人惊叹的超图可视化体验！
