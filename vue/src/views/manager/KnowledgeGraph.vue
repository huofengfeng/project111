<template>
  <div class="kg-container">
    <!-- 顶部工具栏 -->
    <div class="kg-toolbar">
      <div class="kg-title">
        <span class="kg-title-icon">
          <el-icon><Connection /></el-icon>
        </span>
        <span>文物知识图谱</span>
      </div>
      <div class="kg-actions">
        <el-select v-model="artifactLimit" size="small" style="width:110px" @change="onLimitChange">
          <el-option label="10 件文物" :value="10" />
          <el-option label="20 件文物" :value="20" />
          <el-option label="30 件文物" :value="30" />
          <el-option label="50 件文物" :value="50" />
          <el-option label="全部文物" :value="0" />
        </el-select>
        <el-button v-if="isFocusedView" size="small" type="primary" @click="exitFocusedView">
          <el-icon><DArrowLeft /></el-icon>
          <span>返回全图</span>
        </el-button>
        <el-button size="small" @click="fetchData" :loading="loading">
          <el-icon><Refresh /></el-icon>
          <span>刷新</span>
        </el-button>
        <el-button size="small" @click="resetLayout">
          <el-icon><Aim /></el-icon>
          <span>重置</span>
        </el-button>
      </div>
    </div>

    <!-- 搜索 + 统计 + 图例 -->
    <div class="kg-info-row">
      <div class="kg-search">
        <el-input
          v-model="searchText"
          placeholder="搜索节点…"
          size="small"
          clearable
          @input="onSearchInput"
          @clear="clearSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div class="search-results" v-if="searchResults.length > 0 && searchText">
          <div
            v-for="r in searchResults"
            :key="r.id"
            class="search-item"
            @click="focusNode(r.id)"
          >
            <span class="search-dot" :style="{ background: r.color }"></span>
            <span class="search-name">{{ r.label }}</span>
            <span class="search-cat">{{ r.categoryLabel }}</span>
          </div>
        </div>
      </div>

      <div class="kg-stats">
        <div class="stat-item">
          <span class="stat-num">{{ stats.totalNodes }}</span>
          <span class="stat-label">实体</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-num">{{ stats.totalEdges }}</span>
          <span class="stat-label">关系</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-num">{{ stats.totalCategories }}</span>
          <span class="stat-label">类别</span>
        </div>
      </div>

      <div class="kg-legend">
        <span
          v-for="cat in categories"
          :key="cat.id"
          class="legend-item"
          :class="{ active: activeCategories.has(cat.id) }"
          @click="toggleCategory(cat.id)"
        >
          <span class="legend-dot" :style="{ background: cat.color }"></span>
          <span class="legend-text">{{ cat.label }}</span>
        </span>
      </div>
    </div>

    <!-- 图谱画布 -->
    <div class="kg-chart-wrap">
      <div ref="chartContainer" class="kg-chart"></div>

      <div v-if="!loading && stats.totalNodes === 0" class="kg-empty">
        <el-empty description="暂无数据，请先在数据库中添加文物记录" />
      </div>

      <div v-if="loading" class="kg-loading">
        <el-icon class="kg-spin"><Loading /></el-icon>
        <span>正在加载图谱数据…</span>
      </div>

      <!-- 节点详情浮层 -->
      <Transition name="panel">
        <div class="node-detail-panel" v-if="detailNode">
          <div class="detail-head">
            <span class="detail-badge" :style="{ background: detailNode.color }">
              {{ detailNode.categoryLabel }}
            </span>
            <button class="detail-close" @click="clearHighlight">&times;</button>
          </div>
          <h3 class="detail-name">{{ detailNode.label }}</h3>
          <div class="detail-rel-section" v-if="detailRelations.length">
            <div class="detail-rel-title">关联关系</div>
            <div
              v-for="(rel, i) in detailRelations"
              :key="i"
              class="detail-rel-item"
              @click="focusNode(rel.targetId)"
            >
              <span class="rel-label">{{ rel.label }}</span>
              <span class="rel-arrow">→</span>
              <span class="rel-target">{{ rel.targetLabel }}</span>
            </div>
          </div>
          <div v-else class="detail-no-rel">暂无关联数据</div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { Graph } from '@antv/g6'
import { Connection, Refresh, Aim, Loading, Search, DArrowLeft } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'

