<template>
  <div class="tombs-map">
    <div class="map-header">
      <h2>唐三彩墓葬出土地点分布</h2>
      <p class="map-desc">共 <strong>{{ tombs.length }}</strong> 处墓葬遗址，覆盖 <strong>{{ uniqueLocations }}</strong> 个地区</p>
    </div>
    <div class="map-body">
      <div class="map-wrapper">
        <div ref="mapChart" class="map-container"></div>
        <!-- 左上角模式切换 -->
        <div class="map-mode-switch">
          <span
            class="mode-btn"
            :class="{ active: !showHeatmap }"
            @click="toggleMode(false)"
          >散点图</span>
          <span
            class="mode-btn"
            :class="{ active: showHeatmap }"
            @click="toggleMode(true)"
          >热力图</span>
        </div>
        <!-- 右上角分布概览 -->
        <div class="map-summary" :class="{ 'panel-open': selectedLocation }">
          <div class="summary-title">分布概览</div>
          <div class="summary-list">
            <div
              v-for="item in locationRanking"
              :key="item.name"
              class="summary-item"
              :class="{ active: selectedLocation === item.name }"
              @click="handleSummaryClick(item.name)"
            >
              <span class="summary-name" :title="item.name">{{ item.name }}</span>
              <div class="summary-bar-bg">
                <div
                  class="summary-bar"
                  :style="{ width: item.percent + '%' }"
                ></div>
              </div>
              <span class="summary-count">{{ item.count }}</span>
            </div>
          </div>
        </div>
        <!-- 右侧文物联动面板（悬浮覆盖） -->
        <transition name="slide">
          <div v-if="selectedLocation" class="artifact-panel">
            <div class="panel-header">
              <div class="panel-title">
                <span class="panel-location">{{ selectedLocation }}</span>
                <span class="panel-badge">{{ selectedTombs.length }} 处墓葬</span>
              </div>
              <span class="panel-close" @click="closePanel">&times;</span>
            </div>
            <!-- 墓葬列表 -->
            <div class="panel-section">
              <div class="section-label">墓葬信息</div>
              <div class="tomb-list">
                <div v-for="tomb in selectedTombs" :key="tomb.id" class="tomb-card">
                  <div class="tomb-name">{{ tomb.name }}</div>
                  <div class="tomb-meta">
                    <span v-if="tomb.era">{{ tomb.era }}</span>
                    <span v-if="tomb.sancai_items" class="tomb-items">{{ tomb.sancai_items }}</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- 关联文物 -->
            <div class="panel-section">
              <div class="section-label">
                关联文物
                <span v-if="artifactsLoading" class="loading-hint">加载中...</span>
                <span v-else-if="relatedArtifacts.length" class="artifact-count">{{ relatedArtifacts.length }} 件</span>
                <span v-else class="loading-hint">暂无数据</span>
              </div>
              <div class="artifact-list">
                <div v-for="art in relatedArtifacts" :key="art.id" class="artifact-card">
                  <div class="art-img" v-if="art.image_url">
                    <img :src="getImageUrl(art.image_url)" alt="" />
                  </div>
                  <div class="art-img art-img-empty" v-else>
                    <span>无图</span>
                  </div>
                  <div class="art-info">
                    <div class="art-name">{{ art.name }}</div>
                    <div class="art-meta">
                      <span v-if="art.era">{{ art.era }}</span>
                      <span v-if="art.type">{{ art.type }}</span>
                      <span v-if="art.glaze">{{ art.glaze }}</span>
                    </div>
                    <div v-if="art.museum" class="art-location">{{ art.museum }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import chinaGeoJSON from '@/assets/china.json'
import request from '@/utils/request'
import { getImageUrl } from '@/utils/imageUrl'

const mapChart = ref(null)
let chartInstance = null
const tombs = ref([])
const showHeatmap = ref(false)

// 联动状态
const selectedLocation = ref('')
const relatedArtifacts = ref([])
const artifactsLoading = ref(false)

const uniqueLocations = computed(() => {
  return new Set(tombs.value.map(t => t.location)).size
})

// 当前选中地点的墓葬
const selectedTombs = computed(() => {
  if (!selectedLocation.value) return []
  return tombs.value.filter(t => t.location === selectedLocation.value)
})

// 按地区聚合统计，用于右上角概览（只显示前8名）
const locationRanking = computed(() => {
  const map = {}
  tombs.value.forEach(t => {
    if (!t.location) return
    map[t.location] = (map[t.location] || 0) + 1
  })
  const list = Object.entries(map)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
  const max = list.length ? list[0].count : 1
  return list.map(item => ({
    ...item,
    percent: Math.round((item.count / max) * 100),
  }))
})

// 选中地点，加载关联文物
async function selectLocation(location) {
  if (selectedLocation.value === location) return
  selectedLocation.value = location
  relatedArtifacts.value = []
  artifactsLoading.value = true
  try {
    const res = await request.get('/tombs/map/artifacts', { params: { location } })
    if (res.code === '200') {
      relatedArtifacts.value = res.data || []
    }
  } finally {
    artifactsLoading.value = false
  }
}

function closePanel() {
  selectedLocation.value = ''
  relatedArtifacts.value = []
}

// 右上角概览点击
function handleSummaryClick(location) {
  selectLocation(location)
}

// 将同一地点的墓葬聚合
function aggregateByLocation(data) {
  const locationMap = {}
  data.forEach(t => {
    const lng = t.longitude
    const lat = t.latitude
    if (lng == null || lat == null) return
    const key = t.location
    if (!locationMap[key]) {
      locationMap[key] = { coords: [lng, lat], items: [] }
    }
    locationMap[key].items.push(t)
  })
  return locationMap
}

function getScatterOption(locationMap) {
  const scatterData = Object.entries(locationMap).map(([loc, info]) => ({
    name: loc,
    value: [...info.coords, info.items.length],
    items: info.items,
  }))

  // 按省份聚合统计数量，用于颜色深浅
  const provinceMap = {}
  scatterData.forEach(d => {
    const province = extractProvince(d.name)
    provinceMap[province] = (provinceMap[province] || 0) + d.value[2]
  })
  const provinceCounts = Object.values(provinceMap)
  const maxProvinceCount = Math.max(...provinceCounts, 1)

  // 为每个散点分配颜色（基于所属省份的总数）
  const colorPalette = ['#e8c88a', '#d4a76a', '#c4823e', '#a0522d', '#8b1a1a']
  scatterData.forEach(d => {
    const province = extractProvince(d.name)
    const count = provinceMap[province]
    const ratio = count / maxProvinceCount
    const colorIndex = Math.min(Math.floor(ratio * colorPalette.length), colorPalette.length - 1)
    d.itemStyle = { color: colorPalette[colorIndex] }
  })

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(44, 36, 27, 0.92)',
      borderColor: '#c9a84c',
      borderWidth: 1,
      textStyle: { color: '#e8dcc8', fontSize: 13 },
      formatter(params) {
        if (params.seriesType !== 'scatter') return ''
        const items = params.data.items
        let html = `<div style="font-weight:700;font-size:14px;margin-bottom:6px;color:#c9a84c">${params.name}</div>`
        html += `<div style="margin-bottom:4px;color:#a09080">出土墓葬 ${items.length} 处 · 点击查看详情</div>`
        items.forEach(item => {
          html += `<div style="padding:2px 0;border-top:1px solid rgba(255,255,255,0.08)">`
          html += `<span style="color:#e8dcc8">${item.name}</span>`
          if (item.era) html += `<span style="color:#8b7355;margin-left:6px">${item.era}</span>`
          html += `</div>`
        })
        return html
      }
    },
    series: [{
      type: 'scatter',
      coordinateSystem: 'geo',
      data: scatterData,
      symbolSize(val) {
        return Math.max(10, Math.min(24, val[2] * 5))
      },
      itemStyle: {
        shadowBlur: 6,
        shadowColor: 'rgba(196, 130, 62, 0.4)',
      },
      emphasis: {
        scale: 1.6,
        itemStyle: {
          shadowBlur: 12,
          shadowColor: 'rgba(232, 168, 76, 0.6)',
        }
      },
    }]
  }
}

