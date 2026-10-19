/* hypergraph-viz@0.1.0：由 HypergraphViewer/packages/hypergraph-viz 构建（npm run build）后经 scripts/copy-global.mjs 拷入，请勿手改。
 * 需先引入 G6 的 UMD 包（window.G6），全局变量为 window.HypergraphViz */
"use strict";
var HypergraphViz = (() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // g6-global:g6
  var require_g6 = __commonJS({
    "g6-global:g6"(exports, module) {
      "use strict";
      module.exports = window.G6;
    }
  });

  // src/index.ts
  var src_exports = {};
  __export(src_exports, {
    BUBBLE_SETS_TARGET: () => BUBBLE_SETS_TARGET,
    DEFAULT_THEME: () => DEFAULT_THEME,
    EDGE_SEPARATOR: () => EDGE_SEPARATOR,
    HOVER_BUBBLE_SETS: () => HOVER_BUBBLE_SETS,
    HYPERGRAPH_LAYOUT: () => HYPERGRAPH_LAYOUT,
    HoverBubbleSets: () => HoverBubbleSets,
    HypergraphLayout: () => HypergraphLayout,
    KeyBoundsBubbleSets: () => KeyBoundsBubbleSets,
    bubbleKeyOf: () => bubbleKeyOf,
    createHypergraphView: () => createHypergraphView,
    fromKeyedEdges: () => fromKeyedEdges,
    pairId: () => pairId,
    registerHypergraph: () => registerHypergraph,
    resolveTheme: () => resolveTheme,
    toG6Spec: () => toG6Spec,
    typeColorsOf: () => typeColorsOf
  });

  // src/adapters.ts
  var EDGE_SEPARATOR = "|#|";
  var fromKeyedEdges = (graph, separator = EDGE_SEPARATOR) => ({
    vertices: graph.vertices,
    hyperedges: Object.entries(graph.edges).map(
      ([key, edge]) => ({ ...edge, id: key, members: key.split(separator) })
    )
  });

  // src/bubble-sets-key.ts
  var import_g6 = __toESM(require_g6(), 1);
  var KeyBoundsBubbleSets = class extends import_g6.BubbleSets {
    constructor(context, options) {
      super(context, options);
      const self = this;
      const getPath = self.getPath;
      self.getPath = (...args) => {
        if (self.options.memberBoundsType !== "key") return getPath(...args);
        const graph = self.context.graph;
        graph.getElementRenderBounds = (id) => self.context.element.getElement(id).getShape("key").getRenderBounds();
        try {
          return getPath(...args);
        } finally {
          delete graph.getElementRenderBounds;
        }
      };
    }
  };

  // src/hover-bubble-sets.ts
  var import_g62 = __toESM(require_g6(), 1);
  var HOVER_BUBBLE_SETS = "hover-bubble-sets";
  var BUBBLE_SETS_TARGET = "bubble-sets";
  var SHAPE_EVENTS = [import_g62.CommonEvent.POINTER_OVER, import_g62.CommonEvent.POINTER_MOVE, import_g62.CommonEvent.POINTER_LEAVE, import_g62.CommonEvent.CLICK];
  var HoverBubbleSets = class extends KeyBoundsBubbleSets {
    constructor(context, options) {
      super(context, { zIndex: -1, pointerEvents: "all", ...options });
      this.layouting = false;
      this.boundKey = null;
      this.onBeforeLayout = () => {
        this.layouting = true;
        this.setContourVisible(false);
      };
      this.onAfterLayout = () => {
        this.layouting = false;
        this.drawBubbleSets();
      };
      this.forward = (event) => {
        this.context.graph.emit(event.type, {
          ...event,
          target: { ...this.options, id: this.options.key, options: this.options },
          targetType: BUBBLE_SETS_TARGET,
          originalTarget: event.target
        });
      };
      const self = this;
      const { graph } = this.context;
      graph.off(import_g62.GraphEvent.AFTER_RENDER, self.drawBubbleSets);
      const baseDraw = self.drawBubbleSets;
      self.drawBubbleSets = () => {
        self.init();
        baseDraw();
        this.bindShapeEvents();
        this.setContourVisible(!this.layouting);
      };
      graph.on(import_g62.GraphEvent.AFTER_RENDER, self.drawBubbleSets);
      graph.on(import_g62.GraphEvent.BEFORE_LAYOUT, this.onBeforeLayout);
      graph.on(import_g62.GraphEvent.AFTER_LAYOUT, this.onAfterLayout);
    }
    update(options) {
      super.update(options);
      const self = this;
      if (self.shape && !self.shape.destroyed) self.shape.update(self.parseOptions().style);
    }
    setContourVisible(visible) {
      const shape = this.shape;
      if (shape) shape.style.visibility = visible ? "visible" : "hidden";
    }
    bindShapeEvents() {
      const key = this.shape?.shapeMap?.key;
      if (!key || key === this.boundKey) return;
      this.unbindShapeEvents();
      key.style.pointerEvents = "all";
      SHAPE_EVENTS.forEach((type) => key.addEventListener(type, this.forward));
      this.boundKey = key;
    }
    unbindShapeEvents() {
      if (!this.boundKey) return;
      SHAPE_EVENTS.forEach((type) => this.boundKey.removeEventListener(type, this.forward));
      this.boundKey = null;
    }
    destroy() {
      const self = this;
      const { graph } = this.context;
      graph.off(import_g62.GraphEvent.AFTER_RENDER, self.drawBubbleSets);
      graph.off(import_g62.GraphEvent.BEFORE_LAYOUT, this.onBeforeLayout);
      graph.off(import_g62.GraphEvent.AFTER_LAYOUT, this.onAfterLayout);
      this.unbindShapeEvents();
      if (!self.shape) self.shape = { destroy: () => void 0 };
      super.destroy();
    }
  };

  // src/layout.ts
  var import_g63 = __toESM(require_g6(), 1);
  var parseSize = (size = 0) => {
    if (typeof size === "number") return [size, size, size];
    const [x, y = x, z = x] = size;
    return [x, y, z];
  };
  var ALPHA_MIN = 1e-3;
  var _HypergraphLayout = class _HypergraphLayout extends import_g63.BaseLayout {
    constructor() {
      super(...arguments);
      this.id = "hypergraph";
      this.resolvedOptions = { type: "hypergraph" };
      /**
       * <zh/> 执行若干次迭代，未指定次数时迭代至收敛
       *
       * <en/> Run several iterations, until convergence when no count is given
       * @param iterations - <zh/> 迭代次数 | <en/> iterations
       * @returns <zh/> 当前布局结果 | <en/> current layout result
       */
      this.tick = (iterations) => {
        const sim = this.simulation;
        if (!sim) return { nodes: [] };
        const limit = iterations ?? Infinity;
        for (let i = 0; i < limit && sim.alpha >= ALPHA_MIN; i++) step(sim, this.resolvedOptions);
        if (sim.alpha < ALPHA_MIN) settle(sim);
        return this.output();
      };
      this.stop = () => {
        if (this.timer !== void 0) clearTimeout(this.timer);
        this.timer = void 0;
      };
    }
    async execute(model, options) {
      this.stop();
      const opts = Object.assign({}, _HypergraphLayout.defaultOptions, this.options, options);
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
          for (let i = 0; i < ticksPerFrame && sim.alpha >= ALPHA_MIN; i++) step(sim, this.resolvedOptions);
          if (sim.alpha < ALPHA_MIN) settle(sim);
          const data = this.output();
          onTick(data);
          if (sim.alpha < ALPHA_MIN) {
            this.timer = void 0;
            resolve(data);
          } else this.timer = setTimeout(frame, 16);
        };
        this.timer = setTimeout(frame, 0);
      });
    }
    output() {
      const sim = this.simulation;
      if (!sim) return { nodes: [] };
      return { nodes: sim.ids.map((id, i) => ({ id, style: { x: sim.x[i], y: sim.y[i] } })) };
    }
  };
  _HypergraphLayout.defaultOptions = {
    nodeSize: 20,
    nodeSpacing: 10,
    preventLabelOverlap: false,
    labelFontSize: 12,
    labelPlacement: "bottom",
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
    seed: 1
  };
  var HypergraphLayout = _HypergraphLayout;
  function createRandom(seed) {
    let a = seed >>> 0;
    return () => {
      a = a + 1831565813 >>> 0;
      let t = a;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function resolveHyperedges(model, options) {
    const { hyperedges = [] } = options;
    const edges = (model.edges || []).map((edge) => ({ id: edge.id, members: [edge.source, edge.target] }));
    return [...typeof hyperedges === "function" ? hyperedges(model) : hyperedges, ...edges];
  }
  function orderByOverlap(sets, shared) {
    const rest = new Set(sets.map((_, i) => i));
    const order = [];
    const largest = () => [...rest].reduce((a, b) => sets[b].length > sets[a].length ? b : a);
    let current = rest.size ? largest() : -1;
    while (current !== -1) {
      order.push(current);
      rest.delete(current);
      if (!rest.size) break;
      let next = -1;
      let best = 0;
      rest.forEach((candidate) => {
        const score = shared(current, candidate) / Math.min(sets[current].length, sets[candidate].length);
        if (score > best || score === best && next !== -1 && sets[candidate].length > sets[next].length) {
          best = score;
          next = candidate;
        }
      });
      current = best > 0 ? next : largest();
    }
    return order;
  }
  function initSimulation(model, options) {
    const {
      nodeSize = 20,
      nodeSpacing = 10,
      radiusFactor = 0.6,
      centerNode,
      center,
      width = 0,
      height = 0,
      iterations = 300,
      seed = 1,
      preventLabelOverlap = false
    } = options;
    const random = createRandom(seed);
    const nodes = model.nodes || [];
    const n = nodes.length;
    const ids = nodes.map((node) => node.id);
    const indexOf = new Map(ids.map((id, i) => [id, i]));
    const sizeOf = typeof nodeSize === "function" ? nodeSize : () => nodeSize;
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
    const memberSets = [];
    const seen = /* @__PURE__ */ new Set();
    resolveHyperedges(model, options).forEach(({ members }) => {
      const indices = [...new Set(members.map((id) => indexOf.get(id)).filter((i) => i !== void 0))];
      if (indices.length < 2) return;
      indices.sort((a, b) => a - b);
      const key = indices.join(",");
      if (seen.has(key)) return;
      seen.add(key);
      memberSets.push(Int32Array.from(indices));
    });
    const hubSets = memberSets.filter((set) => set.length > 2);
    const pairSets = memberSets.filter((set) => set.length === 2);
    const degree = new Float64Array(n);
    const hubsOf = Array.from({ length: n }, () => []);
    hubSets.forEach((set, h) => set.forEach((v) => (degree[v]++, hubsOf[v].push(h))));
    pairSets.forEach(([u, v]) => (degree[u]++, degree[v]++));
    const hubCount = hubSets.length;
    const sharedCount = /* @__PURE__ */ new Map();
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
    const hubParents = hubSets.map(
      (set, a) => hubSets.map((_, b) => b).filter((b) => b !== a && shared(a, b) === set.length)
    );
    const pairParents = pairSets.map(([u, v]) => hubsOf[u].filter((h) => hubsOf[v].includes(h)));
    const hubs = hubSets.map((members) => {
      const radius2 = radiusFactor * spacing * Math.sqrt(members.length);
      return { members, radius: radius2, rest: radius2 * 0.65, x: cx, y: cy, vx: 0, vy: 0 };
    });
    const x = new Float64Array(n);
    const y = new Float64Array(n);
    const placed = new Uint8Array(n);
    const fixed = centerNode !== void 0 ? indexOf.get(centerNode) ?? -1 : -1;
    const order = orderByOverlap(hubSets, shared);
    if (fixed !== -1) {
      x[fixed] = cx;
      y[fixed] = cy;
      placed[fixed] = 1;
      const leaves = pairSets.filter((set) => set[0] === fixed || set[1] === fixed).map(([u, v]) => u === fixed ? v : u);
      const slots = [
        ...order.map((h) => ({ hub: h, leaf: -1, width: 2 * hubs[h].radius })),
        ...leaves.map((leaf) => ({ hub: -1, leaf, width: spacing }))
      ];
      const total = slots.reduce((sum, slot) => sum + slot.width, 0) || 1;
      let angle = 0;
      slots.forEach((slot) => {
        const theta = (angle + slot.width / 2) / total * Math.PI * 2;
        angle += slot.width;
        if (slot.hub !== -1) {
          const hub = hubs[slot.hub];
          const distance = Math.max(hub.rest, total / (Math.PI * 2) * 0.5);
          hub.x = cx + Math.cos(theta) * distance;
          hub.y = cy + Math.sin(theta) * distance;
        } else if (!hubsOf[slot.leaf].length) {
          const distance = Math.max(spacing * 1.5, total / (Math.PI * 2));
          x[slot.leaf] = cx + Math.cos(theta) * distance;
          y[slot.leaf] = cy + Math.sin(theta) * distance;
          placed[slot.leaf] = 1;
        }
      });
    } else {
      const gap = spacing * 3 / (Math.PI * 2);
      let theta = 0;
      order.forEach((h, i) => {
        const hub = hubs[h];
        if (i > 0) theta += 2 * hub.radius / Math.max(gap * theta, hub.radius);
        hub.x = cx + gap * theta * Math.cos(theta);
        hub.y = cy + gap * theta * Math.sin(theta);
      });
    }
    for (let v = 0; v < n; v++) {
      if (placed[v] || !hubsOf[v].length) continue;
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
    const neighbors = Array.from({ length: n }, () => []);
    pairSets.forEach(([u, v]) => (neighbors[u].push(v), neighbors[v].push(u)));
    const queue = [];
    for (let v = 0; v < n; v++) if (placed[v]) queue.push(v);
    const spread = spacing * Math.sqrt(n);
    for (let v = 0; v < n || queue.length; ) {
      if (!queue.length) {
        while (v < n && placed[v]) v++;
        if (v >= n) break;
        const angle = random() * Math.PI * 2;
        const distance = Math.sqrt(random()) * spread;
        x[v] = cx + Math.cos(angle) * distance;
        y[v] = cy + Math.sin(angle) * distance;
        placed[v] = 1;
        queue.push(v);
      }
      const u = queue.shift();
      neighbors[u].forEach((w) => {
        if (placed[w]) return;
        const angle = random() * Math.PI * 2;
        x[w] = x[u] + Math.cos(angle) * spacing * 1.5;
        y[w] = y[u] + Math.sin(angle) * spacing * 1.5;
        placed[w] = 1;
        queue.push(w);
      });
    }
    const pairs = new Int32Array(pairSets.length * 2);
    pairSets.forEach(([u, v], i) => (pairs[i * 2] = u, pairs[i * 2 + 1] = v));
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
      alphaDecay: 1 - Math.pow(ALPHA_MIN, 1 / Math.max(1, iterations))
    };
  }
  var Grid = class {
    constructor(x, y, size) {
      this.x = x;
      this.y = y;
      this.size = size;
      this.cells = /* @__PURE__ */ new Map();
      for (let i = 0; i < x.length; i++) {
        const key = this.key(Math.floor(x[i] / size), Math.floor(y[i] / size));
        const cell = this.cells.get(key);
        if (cell) cell.push(i);
        else this.cells.set(key, [i]);
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
      const { size } = this;
      for (let i = Math.floor(x0 / size); i <= Math.floor(x1 / size); i++) {
        for (let j = Math.floor(y0 / size); j <= Math.floor(y1 / size); j++) {
          this.cells.get(this.key(i, j))?.forEach(visit);
        }
      }
    }
  };
  function step(sim, options) {
    const {
      attraction = 1,
      repulsion = 1,
      exclusion = 1,
      hyperedgeRepulsion = 1,
      gravity = 0.05,
      velocityDecay = 0.4
    } = options;
    const { x, y, vx, vy, degree, hubs, pairs, hubWeights, hubsOf, hubParents, pairParents, spacing, cx, cy, fixed } = sim;
    const sharesParent = (v, parents) => parents.some((p) => hubsOf[v].includes(p));
    const n = x.length;
    const alpha = sim.alpha;
    const pairRest = spacing * 1.5;
    hubs.forEach((hub) => {
      const size = hub.members.length;
      hub.members.forEach((v) => {
        let dx = hub.x + hub.vx - x[v] - vx[v];
        let dy = hub.y + hub.vy - y[v] - vy[v];
        const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
        const l = (d - hub.rest) / d * alpha * (attraction / Math.min(degree[v], size));
        const bias = size / (size + degree[v]);
        dx *= l;
        dy *= l;
        vx[v] += dx * bias;
        vy[v] += dy * bias;
        hub.vx -= dx * (1 - bias);
        hub.vy -= dy * (1 - bias);
      });
    });
    for (let i = 0; i < pairs.length; i += 2) {
      const u = pairs[i];
      const v = pairs[i + 1];
      let dx = x[v] + vx[v] - x[u] - vx[u];
      let dy = y[v] + vy[v] - y[u] - vy[u];
      const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
      const l = (d - pairRest) / d * alpha * (attraction / Math.min(degree[u], degree[v]));
      const bias = degree[u] / (degree[u] + degree[v]);
      dx *= l;
      dy *= l;
      vx[v] -= dx * bias;
      vy[v] -= dy * bias;
      vx[u] += dx * (1 - bias);
      vy[u] += dy * (1 - bias);
    }
    const range = spacing * 4;
    const grid = new Grid(x, y, range);
    const charge = repulsion * spacing * spacing * 0.5;
    for (let i = 0; i < n; i++) {
      grid.query(x[i] - range, y[i] - range, x[i] + range, y[i] + range, (j) => {
        if (j <= i) return;
        let dx = x[j] - x[i];
        let dy = y[j] - y[i];
        let d2 = dx * dx + dy * dy;
        if (d2 > range * range) return;
        if (d2 < 1e-6) {
          dx = (i - j) * 1e-3;
          dy = 1e-3;
          d2 = dx * dx + dy * dy;
        }
        const d = Math.sqrt(d2);
        let f = charge * alpha / d2;
        if (d < spacing) f += (spacing - d) * 0.35;
        const fx = dx / d * f;
        const fy = dy / d * f;
        vx[i] -= fx;
        vy[i] -= fy;
        vx[j] += fx;
        vy[j] += fy;
      });
    }
    const labelWeight = (1 - alpha) * (1 - alpha);
    if (sim.labels && labelWeight > 0) {
      forEachBoxOverlap(sim, grid, (i, j, ox, oy) => {
        vx[i] -= ox * labelWeight;
        vy[i] -= oy * labelWeight;
        vx[j] += ox * labelWeight;
        vy[j] += oy * labelWeight;
      });
    }
    const mark = new Int32Array(n);
    const margin = spacing * 0.75;
    hubs.forEach((hub, h) => {
      let extent = 0;
      hub.members.forEach((v) => {
        mark[v] = h + 1;
        extent = Math.max(extent, Math.abs(x[v] - hub.x), Math.abs(y[v] - hub.y));
      });
      if (extent > hub.radius * 2.5) return;
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
        if (mark[v] === h + 1 || sharesParent(v, hubParents[h])) return;
        const [distance, nx, ny] = signedDistance(polygon, x[v], y[v]);
        if (distance >= margin) return;
        const f = (margin - distance) * exclusion * Math.max(alpha, 0.1) * 0.5;
        vx[v] += nx * f * 0.8;
        vy[v] += ny * f * 0.8;
        hub.vx -= nx * f * 0.2;
        hub.vy -= ny * f * 0.2;
      });
    });
    for (let i = 0; i < pairs.length; i += 2) {
      const u = pairs[i];
      const v = pairs[i + 1];
      const ex = x[v] - x[u];
      const ey = y[v] - y[u];
      const len2 = ex * ex + ey * ey;
      if (len2 < 1e-6 || len2 > pairRest * pairRest * 9) continue;
      grid.query(
        Math.min(x[u], x[v]) - margin,
        Math.min(y[u], y[v]) - margin,
        Math.max(x[u], x[v]) + margin,
        Math.max(y[u], y[v]) + margin,
        (w) => {
          if (w === u || w === v || sharesParent(w, pairParents[i / 2])) return;
          const t = ((x[w] - x[u]) * ex + (y[w] - y[u]) * ey) / len2;
          if (t <= 0.05 || t >= 0.95) return;
          const dx = x[w] - (x[u] + ex * t);
          const dy = y[w] - (y[u] + ey * t);
          const d = Math.sqrt(dx * dx + dy * dy) || 1e-6;
          if (d >= margin) return;
          const f = (margin - d) / d * exclusion * Math.max(alpha, 0.1) * 0.5;
          vx[w] += dx * f;
          vy[w] += dy * f;
        }
      );
    }
    const hubCount = hubs.length;
    for (let a = 0; a < hubCount; a++) {
      for (let b = a + 1; b < hubCount; b++) {
        const weight = hubWeights[a * hubCount + b] * hyperedgeRepulsion;
        if (weight <= 0) continue;
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
        let f = weight * reach * reach * 0.5 * alpha / d2;
        if (d < reach) f += (reach - d) * weight * 0.1 * alpha;
        const fx = dx / d * f;
        const fy = dy / d * f;
        A.vx -= fx;
        A.vy -= fy;
        B.vx += fx;
        B.vy += fy;
      }
    }
    const g = gravity * alpha;
    for (let i = 0; i < n; i++) {
      vx[i] += (cx - x[i]) * g;
      vy[i] += (cy - y[i]) * g;
    }
    hubs.forEach((hub) => {
      hub.vx += (cx - hub.x) * g;
      hub.vy += (cy - hub.y) * g;
    });
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
  function charWidth(char) {
    const code = char.charCodeAt(0);
    if (code >= 11904) return 1;
    if (code >= 65 && code <= 90) return 0.72;
    return 0.6;
  }
  function measureLabels(nodes, radius, options) {
    const {
      labelText,
      labelFontSize = 12,
      labelMaxWidth = Infinity,
      labelPlacement = "bottom",
      labelPadding = 4
    } = options;
    const textOf = labelText || ((node) => String(node.style?.labelText ?? node.id));
    const boxes = new Float64Array(nodes.length * 4);
    nodes.forEach((node, i) => {
      let width = 0;
      let lines = 0;
      textOf(node).split("\n").forEach((line) => {
        let w = 0;
        for (const char of line) w += labelFontSize * charWidth(char);
        lines += Math.max(1, Math.ceil(w / labelMaxWidth));
        width = Math.max(width, Math.min(w, labelMaxWidth));
      });
      const hw = width / 2 + labelPadding / 2;
      const hh = lines * labelFontSize * 1.3 / 2 + labelPadding / 2;
      const r = radius[i];
      const [dx, dy] = {
        bottom: [0, r + hh],
        top: [0, -r - hh],
        left: [-r - hw, 0],
        right: [r + hw, 0],
        center: [0, 0]
      }[labelPlacement];
      boxes.set([dx, dy, hw, hh], i * 4);
    });
    return boxes;
  }
  function forEachBoxOverlap(sim, grid, visit) {
    const { x, y, radius, reach } = sim;
    const labels = sim.labels;
    const n = x.length;
    const box = (i, label) => label ? [x[i] + labels[i * 4], y[i] + labels[i * 4 + 1], labels[i * 4 + 2], labels[i * 4 + 3]] : [x[i], y[i], radius[i], radius[i]];
    for (let i = 0; i < n; i++) {
      grid.query(x[i] - reach * 2, y[i] - reach * 2, x[i] + reach * 2, y[i] + reach * 2, (j) => {
        if (j <= i) return;
        const sx = x[j] > x[i] || x[j] === x[i] && i < j ? 1 : -1;
        const sy = y[j] > y[i] || y[j] === y[i] && i < j ? 1 : -1;
        let needX = 0;
        let needY = 0;
        const test = (a, b) => {
          const dx = b[0] - a[0];
          const dy = b[1] - a[1];
          if (a[2] + b[2] <= Math.abs(dx) || a[3] + b[3] <= Math.abs(dy)) return;
          needX = Math.max(needX, a[2] + b[2] - sx * dx);
          needY = Math.max(needY, a[3] + b[3] - sy * dy);
        };
        const li = box(i, true);
        const lj = box(j, true);
        test(li, lj);
        test(li, box(j, false));
        test(box(i, false), lj);
        if (!needX && !needY) return;
        if (needX < needY) visit(i, j, sx * needX, 0);
        else visit(i, j, 0, sy * needY);
      });
    }
  }
  function settle(sim) {
    if (sim.settled) return;
    sim.settled = true;
    if (!sim.labels) return;
    const { x, y, fixed } = sim;
    for (let pass = 0; pass < 300; pass++) {
      let moved = false;
      forEachBoxOverlap(sim, new Grid(x, y, sim.reach * 2), (i, j, ox, oy) => {
        moved = true;
        const sx = ox && ox + Math.sign(ox);
        const sy = oy && oy + Math.sign(oy);
        const wi = i === fixed ? 0 : j === fixed ? 1 : 0.5;
        x[i] -= sx * wi;
        y[i] -= sy * wi;
        x[j] += sx * (1 - wi);
        y[j] += sy * (1 - wi);
      });
      if (!moved) break;
    }
  }
  function convexHull(indices, x, y) {
    const points = Array.from(indices).sort((a, b) => x[a] - x[b] || y[a] - y[b]);
    const cross = (o, a, b) => (x[a] - x[o]) * (y[b] - y[o]) - (y[a] - y[o]) * (x[b] - x[o]);
    const chain = (list) => {
      const result = [];
      list.forEach((p) => {
        while (result.length >= 2 && cross(result[result.length - 2], result[result.length - 1], p) <= 0) result.pop();
        result.push(p);
      });
      result.pop();
      return result;
    };
    const hull = [...chain(points), ...chain(points.reverse())];
    return hull.flatMap((i) => [x[i], y[i]]);
  }
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
      if (ex * (py - ay) - ey * (px - ax) < 0) inside = false;
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
    } else {
      nx = 1;
      ny = 0;
    }
    return [inside ? -best : best, nx, ny];
  }

  // src/register.ts
  var import_g64 = __toESM(require_g6(), 1);
  var HYPERGRAPH_LAYOUT = "hypergraph";
  var registered = false;
  var bubbleSetsOverridden = false;
  var registerHypergraph = ({ overrideBubbleSets = false } = {}) => {
    if (!registered) {
      registered = true;
      (0, import_g64.register)(import_g64.ExtensionCategory.LAYOUT, HYPERGRAPH_LAYOUT, HypergraphLayout);
      (0, import_g64.register)(import_g64.ExtensionCategory.PLUGIN, HOVER_BUBBLE_SETS, HoverBubbleSets);
    }
    if (overrideBubbleSets && !bubbleSetsOverridden) {
      bubbleSetsOverridden = true;
      (0, import_g64.register)(import_g64.ExtensionCategory.PLUGIN, "bubble-sets", KeyBoundsBubbleSets);
    }
  };

  // src/theme.ts
  var DEFAULT_THEME = {
    hyperedgeColors: [
      "#F6BD16",
      "#00C9C9",
      "#F08F56",
      "#D580FF",
      "#FF3D00",
      "#16f69c",
      "#004ac9",
      "#f056d1",
      "#a680ff",
      "#c8ff00"
    ],
    typePalette: ["#00C9C9", "#a68fff", "#F08F56", "#0d7c4f", "#004ac9", "#f056d1"],
    nodeColor: "#8b5cf6",
    centerColor: "#6d28d9",
    highlightColor: "#6d28d9",
    edgeColor: "#a68fff",
    nodeSize: 20,
    largeNodeSize: 15,
    largeGraphThreshold: 100,
    labelFontSize: 12,
    bubble: {
      normal: { fillOpacity: 0.2, strokeOpacity: 0.2, lineWidth: 1 },
      highlight: { fillOpacity: 0.45, strokeOpacity: 1, lineWidth: 3 },
      dimmed: { fillOpacity: 0.03, strokeOpacity: 0.05, lineWidth: 1 }
    },
    bubbleOptions: {
      maxRoutingIterations: 100,
      maxMarchingIterations: 20,
      pixelGroup: 4,
      edgeR0: 30,
      edgeR1: 50,
      nodeR0: 1,
      nodeR1: 5,
      morphBuffer: 10,
      threshold: 4,
      memberInfluenceFactor: 1,
      edgeInfluenceFactor: 4,
      nonMemberInfluenceFactor: -0.8,
      virtualEdges: true
    },
    inactiveNodeOpacity: 0.15,
    inactiveEdgeOpacity: 0.1
  };
  var resolveTheme = (theme) => ({
    ...DEFAULT_THEME,
    ...theme,
    bubble: { ...DEFAULT_THEME.bubble, ...theme?.bubble },
    bubbleOptions: { ...DEFAULT_THEME.bubbleOptions, ...theme?.bubbleOptions }
  });
  var typeColorsOf = (vertices, typeField = "entity_type", palette = DEFAULT_THEME.typePalette) => {
    const colors = {};
    let i = 0;
    for (const v of vertices) {
      const type = v?.[typeField];
      if (!type || type in colors) continue;
      colors[type] = palette[i++ % palette.length];
    }
    return colors;
  };

  // src/spec.ts
  var PAIR_SEP = "|#|";
  var pairId = (a, b) => a < b ? `${a}${PAIR_SEP}${b}` : `${b}${PAIR_SEP}${a}`;
  var bubbleKeyOf = (id) => `bubble-sets-${id}`;
  var toG6Spec = (graph, options = {}) => {
    const {
      mode = "hyper",
      centerNode,
      typeField = "entity_type",
      graphEdges = "binary",
      labelText = (d) => String(d.id)
    } = options;
    const theme = resolveTheme(options.theme);
    const isGraph = mode === "graph";
    let nodes = Object.entries(graph.vertices).map(([id, value]) => ({ ...value, id, label: id }));
    const edges = [];
    const lineIds = /* @__PURE__ */ new Set();
    const pushLine = (a, b, attrs) => {
      const id = pairId(a, b);
      if (lineIds.has(id)) return;
      lineIds.add(id);
      edges.push({ ...attrs, id, source: a, target: b });
    };
    const hyperedges = /* @__PURE__ */ new Map();
    const layoutHyperedges = [];
    const plugins = [];
    graph.hyperedges.forEach((he, i) => {
      const members = [...new Set(he.members)];
      if (members.length < 2) return;
      const id = he.id ?? (members.length === 2 ? pairId(members[0], members[1]) : members.join(PAIR_SEP));
      const item = { ...he, id, members };
      hyperedges.set(id, item);
      const { members: _, id: __, ...attrs } = he;
      if (members.length === 2) {
        pushLine(members[0], members[1], attrs);
        return;
      }
      if (isGraph) {
        if (graphEdges === "clique") {
          for (let a = 0; a < members.length; a++) {
            for (let b = a + 1; b < members.length; b++) pushLine(members[a], members[b], attrs);
          }
        }
        return;
      }
      const color = theme.hyperedgeColors[i % theme.hyperedgeColors.length];
      plugins.push({
        key: bubbleKeyOf(id),
        type: HOVER_BUBBLE_SETS,
        members,
        // 只圈节点，不包裹标签
        memberBoundsType: "key",
        hyperedge: item,
        fill: color,
        stroke: color,
        ...theme.bubbleOptions,
        ...theme.bubble.normal
      });
      layoutHyperedges.push({ id, weight: he.weight || members.length, members });
    });
    if (isGraph && graphEdges === "binary") {
      const connected = /* @__PURE__ */ new Set();
      edges.forEach((e) => {
        connected.add(e.source);
        connected.add(e.target);
      });
      nodes = nodes.filter((n) => connected.has(n.id));
    } else if (!isGraph) {
      const clusterOf = /* @__PURE__ */ new Map();
      layoutHyperedges.forEach((he) => {
        he.members.forEach((m) => {
          const cur = clusterOf.get(m);
          if (!cur || he.weight > cur.weight) clusterOf.set(m, { id: he.id, weight: he.weight });
        });
      });
      nodes = nodes.map((n) => {
        const c = clusterOf.get(n.id);
        return c ? { ...n, cluster: c.id } : n;
      });
    }
    const typeColors = options.typeColors ?? typeColorsOf(nodes, typeField, theme.typePalette);
    const large = nodes.length > theme.largeGraphThreshold;
    const hasCenter = centerNode !== void 0 && nodes.some((n) => n.id === centerNode);
    return {
      data: { nodes, edges },
      hyperedges,
      plugins: isGraph ? [] : plugins,
      node: {
        palette: { field: "cluster" },
        style: {
          size: large ? theme.largeNodeSize : theme.nodeSize,
          labelText,
          fill: (d) => hasCenter && d.id === centerNode ? theme.centerColor : typeColors[d[typeField]] || theme.nodeColor,
          // 显式写出被状态覆盖的样式：G6 移除状态时只回到这里的值，不写就会保留状态样式
          opacity: 1,
          lineWidth: 0,
          labelFontWeight: "normal"
        },
        // 点击超边高亮：成员实体 highlight，其余 inactive
        state: {
          highlight: { stroke: theme.highlightColor, lineWidth: 3, labelFontWeight: "bold" },
          inactive: { opacity: theme.inactiveNodeOpacity }
        }
      },
      edge: {
        style: { size: isGraph ? 3 : 2, stroke: theme.edgeColor, lineWidth: 1, opacity: 1 },
        state: {
          highlight: { stroke: theme.highlightColor, lineWidth: 3 },
          inactive: { opacity: theme.inactiveEdgeOpacity }
        }
      },
      // 超图模式：超图布局，连线也作为 2 元超边参与，以中心实体为中心呈花瓣状排布；
      // 图模式：力导布局
      layout: !isGraph ? {
        type: HYPERGRAPH_LAYOUT,
        hyperedges: layoutHyperedges,
        centerNode: hasCenter ? centerNode : void 0,
        nodeSpacing: 50,
        // 标签互不重叠：与节点样式的 labelText、字号保持一致
        preventLabelOverlap: true,
        labelText,
        labelFontSize: theme.labelFontSize
      } : { type: "force", preventOverlap: true, gravity: 50, linkDistance: 50 }
    };
  };

  // src/view.ts
  var import_g65 = __toESM(require_g6(), 1);
  var destroyGraph = (graph) => {
    if (graph.destroyed) return;
    try {
      graph.destroy();
    } catch {
      graph.context.canvas?.destroy();
      graph.destroyed = true;
    }
  };
  var createHypergraphView = (container, initial = {}) => {
    registerHypergraph();
    let options = { ...initial };
    let spec = null;
    let selected = null;
    const host = document.createElement("div");
    host.style.cssText = "position: absolute; inset: 0; overflow: hidden;";
    if (getComputedStyle(container).position === "static") container.style.position = "relative";
    container.appendChild(host);
    const graph = new import_g65.Graph({
      container: host,
      width: container.offsetWidth,
      height: container.offsetHeight || options.fallbackHeight || 300,
      behaviors: options.behaviors ?? ["zoom-canvas", "drag-canvas", "drag-element"],
      autoFit: options.autoFit ?? "center",
      animation: false
    });
    const hitOf = (e) => {
      if (!spec) return null;
      if (e.targetType === "node") {
        const node = spec.data.nodes.find((n) => n.id === e.target.id);
        return node ? { kind: "node", id: node.id, item: node } : null;
      }
      if (e.targetType === "edge") {
        const edge = spec.data.edges.find((d) => d.id === e.target.id);
        if (!edge) return null;
        const { source, target, ...rest } = edge;
        const members = [source, target];
        return { kind: "edge", id: edge.id, members, item: { ...rest, id: edge.id, members } };
      }
      if (e.targetType === BUBBLE_SETS_TARGET) {
        const item = e.target.options?.hyperedge;
        return item ? { kind: "hyperedge", id: item.id, members: item.members, item } : null;
      }
      return null;
    };
    const applySelection = () => {
      if (!spec) return;
      const { bubble } = resolveTheme(options.theme);
      const members = new Set(selected?.members);
      const states = {};
      spec.data.nodes.forEach((n) => {
        states[n.id] = !selected ? [] : members.has(n.id) ? ["highlight"] : ["inactive"];
      });
      spec.data.edges.forEach((d) => {
        states[d.id] = !selected ? [] : selected.kind === "edge" && d.id === selected.id ? ["highlight"] : ["inactive"];
      });
      graph.setElementState(states, false);
      graph.setPlugins(
        (plugins) => plugins.map(
          (p) => p.type !== HOVER_BUBBLE_SETS ? p : {
            ...p,
            ...!selected ? bubble.normal : selected.kind === "hyperedge" && p.hyperedge?.id === selected.id ? bubble.highlight : bubble.dimmed
          }
        )
      );
    };
    const setSelected = (next) => {
      selected = next;
      applySelection();
      options.onSelect?.(selected);
    };
    graph.on("click", (e) => {
      if (e.targetType === "node") return;
      const hit = hitOf(e);
      const next = hit && hit.kind !== "node" && hit.id !== selected?.id ? hit : null;
      if (next || selected) setSelected(next);
    });
    graph.on("pointermove", (e) => {
      if (!options.onHover) return;
      const hit = e.client ? hitOf(e) : null;
      options.onHover(hit ? { ...hit, client: { x: e.client.x, y: e.client.y } } : null);
    });
    const onLeave = () => options.onHover?.(null);
    container.addEventListener("pointerleave", onLeave);
    const observer = new ResizeObserver(() => {
      if (!graph.destroyed && container.offsetWidth && container.offsetHeight) {
        graph.setSize(container.offsetWidth, container.offsetHeight);
      }
    });
    observer.observe(container);
    const render = () => {
      if (graph.destroyed || !options.data) return;
      if (selected) {
        selected = null;
        applySelection();
      }
      spec = toG6Spec(options.data, options);
      if (graph.context.layout) graph.stopLayout();
      graph.setOptions({
        data: spec.data,
        node: spec.node,
        edge: spec.edge,
        layout: spec.layout,
        plugins: spec.plugins
      });
      scheduleRender();
    };
    let renderPending = false;
    const scheduleRender = () => {
      if (renderPending) return;
      renderPending = true;
      queueMicrotask(() => {
        renderPending = false;
        if (!graph.destroyed) graph.render().catch(() => void 0);
      });
    };
    render();
    return {
      graph,
      update(next) {
        options = { ...options, ...next };
        const hadSelection = !!selected;
        render();
        if (hadSelection) options.onSelect?.(null);
      },
      select(id) {
        if (id === null) return setSelected(null);
        const he = spec?.hyperedges.get(id);
        if (!he) return;
        const [a, b] = he.members;
        setSelected(
          he.members.length === 2 ? { kind: "edge", id: pairId(a, b), members: he.members, item: he } : { kind: "hyperedge", id: he.id, members: he.members, item: he }
        );
      },
      destroy() {
        observer.disconnect();
        container.removeEventListener("pointerleave", onLeave);
        spec = null;
        destroyGraph(graph);
        host.remove();
      }
    };
  };
  return __toCommonJS(src_exports);
})();