// ==================== 状态 ====================
const chartContainer = ref(null)
let graph = null
let rawData = { nodes: [], edges: [], categories: [] }
let resizeObserver = null

const loading = ref(false)
const nodes = ref([])
const edges = ref([])
const categories = ref([])
const activeCategories = ref(new Set(['artifact']))
const isFocusedView = ref(false)
const artifactLimit = ref(20)
const searchText = ref('')
const searchResults = ref([])
const detailNode = ref(null)
const detailRelations = ref([])
const focusedNodeId = ref(null)

const CATEGORY_LABELS = {
  artifact: '文物', dynasty: '朝代', museum: '博物馆',
  glaze: '釉色', type: '器型', tomb: '墓葬', site: '出土地',
}

const stats = computed(() => ({
  totalNodes: nodes.value.length,
  totalEdges: edges.value.length,
  totalCategories: categories.value.length,
}))

// ==================== 数据加载 ====================
async function fetchData() {
  loading.value = true
  detailNode.value = null
  try {
    const params = {}
    if (artifactLimit.value > 0) params.limit = artifactLimit.value
    const res = await request.get('/knowledge-graph/data', { params })
    if (res.code === '200' || res.code === 200) {
      rawData = res.data || { nodes: [], edges: [], categories: [] }
      nodes.value = rawData.nodes || []
      edges.value = rawData.edges || []
      categories.value = rawData.categories || []
      if (categories.value.length === 0) {
        ElMessage.warning('图谱数据为空，请先在数据库中添加文物记录')
      }
      activeCategories.value = new Set(['artifact'])
      focusedNodeId.value = null
      isFocusedView.value = false
      await nextTick()
      await renderGraph()
    } else {
      ElMessage.error(res.msg || `请求失败`)
    }
  } catch (e) {
    const msg = e.response?.data?.msg || e.response?.statusText || e.message || String(e)
    ElMessage.error('加载图谱数据失败：' + msg)
  } finally {
    loading.value = false
  }
}

function onLimitChange() { fetchData() }