// 从地点名称提取省份
function extractProvince(location) {
  if (!location) return '其他'
  const provinces = ['河南', '陕西', '山西', '江苏', '河北', '山东', '四川', '湖北', '湖南', '安徽', '浙江', '江西', '福建', '广东', '广西', '云南', '贵州', '甘肃', '青海', '宁夏', '新疆', '西藏', '内蒙古', '黑龙江', '吉林', '辽宁', '北京', '天津', '上海', '重庆']
  for (const p of provinces) {
    if (location.includes(p)) return p
  }
  // 特殊处理：西安、咸阳、乾县等属于陕西
  if (['西安', '咸阳', '乾县', '礼泉', '凤翔', '宝鸡', '潼关', '华阴'].some(k => location.includes(k))) return '陕西'
  // 洛阳、巩义、郑州等属于河南
  if (['洛阳', '巩义', '郑州', '孟津', '偃师', '新安', '登封', '开封'].some(k => location.includes(k))) return '河南'
  // 扬州属于江苏
  if (location.includes('扬州')) return '江苏'
  // 太原属于山西
  if (location.includes('太原')) return '山西'
  return '其他'
}

function getHeatmapOption(locationMap) {
  const heatmapData = Object.values(locationMap).map(info => [
    info.coords[0], info.coords[1], info.items.length
  ])

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(44, 36, 27, 0.92)',
      borderColor: '#c9a84c',
      borderWidth: 1,
      textStyle: { color: '#e8dcc8', fontSize: 13 },
      formatter(params) {
        if (params.seriesType !== 'heatmap') return ''
        const loc = Object.entries(locationMap).find(
          ([, info]) => info.coords[0] === params.value[0] && info.coords[1] === params.value[1]
        )
        if (!loc) return ''
        const [name, info] = loc
        let html = `<div style="font-weight:700;font-size:14px;margin-bottom:6px;color:#c9a84c">${name}</div>`
        html += `<div style="color:#a09080">出土墓葬 ${info.items.length} 处 · 点击查看详情</div>`
        return html
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...Object.values(locationMap).map(i => i.items.length), 1),
      text: ['密集', '稀疏'],
      textStyle: { color: '#5a4d3f' },
      inRange: {
        color: ['#f5edd8', '#e8c88a', '#c4823e', '#a0522d', '#8b1a1a']
      },
      calculable: true,
      orient: 'vertical',
      left: 16,
      bottom: 24,
      itemWidth: 12,
      itemHeight: 100,
    },
    series: [{
      type: 'heatmap',
      coordinateSystem: 'geo',
      data: heatmapData,
      pointSize: 18,
      blurSize: 24,
    }]
  }
}

