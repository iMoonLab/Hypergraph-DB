/**
 * 超图布局（浏览器全局版）/ Hypergraph layout (browser global build)
 *
 * 由 G6 仓库 hypergraph/build-hypergraph-layout.mjs 生成，请勿手改。
 * 在 G6 UMD 包（window.G6）之后以 <script> 引入，加载后自动注册为 'hypergraph' 布局，并暴露 window.HypergraphLayout；
 * 同时覆盖注册 'bubble-sets'，支持 memberBoundsType: 'key'（只圈节点、不包裹标签），并暴露 window.KeyBoundsBubbleSets 供继承。
 * Generated, do not edit. Load after the G6 UMD bundle; registers the 'hypergraph' layout and exposes window.HypergraphLayout,
 * and re-registers 'bubble-sets' with support for memberBoundsType: 'key' (wrap nodes only, not labels), exposing window.KeyBoundsBubbleSets to extend.
 */
(function (G6) {
  const { BaseLayout } = G6;
const parseSize = (size = 0) => {
    if (typeof size === 'number')
        return [size, size, size];
    const [x, y = x, z = x] = size;
    return [x, y, z];
};
const ALPHA_MIN = 0.001;
/**
 * <zh/> 超图布局
 *
 * <en/> Hypergraph layout
 * @remarks
 * <zh/> 基于力导向的超图布局，让同一超边连接的节点尽量聚在一起，便于配合 bubble-sets 绘制超边。每条超边（3 个及以上成员）被展开为一个虚拟中心点，成员通过弹簧与之相连（星形展开）；非成员节点被推出超边成员的凸包（同属某个更大超边的节点除外），不同超边之间按共享成员的多少相互排斥。2 元超边直接作为弹簧，并把非成员节点推离其连线。
 *
 * <en/> A force-directed hypergraph layout that keeps the members of a hyperedge close together, to be drawn with bubble-sets. Each hyperedge with 3 or more members is expanded into a virtual center node linked to its members by springs (star expansion); non-member nodes are pushed out of the members' convex hull (unless they share a larger hyperedge containing it), and hyperedges repel each other according to how few members they share. 2-member hyperedges act as plain springs that also push non-members off their segment.
 */
class HypergraphLayout extends BaseLayout {
    constructor() {
        super(...arguments);
        this.id = 'hypergraph';
        this.resolvedOptions = { type: 'hypergraph' };
        /**
         * <zh/> 执行若干次迭代，未指定次数时迭代至收敛
         *
         * <en/> Run several iterations, until convergence when no count is given
         * @param iterations - <zh/> 迭代次数 | <en/> iterations
         * @returns <zh/> 当前布局结果 | <en/> current layout result
         */
        this.tick = (iterations) => {
            const sim = this.simulation;
            if (!sim)
                return { nodes: [] };
            const limit = iterations !== null && iterations !== void 0 ? iterations : Infinity;
            for (let i = 0; i < limit && sim.alpha >= ALPHA_MIN; i++)
                step(sim, this.resolvedOptions);
            if (sim.alpha < ALPHA_MIN)
                settle(sim);
            return this.output();
        };
        this.stop = () => {
            if (this.timer !== undefined)
                clearTimeout(this.timer);
            this.timer = undefined;
        };
    }
    async execute(model, options) {
        this.stop();
        const opts = Object.assign({}, HypergraphLayout.defaultOptions, this.options, options);
        this.resolvedOptions = opts;
        this.simulation = initSimulation(model, opts);
        const { onTick, ticksPerFrame = 3 } = opts;
        if (!onTick) {
            this.tick();
            return this.output();
        }
        return new Promise((resolve) => {
            const frame = () => {
                const sim = this.simulation;
                for (let i = 0; i < ticksPerFrame && sim.alpha >= ALPHA_MIN; i++)
                    step(sim, this.resolvedOptions);
                if (sim.alpha < ALPHA_MIN)
                    settle(sim);
                const data = this.output();
                onTick(data);
                if (sim.alpha < ALPHA_MIN) {
                    this.timer = undefined;
                    resolve(data);
                }
                else
                    this.timer = setTimeout(frame, 16);
            };
            this.timer = setTimeout(frame, 0);
        });
    }
    output() {
        const sim = this.simulation;
        if (!sim)
            return { nodes: [] };
        return { nodes: sim.ids.map((id, i) => ({ id, style: { x: sim.x[i], y: sim.y[i] } })) };
    }
}
HypergraphLayout.defaultOptions = {
    nodeSize: 20,
    nodeSpacing: 10,
    preventLabelOverlap: false,
    labelFontSize: 12,
    labelPlacement: 'bottom',
    labelPadding: 4,
    radiusFactor: 0.6,
    attraction: 1,
    repulsion: 1,
    exclusion: 1,
    hyperedgeRepulsion: 1,
    gravity: 0.05,
    iterations: 300,
    ticksPerFrame: 3,
    velocityDecay: 0.4,
    seed: 1,
};
/**
 * <zh/> 可复现的伪随机数（mulberry32）
 *
 * <en/> Reproducible pseudo random numbers (mulberry32)
 * @param seed - <zh/> 种子 | <en/> seed
 * @returns <zh/> 随机数生成器 | <en/> random number generator
 */
function createRandom(seed) {
    let a = seed >>> 0;
    return () => {
        a = (a + 0x6d2b79f5) >>> 0;
        let t = a;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
}
function resolveHyperedges(model, options) {
    const { hyperedges = [] } = options;
    const edges = (model.edges || []).map((edge) => ({ id: edge.id, members: [edge.source, edge.target] }));
    return [...(typeof hyperedges === 'function' ? hyperedges(model) : hyperedges), ...edges];
}
/**
 * <zh/> 贪心排序超边，使共享成员多的超边相邻
 *
 * <en/> Greedily order hyperedges so that the ones sharing more members are adjacent
 * @param sets - <zh/> 各超边的成员 | <en/> members of each hyperedge
 * @param shared - <zh/> 查询两条超边共享的成员数 | <en/> number of members shared by two hyperedges
 * @returns <zh/> 排序后的超边下标 | <en/> ordered hyperedge indices
 */
function orderByOverlap(sets, shared) {
    const rest = new Set(sets.map((_, i) => i));
    const order = [];
    const largest = () => [...rest].reduce((a, b) => (sets[b].length > sets[a].length ? b : a));
    let current = rest.size ? largest() : -1;
    while (current !== -1) {
        order.push(current);
        rest.delete(current);
        if (!rest.size)
            break;
        let next = -1;
        let best = 0;
        rest.forEach((candidate) => {
            const score = shared(current, candidate) / Math.min(sets[current].length, sets[candidate].length);
            if (score > best || (score === best && next !== -1 && sets[candidate].length > sets[next].length)) {
                best = score;
                next = candidate;
            }
        });
        current = best > 0 ? next : largest();
    }
    return order;
}
function initSimulation(model, options) {
    var _a;
    const { nodeSize = 20, nodeSpacing = 10, radiusFactor = 0.6, centerNode, center, width = 0, height = 0, iterations = 300, seed = 1, preventLabelOverlap = false, } = options;
    const random = createRandom(seed);
    const nodes = model.nodes || [];
    const n = nodes.length;
    const ids = nodes.map((node) => node.id);
    const indexOf = new Map(ids.map((id, i) => [id, i]));
    const sizeOf = typeof nodeSize === 'function' ? nodeSize : () => nodeSize;
    const diameter = nodes.reduce((max, node) => {
        const [w, h] = parseSize(sizeOf(node));
        return Math.max(max, w, h);
    }, 0);
    const spacing = diameter + nodeSpacing;
    const [cx, cy] = center || [width / 2, height / 2];
    const radius = Float64Array.from(nodes, (node) => Math.max(...parseSize(sizeOf(node))) / 2);
    const labels = preventLabelOverlap ? measureLabels(nodes, radius, options) : null;
    let reach = diameter / 2;
    if (labels) {
        for (let i = 0; i < n; i++) {
            const [dx, dy, hw, hh] = labels.subarray(i * 4, i * 4 + 4);
            reach = Math.max(reach, Math.abs(dx) + hw, Math.abs(dy) + hh);
        }
    }
    // 去重并剔除不在图中的成员 / Dedupe and drop members not in the graph
    const memberSets = [];
    const seen = new Set();
    resolveHyperedges(model, options).forEach(({ members }) => {
        const indices = [...new Set(members.map((id) => indexOf.get(id)).filter((i) => i !== undefined))];
        if (indices.length < 2)
            return;
        indices.sort((a, b) => a - b);
        const key = indices.join(',');
        if (seen.has(key))
            return;
        seen.add(key);
        memberSets.push(Int32Array.from(indices));
    });
    const hubSets = memberSets.filter((set) => set.length > 2);
    const pairSets = memberSets.filter((set) => set.length === 2);
    const degree = new Float64Array(n);
    const hubsOf = Array.from({ length: n }, () => []);
    hubSets.forEach((set, h) => set.forEach((v) => (degree[v]++, hubsOf[v].push(h))));
    pairSets.forEach(([u, v]) => (degree[u]++, degree[v]++));
    // 超边两两共享的成员数 / Members shared by each pair of hubs
    const hubCount = hubSets.length;
    const sharedCount = new Map();
    hubsOf.forEach((list) => {
        for (let a = 0; a < list.length; a++) {
            for (let b = a + 1; b < list.length; b++) {
                const key = list[a] * hubCount + list[b];
                sharedCount.set(key, (sharedCount.get(key) || 0) + 1);
            }
        }
    });
    const shared = (a, b) => sharedCount.get(Math.min(a, b) * hubCount + Math.max(a, b)) || 0;
    const hubWeights = new Float64Array(hubCount * hubCount);
    for (let a = 0; a < hubCount; a++) {
        for (let b = a + 1; b < hubCount; b++) {
            const weight = 1 - shared(a, b) / Math.min(hubSets[a].length, hubSets[b].length);
            hubWeights[a * hubCount + b] = hubWeights[b * hubCount + a] = weight;
        }
    }
    const hubParents = hubSets.map((set, a) => hubSets.map((_, b) => b).filter((b) => b !== a && shared(a, b) === set.length));
    const pairParents = pairSets.map(([u, v]) => hubsOf[u].filter((h) => hubsOf[v].includes(h)));
    const hubs = hubSets.map((members) => {
        const radius = radiusFactor * spacing * Math.sqrt(members.length);
        return { members, radius, rest: radius * 0.65, x: cx, y: cy, vx: 0, vy: 0 };
    });
    // 初始化：超边中心沿螺旋线（或绕中心节点的环）依次排布，共享成员多的超边相邻
    // Init: hub centers are laid along a spiral (or a ring around the center node), with overlapping hubs adjacent
    const x = new Float64Array(n);
    const y = new Float64Array(n);
    const placed = new Uint8Array(n);
    const fixed = centerNode !== undefined ? ((_a = indexOf.get(centerNode)) !== null && _a !== void 0 ? _a : -1) : -1;
    const order = orderByOverlap(hubSets, shared);
    if (fixed !== -1) {
        x[fixed] = cx;
        y[fixed] = cy;
        placed[fixed] = 1;
        // 每条超边占据一段角度，2 元超边的另一端作为花瓣上的叶子 / Each hyperedge takes an angular slot
        const leaves = pairSets.filter((set) => set[0] === fixed || set[1] === fixed).map(([u, v]) => (u === fixed ? v : u));
        const slots = [
            ...order.map((h) => ({ hub: h, leaf: -1, width: 2 * hubs[h].radius })),
            ...leaves.map((leaf) => ({ hub: -1, leaf, width: spacing })),
        ];
        const total = slots.reduce((sum, slot) => sum + slot.width, 0) || 1;
        let angle = 0;
        slots.forEach((slot) => {
            const theta = ((angle + slot.width / 2) / total) * Math.PI * 2;
            angle += slot.width;
            if (slot.hub !== -1) {
                const hub = hubs[slot.hub];
                const distance = Math.max(hub.rest, (total / (Math.PI * 2)) * 0.5);
                hub.x = cx + Math.cos(theta) * distance;
                hub.y = cy + Math.sin(theta) * distance;
            }
            else if (!hubsOf[slot.leaf].length) {
                const distance = Math.max(spacing * 1.5, total / (Math.PI * 2));
                x[slot.leaf] = cx + Math.cos(theta) * distance;
                y[slot.leaf] = cy + Math.sin(theta) * distance;
                placed[slot.leaf] = 1;
            }
        });
    }
    else {
        // 阿基米德螺线，按弧长依次放置 / Archimedean spiral, placed by arc length
        const gap = (spacing * 3) / (Math.PI * 2);
        let theta = 0;
        order.forEach((h, i) => {
            const hub = hubs[h];
            if (i > 0)
                theta += (2 * hub.radius) / Math.max(gap * theta, hub.radius);
            hub.x = cx + gap * theta * Math.cos(theta);
            hub.y = cy + gap * theta * Math.sin(theta);
        });
    }
    // 节点放在其所属超边中心的均值附近 / Nodes start around the mean of their hub centers
    for (let v = 0; v < n; v++) {
        if (placed[v] || !hubsOf[v].length)
            continue;
        let sx = 0;
        let sy = 0;
        let r = Infinity;
        hubsOf[v].forEach((h) => {
            sx += hubs[h].x;
            sy += hubs[h].y;
            r = Math.min(r, hubs[h].radius);
        });
        const angle = random() * Math.PI * 2;
        const distance = Math.sqrt(random()) * r * 0.8;
        x[v] = sx / hubsOf[v].length + Math.cos(angle) * distance;
        y[v] = sy / hubsOf[v].length + Math.sin(angle) * distance;
        placed[v] = 1;
    }
    // 只通过 2 元超边相连的节点，沿已放置的邻居逐层展开 / Nodes linked only by pairs grow out from placed neighbors
    const neighbors = Array.from({ length: n }, () => []);
    pairSets.forEach(([u, v]) => (neighbors[u].push(v), neighbors[v].push(u)));
    const queue = [];
    for (let v = 0; v < n; v++)
        if (placed[v])
            queue.push(v);
    const spread = spacing * Math.sqrt(n);
    for (let v = 0; v < n || queue.length;) {
        if (!queue.length) {
            while (v < n && placed[v])
                v++;
            if (v >= n)
                break;
            const angle = random() * Math.PI * 2;
            const distance = Math.sqrt(random()) * spread;
            x[v] = cx + Math.cos(angle) * distance;
            y[v] = cy + Math.sin(angle) * distance;
            placed[v] = 1;
            queue.push(v);
        }
        const u = queue.shift();
        neighbors[u].forEach((w) => {
            if (placed[w])
                return;
            const angle = random() * Math.PI * 2;
            x[w] = x[u] + Math.cos(angle) * spacing * 1.5;
            y[w] = y[u] + Math.sin(angle) * spacing * 1.5;
            placed[w] = 1;
            queue.push(w);
        });
    }
    const pairs = new Int32Array(pairSets.length * 2);
    pairSets.forEach(([u, v], i) => ((pairs[i * 2] = u), (pairs[i * 2 + 1] = v)));
    return {
        ids,
        x,
        y,
        vx: new Float64Array(n),
        vy: new Float64Array(n),
        degree,
        hubs,
        pairs,
        hubWeights,
        hubsOf,
        hubParents,
        pairParents,
        radius,
        labels,
        reach,
        settled: false,
        fixed,
        spacing,
        cx,
        cy,
        alpha: 1,
        alphaDecay: 1 - Math.pow(ALPHA_MIN, 1 / Math.max(1, iterations)),
    };
}
/**
 * <zh/> 均匀网格，用于邻域查询
 *
 * <en/> Uniform grid for neighborhood queries
 */
class Grid {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.cells = new Map();
        for (let i = 0; i < x.length; i++) {
            const key = this.key(Math.floor(x[i] / size), Math.floor(y[i] / size));
            const cell = this.cells.get(key);
            if (cell)
                cell.push(i);
            else
                this.cells.set(key, [i]);
        }
    }
    key(i, j) {
        return (i + 32768) * 65536 + (j + 32768);
    }
    /**
     * <zh/> 遍历包围盒内的点
     *
     * <en/> Visit points within a bounding box
     * @param x0 - <zh/> 左 | <en/> left
     * @param y0 - <zh/> 上 | <en/> top
     * @param x1 - <zh/> 右 | <en/> right
     * @param y1 - <zh/> 下 | <en/> bottom
     * @param visit - <zh/> 回调 | <en/> callback
     */
    query(x0, y0, x1, y1, visit) {
        var _a;
        const { size } = this;
        for (let i = Math.floor(x0 / size); i <= Math.floor(x1 / size); i++) {
            for (let j = Math.floor(y0 / size); j <= Math.floor(y1 / size); j++) {
                (_a = this.cells.get(this.key(i, j))) === null || _a === void 0 ? void 0 : _a.forEach(visit);
            }
        }
    }
}
function step(sim, options) {
    const { attraction = 1, repulsion = 1, exclusion = 1, hyperedgeRepulsion = 1, gravity = 0.05, velocityDecay = 0.4, } = options;
    const { x, y, vx, vy, degree, hubs, pairs, hubWeights, hubsOf, hubParents, pairParents, spacing, cx, cy, fixed } = sim;
    const sharesParent = (v, parents) => parents.some((p) => hubsOf[v].includes(p));
    const n = x.length;
    const alpha = sim.alpha;
    const pairRest = spacing * 1.5;
    // ① 成员 ↔ 超边中心弹簧 / member ↔ hub springs
    hubs.forEach((hub) => {
        const size = hub.members.length;
        hub.members.forEach((v) => {
            let dx = hub.x + hub.vx - x[v] - vx[v];
            let dy = hub.y + hub.vy - y[v] - vy[v];
            const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
            const l = ((d - hub.rest) / d) * alpha * (attraction / Math.min(degree[v], size));
            const bias = size / (size + degree[v]);
            dx *= l;
            dy *= l;
            vx[v] += dx * bias;
            vy[v] += dy * bias;
            hub.vx -= dx * (1 - bias);
            hub.vy -= dy * (1 - bias);
        });
    });
    // 2 元超边弹簧 / springs of 2-member hyperedges
    for (let i = 0; i < pairs.length; i += 2) {
        const u = pairs[i];
        const v = pairs[i + 1];
        let dx = x[v] + vx[v] - x[u] - vx[u];
        let dy = y[v] + vy[v] - y[u] - vy[u];
        const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
        const l = ((d - pairRest) / d) * alpha * (attraction / Math.min(degree[u], degree[v]));
        const bias = degree[u] / (degree[u] + degree[v]);
        dx *= l;
        dy *= l;
        vx[v] -= dx * bias;
        vy[v] -= dy * bias;
        vx[u] += dx * (1 - bias);
        vy[u] += dy * (1 - bias);
    }
    // ② 节点排斥 + 碰撞（截断距离内） / node repulsion + collision within a cutoff
    const range = spacing * 4;
    const grid = new Grid(x, y, range);
    const charge = repulsion * spacing * spacing * 0.5;
    for (let i = 0; i < n; i++) {
        grid.query(x[i] - range, y[i] - range, x[i] + range, y[i] + range, (j) => {
            if (j <= i)
                return;
            let dx = x[j] - x[i];
            let dy = y[j] - y[i];
            let d2 = dx * dx + dy * dy;
            if (d2 > range * range)
                return;
            if (d2 < 1e-6) {
                dx = (i - j) * 1e-3;
                dy = 1e-3;
                d2 = dx * dx + dy * dy;
            }
            const d = Math.sqrt(d2);
            let f = (charge * alpha) / d2;
            // 重叠时与 alpha 无关地强制分开 / Overlapping nodes are pushed apart regardless of alpha
            if (d < spacing)
                f += (spacing - d) * 0.35;
            const fx = (dx / d) * f;
            const fy = (dy / d) * f;
            vx[i] -= fx;
            vy[i] -= fy;
            vx[j] += fx;
            vy[j] += fy;
        });
    }
    // 标签碰撞：标签之间、标签与节点之间互相推开。强度随 (1 - alpha)² 渐入：开始时节点都挤在一起，
    // 满强度的标签碰撞像一股很大的随机斥力，会把节点推进别的超边轮廓（30 个子图上入侵数约翻倍）；
    // 收敛后的 settle 再清理剩余重叠
    // label collision: labels keep off each other and off nodes. Phased in by (1 - alpha)²: at the start every
    // node is crowded, and a full-strength label push acts like a large random repulsion that shoves nodes into
    // other hyperedges (about twice the intrusions over 30 subgraphs); settle() removes what is left after convergence
    const labelWeight = (1 - alpha) * (1 - alpha);
    if (sim.labels && labelWeight > 0) {
        forEachBoxOverlap(sim, grid, (i, j, ox, oy) => {
            vx[i] -= ox * labelWeight;
            vy[i] -= oy * labelWeight;
            vx[j] += ox * labelWeight;
            vy[j] += oy * labelWeight;
        });
    }
    // ③ 非成员排斥：将非成员推出超边成员的凸包（外扩 margin），即 bubble-sets 轮廓所在区域
    // exclusion: push non-members out of the members' convex hull grown by a margin, where the bubble-sets contour lies
    const mark = new Int32Array(n);
    const margin = spacing * 0.75;
    hubs.forEach((hub, h) => {
        // 成员尚未聚拢时凸包几乎覆盖全图，推开非成员既无意义又会退化为 O(N)，等聚拢后再生效
        // While members are still scattered the hull spans the whole layout: skip until they gather
        let extent = 0;
        hub.members.forEach((v) => {
            mark[v] = h + 1;
            extent = Math.max(extent, Math.abs(x[v] - hub.x), Math.abs(y[v] - hub.y));
        });
        if (extent > hub.radius * 2.5)
            return;
        const polygon = convexHull(hub.members, x, y);
        let x0 = Infinity;
        let y0 = Infinity;
        let x1 = -Infinity;
        let y1 = -Infinity;
        for (let i = 0; i < polygon.length; i += 2) {
            x0 = Math.min(x0, polygon[i]);
            x1 = Math.max(x1, polygon[i]);
            y0 = Math.min(y0, polygon[i + 1]);
            y1 = Math.max(y1, polygon[i + 1]);
        }
        grid.query(x0 - margin, y0 - margin, x1 + margin, y1 + margin, (v) => {
            if (mark[v] === h + 1 || sharesParent(v, hubParents[h]))
                return;
            const [distance, nx, ny] = signedDistance(polygon, x[v], y[v]);
            if (distance >= margin)
                return;
            const f = (margin - distance) * exclusion * Math.max(alpha, 0.1) * 0.5;
            vx[v] += nx * f * 0.8;
            vy[v] += ny * f * 0.8;
            hub.vx -= nx * f * 0.2;
            hub.vy -= ny * f * 0.2;
        });
    });
    // 非成员远离 2 元超边的连线 / non-members keep off the segment of 2-member hyperedges
    for (let i = 0; i < pairs.length; i += 2) {
        const u = pairs[i];
        const v = pairs[i + 1];
        const ex = x[v] - x[u];
        const ey = y[v] - y[u];
        const len2 = ex * ex + ey * ey;
        if (len2 < 1e-6 || len2 > pairRest * pairRest * 9)
            continue;
        grid.query(Math.min(x[u], x[v]) - margin, Math.min(y[u], y[v]) - margin, Math.max(x[u], x[v]) + margin, Math.max(y[u], y[v]) + margin, (w) => {
            if (w === u || w === v || sharesParent(w, pairParents[i / 2]))
                return;
            const t = ((x[w] - x[u]) * ex + (y[w] - y[u]) * ey) / len2;
            if (t <= 0.05 || t >= 0.95)
                return;
            const dx = x[w] - (x[u] + ex * t);
            const dy = y[w] - (y[u] + ey * t);
            const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
            if (d >= margin)
                return;
            const f = ((margin - d) / d) * exclusion * Math.max(alpha, 0.1) * 0.5;
            vx[w] += dx * f;
            vy[w] += dy * f;
        });
    }
    // ④ 超边中心之间排斥，共享成员越多越弱 / hub repulsion, weakened by shared members
    const hubCount = hubs.length;
    for (let a = 0; a < hubCount; a++) {
        for (let b = a + 1; b < hubCount; b++) {
            const weight = hubWeights[a * hubCount + b] * hyperedgeRepulsion;
            if (weight <= 0)
                continue;
            const A = hubs[a];
            const B = hubs[b];
            let dx = B.x - A.x;
            let dy = B.y - A.y;
            let d2 = dx * dx + dy * dy;
            if (d2 < 1e-6) {
                dx = (a - b) * 1e-3;
                dy = 1e-3;
                d2 = dx * dx + dy * dy;
            }
            const reach = A.radius + B.radius;
            const d = Math.sqrt(d2);
            let f = (weight * reach * reach * 0.5 * alpha) / d2;
            if (d < reach)
                f += (reach - d) * weight * 0.1 * alpha;
            const fx = (dx / d) * f;
            const fy = (dy / d) * f;
            A.vx -= fx;
            A.vy -= fy;
            B.vx += fx;
            B.vy += fy;
        }
    }
    // ⑤ 向心力 / gravity
    const g = gravity * alpha;
    for (let i = 0; i < n; i++) {
        vx[i] += (cx - x[i]) * g;
        vy[i] += (cy - y[i]) * g;
    }
    hubs.forEach((hub) => {
        hub.vx += (cx - hub.x) * g;
        hub.vy += (cy - hub.y) * g;
    });
    // 积分 / integrate
    const decay = 1 - velocityDecay;
    const maxSpeed = spacing * 4;
    const clamp = (v) => Math.max(-maxSpeed, Math.min(maxSpeed, v));
    for (let i = 0; i < n; i++) {
        if (i === fixed) {
            x[i] = cx;
            y[i] = cy;
            vx[i] = vy[i] = 0;
            continue;
        }
        vx[i] = clamp(vx[i] * decay);
        vy[i] = clamp(vy[i] * decay);
        x[i] += vx[i];
        y[i] += vy[i];
    }
    hubs.forEach((hub) => {
        hub.vx = clamp(hub.vx * decay);
        hub.vy = clamp(hub.vy * decay);
        hub.x += hub.vx;
        hub.y += hub.vy;
    });
    sim.alpha += (0 - sim.alpha) * sim.alphaDecay;
}
/**
 * <zh/> 字符宽度（以字号为单位）的估计：CJK 1，大写字母 0.72，其他 0.6
 *
 * <en/> Estimated character width in font sizes: CJK 1, capital letters 0.72, others 0.6
 * @param char - <zh/> 字符 | <en/> character
 * @returns <zh/> 宽度 | <en/> width
 */
function charWidth(char) {
    const code = char.charCodeAt(0);
    if (code >= 0x2e80)
        return 1;
    if (code >= 65 && code <= 90)
        return 0.72;
    return 0.6;
}
/**
 * <zh/> 按文字估算标签包围盒，字符宽度见 charWidth
 *
 * <en/> Estimate label boxes from their text, see charWidth for character widths
 * @param nodes - <zh/> 节点 | <en/> nodes
 * @param radius - <zh/> 节点半径 | <en/> node radii
 * @param options - <zh/> 布局配置 | <en/> layout options
 * @returns <zh/> 标签包围盒 | <en/> label boxes
 */
function measureLabels(nodes, radius, options) {
    const { labelText, labelFontSize = 12, labelMaxWidth = Infinity, labelPlacement = 'bottom', labelPadding = 4 } = options;
    const textOf = labelText || ((node) => { var _a, _b; return String((_b = (_a = node.style) === null || _a === void 0 ? void 0 : _a.labelText) !== null && _b !== void 0 ? _b : node.id); });
    const boxes = new Float64Array(nodes.length * 4);
    nodes.forEach((node, i) => {
        let width = 0;
        let lines = 0;
        textOf(node)
            .split('\n')
            .forEach((line) => {
            let w = 0;
            for (const char of line)
                w += labelFontSize * charWidth(char);
            lines += Math.max(1, Math.ceil(w / labelMaxWidth));
            width = Math.max(width, Math.min(w, labelMaxWidth));
        });
        const hw = width / 2 + labelPadding / 2;
        const hh = (lines * labelFontSize * 1.3) / 2 + labelPadding / 2;
        const r = radius[i];
        const [dx, dy] = {
            bottom: [0, r + hh],
            top: [0, -r - hh],
            left: [-r - hw, 0],
            right: [r + hw, 0],
            center: [0, 0],
        }[labelPlacement];
        boxes.set([dx, dy, hw, hh], i * 4);
    });
    return boxes;
}
/**
 * <zh/> 遍历相互重叠的包围盒对（标签—标签、标签—节点），给出沿最小穿透轴的穿透量
 *
 * <en/> Visit overlapping box pairs (label–label, label–node) with the penetration along the axis of least penetration
 * @param sim - <zh/> 模拟状态 | <en/> simulation state
 * @param grid - <zh/> 节点网格 | <en/> node grid
 * @param visit - <zh/> 回调，(ox, oy) 为 j 相对 i 需要移开的量 | <en/> callback, (ox, oy) is how far j has to move away from i
 */
function forEachBoxOverlap(sim, grid, visit) {
    const { x, y, radius, reach } = sim;
    const labels = sim.labels;
    const n = x.length;
    const box = (i, label) => label
        ? [x[i] + labels[i * 4], y[i] + labels[i * 4 + 1], labels[i * 4 + 2], labels[i * 4 + 3]]
        : [x[i], y[i], radius[i], radius[i]];
    for (let i = 0; i < n; i++) {
        grid.query(x[i] - reach * 2, y[i] - reach * 2, x[i] + reach * 2, y[i] + reach * 2, (j) => {
            if (j <= i)
                return;
            // 三组盒子共用一个移开方向（按节点中心的相对位置），否则各组的方向可能互相抵消
            // The three box pairs share one direction (from the node centers), otherwise they may cancel each other out
            const sx = x[j] > x[i] || (x[j] === x[i] && i < j) ? 1 : -1;
            const sy = y[j] > y[i] || (y[j] === y[i] && i < j) ? 1 : -1;
            let needX = 0;
            let needY = 0;
            const test = (a, b) => {
                const dx = b[0] - a[0];
                const dy = b[1] - a[1];
                if (a[2] + b[2] <= Math.abs(dx) || a[3] + b[3] <= Math.abs(dy))
                    return;
                // 沿该方向移开所需的距离 / distance needed to separate along that direction
                needX = Math.max(needX, a[2] + b[2] - sx * dx);
                needY = Math.max(needY, a[3] + b[3] - sy * dy);
            };
            const li = box(i, true);
            const lj = box(j, true);
            test(li, lj);
            test(li, box(j, false));
            test(box(i, false), lj);
            if (!needX && !needY)
                return;
            if (needX < needY)
                visit(i, j, sx * needX, 0);
            else
                visit(i, j, 0, sy * needY);
        });
    }
}
/**
 * <zh/> 收敛后直接移动节点，消除剩余的标签重叠
 *
 * <en/> After convergence, move nodes directly to remove the remaining label overlaps
 * @param sim - <zh/> 模拟状态 | <en/> simulation state
 */
function settle(sim) {
    if (sim.settled)
        return;
    sim.settled = true;
    if (!sim.labels)
        return;
    const { x, y, fixed } = sim;
    for (let pass = 0; pass < 300; pass++) {
        let moved = false;
        forEachBoxOverlap(sim, new Grid(x, y, sim.reach * 2), (i, j, ox, oy) => {
            moved = true;
            // 多移 1px 以免浮点误差留下贴边重叠 / move 1px further so rounding does not leave them touching
            const sx = ox && ox + Math.sign(ox);
            const sy = oy && oy + Math.sign(oy);
            const wi = i === fixed ? 0 : j === fixed ? 1 : 0.5;
            x[i] -= sx * wi;
            y[i] -= sy * wi;
            x[j] += sx * (1 - wi);
            y[j] += sy * (1 - wi);
        });
        if (!moved)
            break;
    }
}
/**
 * <zh/> 计算点集凸包（单调链）
 *
 * <en/> Convex hull of a point set (monotone chain)
 * @param indices - <zh/> 点的下标 | <en/> point indices
 * @param x - <zh/> x 坐标 | <en/> x coordinates
 * @param y - <zh/> y 坐标 | <en/> y coordinates
 * @returns <zh/> 逆时针顶点，展开为 [x0, y0, x1, y1, ...] | <en/> counter-clockwise vertices, flattened
 */
function convexHull(indices, x, y) {
    const points = Array.from(indices).sort((a, b) => x[a] - x[b] || y[a] - y[b]);
    const cross = (o, a, b) => (x[a] - x[o]) * (y[b] - y[o]) - (y[a] - y[o]) * (x[b] - x[o]);
    const chain = (list) => {
        const result = [];
        list.forEach((p) => {
            while (result.length >= 2 && cross(result[result.length - 2], result[result.length - 1], p) <= 0)
                result.pop();
            result.push(p);
        });
        result.pop();
        return result;
    };
    const hull = [...chain(points), ...chain(points.reverse())];
    return hull.flatMap((i) => [x[i], y[i]]);
}
/**
 * <zh/> 点到凸多边形的有向距离（内部为负）及远离多边形的单位方向
 *
 * <en/> Signed distance from a point to a convex polygon (negative inside), and the unit direction away from it
 * @param polygon - <zh/> 多边形顶点，展开形式 | <en/> flattened polygon vertices
 * @param px - <zh/> 点 x | <en/> point x
 * @param py - <zh/> 点 y | <en/> point y
 * @returns <zh/> [距离, 方向 x, 方向 y] | <en/> [distance, direction x, direction y]
 */
function signedDistance(polygon, px, py) {
    const count = polygon.length / 2;
    let best = Infinity;
    let qx = px;
    let qy = py;
    let inside = count >= 3;
    for (let i = 0; i < count; i++) {
        const ax = polygon[i * 2];
        const ay = polygon[i * 2 + 1];
        const j = (i + 1) % count;
        const ex = polygon[j * 2] - ax;
        const ey = polygon[j * 2 + 1] - ay;
        const length2 = ex * ex + ey * ey;
        // 逆时针多边形，点在某条边右侧即在外部 / counter-clockwise polygon: right of any edge means outside
        if (ex * (py - ay) - ey * (px - ax) < 0)
            inside = false;
        const t = length2 ? Math.max(0, Math.min(1, ((px - ax) * ex + (py - ay) * ey) / length2)) : 0;
        const cx = ax + ex * t;
        const cy = ay + ey * t;
        const d = Math.hypot(px - cx, py - cy);
        if (d < best) {
            best = d;
            qx = cx;
            qy = cy;
        }
    }
    let nx = inside ? qx - px : px - qx;
    let ny = inside ? qy - py : py - qy;
    const length = Math.hypot(nx, ny);
    if (length > 1e-6) {
        nx /= length;
        ny /= length;
    }
    else {
        nx = 1;
        ny = 0;
    }
    return [inside ? -best : best, nx, ny];
}

  G6.register(G6.ExtensionCategory.LAYOUT, 'hypergraph', HypergraphLayout);
  window.HypergraphLayout = HypergraphLayout;
})(window.G6);

// bubble-sets 只圈节点：配置 memberBoundsType: 'key' / bubble-sets wrapping nodes only: set memberBoundsType: 'key'
(function (G6) {
  const { BubbleSets } = G6;
class KeyBoundsBubbleSets extends BubbleSets {
    constructor(context, options) {
        super(context, options);
        const self = this;
        const getPath = self.getPath;
        // getPath 同步地经 graph.getElementRenderBounds 取成员包围盒，调用期间临时换成主图形包围盒
        // getPath reads member bounds synchronously via graph.getElementRenderBounds: swap in key shape bounds while it runs
        self.getPath = (...args) => {
            if (self.options.memberBoundsType !== 'key')
                return getPath(...args);
            const graph = self.context.graph;
            graph.getElementRenderBounds = (id) => self.context.element.getElement(id).getShape('key').getRenderBounds();
            try {
                return getPath(...args);
            }
            finally {
                delete graph.getElementRenderBounds;
            }
        };
    }
}

  G6.register(G6.ExtensionCategory.PLUGIN, 'bubble-sets', KeyBoundsBubbleSets);
  window.KeyBoundsBubbleSets = KeyBoundsBubbleSets;
})(window.G6);