// ==================== G6 图谱渲染 ====================
async function renderGraph() {
  if (!chartContainer.value) return
  if (graph) { graph.destroy(); graph = null }

  const { clientWidth, clientHeight } = chartContainer.value
  if (clientWidth === 0 || clientHeight === 0) return

  // 筛选可见节点
  let visibleNodes, visibleEdges
  if (isFocusedView.value && focusedNodeId.value) {
    const neighborIds = new Set([focusedNodeId.value])
    rawData.edges.forEach(e => {
      if (e.source === focusedNodeId.value) neighborIds.add(e.target)
      if (e.target === focusedNodeId.value) neighborIds.add(e.source)
    })
    visibleNodes = rawData.nodes.filter(n => neighborIds.has(n.id))
    const ids = new Set(visibleNodes.map(n => n.id))
    visibleEdges = rawData.edges.filter(e => ids.has(e.source) && ids.has(e.target))
  } else {
    visibleNodes = rawData.nodes.filter(n => activeCategories.value.has(n.category))
    const ids = new Set(visibleNodes.map(n => n.id))
    visibleEdges = rawData.edges.filter(e => ids.has(e.source) && ids.has(e.target))
  }

  if (visibleNodes.length === 0) {
    nodes.value = []; edges.value = []; return
  }
  nodes.value = visibleNodes
  edges.value = visibleEdges

  // 构建节点查找表
  const nodeMap = {}
  visibleNodes.forEach(n => { nodeMap[n.id] = n })

  const dataNodes = visibleNodes.map(n => ({
    id: n.id,
    data: {
      label: n.label,
      category: n.category,
      color: n.style?.fill || '#c9a84c',
      nodeSize: n.size || 24,
    },
  }))

  const dataEdges = visibleEdges.map(e => ({
    id: e.id,
    source: e.source,
    target: e.target,
    data: { label: e.label },
  }))

  graph = new Graph({
    container: chartContainer.value,
    width: clientWidth,
    height: clientHeight,
    autoFit: 'center',
    padding: [60, 40, 60, 40],
    data: { nodes: dataNodes, edges: dataEdges },
    node: {
      type: 'circle',
      style: {
        size: (d) => d.data?.nodeSize || 24,
        fill: (d) => d.data?.color || '#c9a84c',
        stroke: (d) => d.data?.color || '#c9a84c',
        strokeOpacity: 0.3,
        lineWidth: 3,
        // 标签
        labelText: (d) => {
          const label = d.data?.label || ''
          return label.length > 8 ? label.slice(0, 7) + '…' : label
        },
        labelFill: '#3a2f24',
        labelFontSize: 12,
        labelFontWeight: 500,
        labelPlacement: 'bottom',
        labelOffsetY: 4,
        labelBackground: true,
        labelBackgroundFill: 'rgba(255,255,255,0.85)',
        labelBackgroundRadius: 4,
        labelBackgroundPadding: [2, 6],
        labelBackgroundStroke: (d) => d.data?.color || '#c9a84c',
        labelBackgroundStrokeOpacity: 0.15,
        labelBackgroundLineWidth: 1,
        // 阴影
        shadowBlur: 6,
        shadowColor: 'rgba(0,0,0,0.08)',
        shadowOffsetX: 0,
        shadowOffsetY: 2,
        // 光标
        cursor: 'pointer',
      },
      state: {
        selected: {
          lineWidth: 3,
          stroke: '#e8b84b',
          strokeOpacity: 0.8,
          shadowBlur: 16,
          shadowColor: 'rgba(201,168,76,0.35)',
          labelFontSize: 13,
          labelFontWeight: 700,
          labelFill: '#2a1f14',
          labelBackgroundFill: 'rgba(255,255,255,0.95)',
        },
        inactive: {
          fill: '#d4c8b0',
          stroke: '#d4c8b0',
          strokeOpacity: 0.2,
          labelFill: '#b0a090',
          labelBackgroundFill: 'rgba(255,255,255,0.5)',
          labelBackgroundStroke: 'transparent',
          opacity: 0.35,
          shadowBlur: 0,
        },
      },
    },
    edge: {
      type: 'line',
      style: {
        stroke: '#c9a84c',
        strokeOpacity: 0.35,
        lineWidth: 1.2,
        lineDash: [6, 3],
        endArrow: true,
        endArrowType: 'triangle',
        endArrowSize: 8,
        endArrowFill: '#c9a84c',
        endArrowFillOpacity: 0.5,
        labelText: (d) => d.data?.label || '',
        labelFontSize: 10,
        labelFill: '#8b7355',
        labelFontWeight: 400,
        labelAutoRotate: true,
        labelBackground: true,
        labelBackgroundFill: 'rgba(255,255,255,0.8)',
        labelBackgroundRadius: 3,
        labelBackgroundPadding: [1, 4],
        cursor: 'default',
      },
      state: {
        selected: {
          stroke: '#c9a84c',
          strokeOpacity: 0.7,
          lineWidth: 2,
          lineDash: [0, 0],
          endArrowFillOpacity: 0.8,
          labelFill: '#5a3d2f',
          labelFontWeight: 500,
        },
        inactive: {
          stroke: '#d4c8b0',
          strokeOpacity: 0.15,
          labelFill: 'transparent',
          labelBackgroundFill: 'transparent',
        },
      },
    },
    layout: {
      type: 'force',
      linkDistance: 180,
      nodeStrength: -200,
      edgeStrength: 0.15,
      preventOverlap: true,
      nodeSize: (d) => (d.data?.nodeSize || 24) + 20,
      nodeSpacing: 16,
      animation: false,
    },
    behaviors: [
      { type: 'drag-canvas', sensitivity: 0.8 },
      { type: 'zoom-canvas', sensitivity: 0.8, enableOptimize: true },
      { type: 'drag-element', enableOptimize: true },
      { type: 'click-select', multiple: false },
    ],
    theme: { type: 'light', background: 'transparent' },
  })

  await graph.render()

  // 事件绑定
  graph.on('node:click', (e) => {
    const id = e.target?.id
    if (!id) return
    showNodeDetail(id)
    highlightNeighbors(id)
  })
  graph.on('edge:click', () => clearHighlight())
  graph.on('canvas:click', () => clearHighlight())
}