// 按省份统计墓葬数量，用于地图着色
function getProvinceCountMap(data) {
  const provinceMap = {}
  data.forEach(t => {
    if (!t.location) return
    const province = extractProvince(t.location)
    provinceMap[province] = (provinceMap[province] || 0) + 1
  })
  return Object.entries(provinceMap).map(([name, value]) => ({ name, value }))
}

function getBaseOption(data) {
  const provinceData = getProvinceCountMap(data)
  const maxCount = Math.max(...provinceData.map(d => d.value), 1)

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(44, 36, 27, 0.92)',
      borderColor: '#c9a84c',
      borderWidth: 1,
      textStyle: { color: '#e8dcc8', fontSize: 13 },
      formatter(params) {
        if (params.seriesType === 'map') {
          return `<div style="font-weight:700;font-size:14px;color:#c9a84c">${params.name}</div>
                  <div style="color:#a09080;margin-top:4px">出土墓葬 ${params.value || 0} 处</div>`
        }
        return ''
      }
    },
    visualMap: {
      min: 0,
      max: maxCount,
      text: ['密集', '稀疏'],
      textStyle: { color: '#5a4d3f' },
      inRange: {
        color: ['#f5edd8', '#e8d5a3', '#d4a76a', '#c4823e', '#a0522d'],
      },
      orient: 'vertical',
      left: 16,
      bottom: 24,
      itemWidth: 12,
      itemHeight: 100,
      show: !showHeatmap.value,
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      center: [108, 35],
      itemStyle: {
        areaColor: '#f5edd8',
        borderColor: '#c4823e',
        borderWidth: 0.8,
      },
      emphasis: {
        itemStyle: { areaColor: '#e8d5a3' },
        label: { show: false }
      },
      label: { show: false }
    },
    series: [
      {
        type: 'map',
        map: 'china',
        geoIndex: 0,
        data: provinceData,
        silent: true,
      }
    ]
  }
}

function renderMap() {
  if (!chartInstance || !tombs.value.length) return
  const locationMap = aggregateByLocation(tombs.value)
  const baseOption = getBaseOption(tombs.value)
  const modeOption = showHeatmap.value
    ? getHeatmapOption(locationMap)
    : getScatterOption(locationMap)
  chartInstance.setOption({ ...baseOption, ...modeOption }, true)
}

function toggleMode(heatmap) {
  showHeatmap.value = heatmap
  renderMap()
}

function handleResize() {
  chartInstance?.resize()
}

// 地图点击事件
function handleChartClick(params) {
  if (params.componentType === 'series') {
    const locationName = params.name
    if (locationName) {
      selectLocation(locationName)
    }
  }
}