// ==================== 交互 ====================
function highlightNeighbors(nodeId) {
  if (!graph) return
  focusedNodeId.value = nodeId
  const neighborIds = new Set([nodeId])
  rawData.edges.forEach(e => {
    if (e.source === nodeId) neighborIds.add(e.target)
    if (e.target === nodeId) neighborIds.add(e.source)
  })
  graph.getNodeData().forEach(n => {
    graph.setElementState(n.id, neighborIds.has(n.id) ? 'selected' : 'inactive')
  })
  graph.getEdgeData().forEach(ed => {
    graph.setElementState(ed.id, (ed.source === nodeId || ed.target === nodeId) ? 'selected' : 'inactive')
  })
  if (isFocusedView.value) {
    try { graph.focusElement(nodeId, { duration: 500, easing: 'ease-in-out' }) } catch (_) {}
  }
}

function clearHighlight() {
  if (!graph) return
  focusedNodeId.value = null
  detailNode.value = null
  detailRelations.value = []
  graph.getNodeData().forEach(n => graph.setElementState(n.id, 'selected'))
  graph.getEdgeData().forEach(ed => graph.setElementState(ed.id, 'selected'))
  if (isFocusedView.value) {
    try { graph.fitView({ duration: 500 }) } catch (_) {}
  }
}

function showNodeDetail(nodeId) {
  const node = rawData.nodes.find(n => n.id === nodeId)
  if (!node) return
  detailNode.value = {
    id: node.id,
    label: node.label,
    category: node.category,
    categoryLabel: node.categoryLabel || CATEGORY_LABELS[node.category] || node.category,
    color: node.style?.fill || '#c9a84c',
  }
  const rels = []
  rawData.edges.forEach(e => {
    if (e.source === nodeId) {
      const t = rawData.nodes.find(n => n.id === e.target)
      if (t) rels.push({ label: e.label, targetId: e.target, targetLabel: t.label })
    } else if (e.target === nodeId) {
      const s = rawData.nodes.find(n => n.id === e.source)
      if (s) rels.push({ label: '被' + (e.label || '关联'), targetId: e.source, targetLabel: s.label })
    }
  })
  detailRelations.value = rels
}

function focusNode(nodeId) {
  searchText.value = ''
  searchResults.value = []
  isFocusedView.value = true
  focusedNodeId.value = nodeId
  showNodeDetail(nodeId)
  nextTick(() => renderGraph())
}

function exitFocusedView() {
  isFocusedView.value = false
  focusedNodeId.value = null
  detailNode.value = null
  detailRelations.value = []
  nextTick(() => renderGraph())
}

function resetLayout() {
  if (!graph) return
  graph.layout()
  graph.fitView({ duration: 500 })
}

function toggleCategory(catId) {
  isFocusedView.value = false
  focusedNodeId.value = null
  detailNode.value = null
  detailRelations.value = []
  const next = new Set(activeCategories.value)
  if (next.has(catId)) next.delete(catId)
  else next.add(catId)
  activeCategories.value = next
  nextTick(() => renderGraph())
}

// ==================== 搜索 ====================
function onSearchInput() {
  const q = searchText.value.trim().toLowerCase()
  if (!q) { searchResults.value = []; return }
  searchResults.value = (rawData.nodes || [])
    .filter(n => n.label && n.label.toLowerCase().includes(q))
    .slice(0, 8)
    .map(n => ({
      id: n.id,
      label: n.label,
      category: n.category,
      categoryLabel: n.categoryLabel || CATEGORY_LABELS[n.category] || n.category,
      color: n.style?.fill || '#c9a84c',
    }))
}

function clearSearch() { searchResults.value = [] }

function handleResize() {
  if (!graph || !chartContainer.value) return
  const { clientWidth, clientHeight } = chartContainer.value
  graph.resize(clientWidth, clientHeight)
}

// ==================== 生命周期 ====================
onMounted(async () => {
  await nextTick()
  resizeObserver = new ResizeObserver(handleResize)
  if (chartContainer.value) resizeObserver.observe(chartContainer.value)
  fetchData()
})

onUnmounted(() => {
  if (graph) { graph.destroy(); graph = null }
  if (resizeObserver) { resizeObserver.disconnect(); resizeObserver = null }
})
</script>

<style scoped>
/* ==================== 容器 ==================== */
.kg-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: calc(100vh - 120px);
  min-height: 500px;
}

/* ==================== 工具栏 ==================== */
.kg-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: rgba(255,255,255,0.75);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 12px;
  backdrop-filter: blur(8px);
}

.kg-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 0.5px;
}

.kg-title-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(201,168,76,0.05));
  color: #c9a84c;
  font-size: 18px;
}

.kg-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ==================== 信息行 ==================== */
.kg-info-row {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background: rgba(255,255,255,0.6);
  border: 1px solid rgba(201,168,76,0.15);
  border-radius: 12px;
  backdrop-filter: blur(8px);
  flex-wrap: wrap;
  gap: 16px;
}

/* 搜索 */
.kg-search {
  position: relative;
  width: 200px;
  flex-shrink: 0;
}

.kg-search :deep(.el-input__wrapper) {
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(201,168,76,0.15) inset;
}

.search-results {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 50;
  background: #fff;
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 10px;
  max-height: 220px;
  overflow-y: auto;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.search-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 13px;
}
.search-item:hover { background: rgba(201,168,76,0.06); }
.search-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.search-name { flex: 1; color: #4a3f35; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.search-cat { font-size: 11px; color: #8b7355; background: rgba(201,168,76,0.08); padding: 1px 8px; border-radius: 10px; flex-shrink: 0; }

/* 统计 */
.kg-stats {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-shrink: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 48px;
}

.stat-num {
  font-size: 20px;
  font-weight: 700;
  color: #c9a84c;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  font-size: 11px;
  color: #8b7355;
  letter-spacing: 0.5px;
  margin-top: 2px;
}

.stat-divider {
  width: 1px;
  height: 28px;
  background: rgba(201,168,76,0.2);
}

/* 图例 */
.kg-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1;
  justify-content: flex-end;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  background: rgba(255,255,255,0.5);
  border: 1px solid transparent;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px;
  color: #5a4d3f;
  user-select: none;
}
.legend-item:hover {
  background: rgba(201,168,76,0.08);
  border-color: rgba(201,168,76,0.25);
}
.legend-item.active {
  background: rgba(201,168,76,0.1);
  border-color: rgba(201,168,76,0.35);
  color: #3a2f24;
  font-weight: 600;
}
.legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.legend-text { white-space: nowrap; }

/* ==================== 画布容器 ==================== */
.kg-chart-wrap {
  position: relative;
  flex: 1;
  min-height: 400px;
  background: rgba(255,255,255,0.45);
  border: 1px solid rgba(201,168,76,0.15);
  border-radius: 14px;
  overflow: hidden;
}

.kg-chart {
  width: 100%;
  height: 100%;
}

/* 空状态 & 加载 */
.kg-empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.5);
}

.kg-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #8b7355;
  background: rgba(255,255,255,0.5);
  font-size: 13px;
}

.kg-spin {
  font-size: 32px;
  color: #c9a84c;
  animation: spin 1.2s linear infinite;
}

/* ==================== 节点详情面板 ==================== */
.node-detail-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 220px;
  max-height: calc(100% - 32px);
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 12px;
  padding: 14px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  overflow-y: auto;
  z-index: 10;
}

.detail-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.detail-badge {
  font-size: 11px;
  color: #fff;
  padding: 2px 10px;
  border-radius: 10px;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.detail-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #8b7355;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background 0.15s;
}
.detail-close:hover { background: rgba(0,0,0,0.04); color: #c07050; }

.detail-name {
  font-size: 15px;
  font-weight: 700;
  color: #3a2f24;
  margin: 0 0 12px;
  line-height: 1.4;
}

.detail-rel-section { border-top: 1px solid rgba(201,168,76,0.12); padding-top: 10px; }

.detail-rel-title {
  font-size: 11px;
  color: #8b7355;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
  font-weight: 600;
}

.detail-rel-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 12px;
}
.detail-rel-item:hover { background: rgba(201,168,76,0.06); }

.rel-label { color: #8b7355; flex-shrink: 0; font-size: 11px; }
.rel-arrow { color: #c9a84c; font-size: 10px; flex-shrink: 0; }
.rel-target { color: #c9a84c; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.detail-no-rel {
  font-size: 12px;
  color: #b0a090;
  text-align: center;
  padding: 12px 0;
}

/* 面板动画 */
.panel-enter-active { transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
.panel-leave-active { transition: all 0.15s ease; }
.panel-enter-from { opacity: 0; transform: translateX(16px); }
.panel-leave-to { opacity: 0; transform: translateX(16px); }

/* ==================== 动画 ==================== */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>