onMounted(async () => {
  const res = await request.get('/tombs/map/locations')
  if (res.code === '200') {
    tombs.value = res.data
  }

  echarts.registerMap('china', chinaGeoJSON)
  chartInstance = echarts.init(mapChart.value)
  chartInstance.on('click', handleChartClick)
  renderMap()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.tombs-map {
  background: #faf6f0;
  border-radius: 8px;
  padding: 16px 20px;
  border: 1px solid #e0d5c5;
  height: calc(100vh - 60px - 32px);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.map-header {
  text-align: center;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.map-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 4px;
  letter-spacing: 2px;
}

.map-desc {
  color: #8b7355;
  font-size: 13px;
  margin: 0;
}

.map-desc strong {
  color: #c4823e;
}

.map-body {
  display: flex;
  gap: 0;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  width: 100%;
}

.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 6px;
  overflow: hidden;
}

/* 左上角模式切换 */
.map-mode-switch {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 10;
  display: flex;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  border: 1px solid #e0d5c5;
}

.mode-btn {
  padding: 6px 16px;
  font-size: 13px;
  color: #8b7355;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.mode-btn + .mode-btn {
  border-left: 1px solid #e0d5c5;
}

.mode-btn:hover {
  color: #c4823e;
}

.mode-btn.active {
  background: #c4823e;
  color: #fff;
}

/* 右上角分布概览 */
.map-summary {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  width: 180px;
  background: rgba(255, 255, 255, 0.94);
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  border: 1px solid #e0d5c5;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: right 0.3s ease;
}

.map-summary.panel-open {
  right: 344px;
}

.summary-title {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  color: #4a3f35;
  border-bottom: 1px solid #e0d5c5;
  background: rgba(196, 130, 62, 0.08);
}

.summary-list {
  padding: 6px 0;
  flex: 1;
}

.summary-item {
  display: flex;
  align-items: center;
  padding: 4px 12px;
  gap: 8px;
  cursor: pointer;
  transition: background 0.15s;
}

.summary-item:hover {
  background: rgba(196, 130, 62, 0.08);
}

.summary-item.active {
  background: rgba(196, 130, 62, 0.15);
}

.summary-name {
  width: 64px;
  font-size: 12px;
  color: #5a4d3f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.summary-bar-bg {
  flex: 1;
  height: 6px;
  background: #ede5d8;
  border-radius: 3px;
  overflow: hidden;
}

.summary-bar {
  height: 100%;
  background: linear-gradient(90deg, #e8c88a, #c4823e);
  border-radius: 3px;
  transition: width 0.3s;
}

.summary-count {
  width: 20px;
  text-align: right;
  font-size: 12px;
  font-weight: 600;
  color: #c4823e;
  flex-shrink: 0;
}

/* 右侧文物联动面板 */
.artifact-panel {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 20;
  width: 320px;
  height: calc(100% - 24px);
  background: rgba(255, 255, 255, 0.96);
  border-radius: 6px;
  border: 1px solid #e0d5c5;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #e0d5c5;
  background: rgba(196, 130, 62, 0.06);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-location {
  font-size: 15px;
  font-weight: 600;
  color: #4a3f35;
}

.panel-badge {
  font-size: 11px;
  color: #c4823e;
  background: rgba(196, 130, 62, 0.12);
  padding: 2px 8px;
  border-radius: 10px;
}

.panel-close {
  font-size: 20px;
  color: #8b7355;
  cursor: pointer;
  line-height: 1;
  padding: 0 4px;
  transition: color 0.15s;
}

.panel-close:hover {
  color: #c4823e;
}

.panel-section {
  padding: 12px 16px;
  border-bottom: 1px solid #f0e8da;
}

.panel-section:last-child {
  border-bottom: none;
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.section-label {
  font-size: 12px;
  font-weight: 600;
  color: #8b7355;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.artifact-count {
  font-weight: 400;
  color: #c4823e;
  font-size: 11px;
}

.loading-hint {
  font-weight: 400;
  color: #b0a090;
  font-size: 11px;
}

/* 墓葬卡片 */
.tomb-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tomb-card {
  background: #faf6f0;
  border-radius: 4px;
  padding: 8px 10px;
  border: 1px solid #ede5d8;
}

.tomb-name {
  font-size: 13px;
  font-weight: 600;
  color: #4a3f35;
}

.tomb-meta {
  display: flex;
  gap: 8px;
  margin-top: 3px;
  font-size: 11px;
  color: #8b7355;
}

.tomb-items {
  color: #c4823e;
}

/* 文物卡片 */
.artifact-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.artifact-card {
  display: flex;
  gap: 10px;
  background: #faf6f0;
  border-radius: 4px;
  padding: 8px 10px;
  border: 1px solid #ede5d8;
}

.art-img {
  width: 52px;
  height: 52px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #e0d5c5;
}

.art-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.art-img-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0e8da;
  font-size: 11px;
  color: #b0a090;
}

.art-info {
  flex: 1;
  min-width: 0;
}

.art-name {
  font-size: 13px;
  font-weight: 600;
  color: #4a3f35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.art-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 3px;
  font-size: 11px;
  color: #8b7355;
}

.art-location {
  font-size: 11px;
  color: #a09080;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 面板滑入动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.35s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(340px);
}
</style>
