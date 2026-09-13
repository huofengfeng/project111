<template>
  <div class="timeline-page">
    <div class="page-header">
      <h2>唐三彩年代演变</h2>
      <p class="page-intro">探索唐代三彩陶瓷在不同历史时期的艺术风格演变</p>
    </div>

    <!-- 横向时间轴线条 -->
    <div class="timeline-line">
      <div class="line-track">
        <div class="line-fill" :style="{ width: fillPercent + '%' }"></div>
        <div
          v-for="(p, idx) in periods"
          :key="p.name"
          class="line-node"
          :class="{ active: currentPeriod === p.name, passed: periodIndex[idx] <= currentIdx }"
          :style="{ left: nodePositions[idx] + '%' }"
          @click="selectPeriod(p.name)"
        >
          <span class="node-dot"></span>
          <div class="node-label">
            <strong>{{ p.name }}</strong>
            <small>{{ p.year }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- 双栏布局 -->
    <div class="timeline-layout">
      <!-- 左侧：时期摘要 -->
      <div class="timeline-bar">
        <div
          v-for="p in periods"
          :key="p.name"
          class="period-nav"
          :class="{ active: currentPeriod === p.name }"
          @click="selectPeriod(p.name)"
        >
          <span class="nav-dot" :class="p.name"></span>
          <div class="nav-info">
            <strong>{{ p.name }}</strong>
            <small>{{ p.year }}</small>
          </div>
          <span class="nav-count">{{ allArtifacts[p.name]?.length || 0 }}</span>
        </div>
      </div>

      <!-- 右侧：文物展示区 -->
      <div class="timeline-content">
        <div v-if="loading" class="status-tip">
          <el-icon class="is-loading" :size="24"><Loading /></el-icon>
          <span>正在加载文物数据...</span>
        </div>

        <template v-else>
          <div class="period-header">
            <h3>
              {{ currentPeriod }}时期文物
              <small>（{{ currentData.year }}）</small>
            </h3>
            <p class="period-desc">{{ currentData.description }}</p>
            <div class="period-meta">
              <span class="period-event">
                <el-icon><Clock /></el-icon>
                {{ currentData.event }}
              </span>
              <span class="period-total">
                共 <strong>{{ currentArtifacts.length }}</strong> 件文物
              </span>
            </div>
          </div>

          <div v-if="currentArtifacts.length === 0" class="status-tip">
            <span>暂无该时期文物数据，请补充数据库记录</span>
          </div>

          <div v-else class="artifact-grid">
            <div
              v-for="item in currentArtifacts"
              :key="item.id"
              class="artifact-card"
            >
              <div class="card-img">
                <img
                  v-if="item.image_url"
                  :src="getImageUrl(item.image_url)"
                  :alt="item.name"
                  @error="handleImgError"
                />
                <div v-else class="card-placeholder">
                  <el-icon :size="32"><PictureFilled /></el-icon>
                  <span>暂无图片</span>
                </div>
              </div>
              <div class="card-info">
                <h4>{{ item.name }}</h4>
                <p v-if="item.source" class="card-source">{{ item.source }}</p>
                <div class="card-tags">
                  <span v-if="item.type" class="tag">{{ item.type }}</span>
                  <span v-if="item.glaze" class="tag">{{ item.glaze }}</span>
                  <span v-if="item.museum" class="tag tag-museum">{{ item.museum }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock, Loading, PictureFilled } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { getImageUrl } from '@/utils/imageUrl'

const periods = [
  { name: '初唐', year: '618-712' },
  { name: '盛唐', year: '713-766' },
  { name: '中唐', year: '766-835' },
  { name: '晚唐', year: '836-907' },
]

// 节点在横线上的位置百分比（均匀分布）
const nodePositions = computed(() => {
  const total = periods.length - 1
  return periods.map((_, i) => (total === 0 ? 50 : (i / total) * 100))
})

const periodIndex = { '初唐': 0, '盛唐': 1, '中唐': 2, '晚唐': 3 }

const currentPeriod = ref('初唐')
const allArtifacts = ref({})
const currentArtifacts = ref([])
const loading = ref(true)

const currentIdx = computed(() => periodIndex[currentPeriod.value] || 0)

const currentData = computed(() => {
  const config = {
    '初唐': { year: '618-712', description: '唐三彩开始出现，造型相对简单，釉色以黄、绿为主。', event: '唐朝建立' },
    '盛唐': { year: '713-766', description: '唐三彩鼎盛期，造型丰富多样，釉色鲜艳，人物俑和动物俑大量出现。', event: '开元盛世' },
    '中唐': { year: '766-835', description: '风格趋于写实，器型更加规整，部分出现绞胎工艺。', event: '安史之乱后' },
    '晚唐': { year: '836-907', description: '唐三彩逐渐衰落，产量减少，风格趋于简化。', event: '藩镇割据' },
  }
  return config[currentPeriod.value] || config['初唐']
})

// 线条填充进度
const fillPercent = computed(() => {
  const total = periods.length - 1
  if (total === 0) return 0
  return (currentIdx.value / total) * 100
})

function selectPeriod(name) {
  currentPeriod.value = name
  currentArtifacts.value = allArtifacts.value[name] || []
}

function handleImgError(e) {
  e.target.style.display = 'none'
  e.target.parentElement.querySelector('.card-placeholder')?.classList.add('show')
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await request.get('/timeline/periods')
    if (res.code === '200' && res.data) {
      res.data.forEach(p => {
        allArtifacts.value[p.name] = p.artifacts || []
      })
      currentArtifacts.value = allArtifacts.value['初唐'] || []
    }
  } catch (err) {
    console.error('加载时间线数据失败:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.timeline-page {
  /* 不额外设置背景 */
}

.page-header {
  text-align: center;
  margin-bottom: 0;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 6px;
  letter-spacing: 2px;
}

.page-intro {
  color: #8b7355;
  font-size: 14px;
  margin: 0 0 20px;
}

/* ===== 横向时间轴线条 ===== */
.timeline-line {
  padding: 0 0 40px;
  margin-bottom: 20px;
}

.line-track {
  position: relative;
  height: 4px;
  background: #e0d5c5;
  border-radius: 2px;
  margin: 0 10%;
}

.line-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #b58c59, #c4823e);
  border-radius: 2px;
  transition: width 0.4s ease;
}

.line-node {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 2;
}

.node-dot {
  display: block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #f5f0e8;
  border: 3px solid #d4c4a8;
  transition: all 0.3s ease;
  margin: 0 auto;
}

.line-node.active .node-dot,
.line-node.passed .node-dot {
  background: #c4823e;
  border-color: #c4823e;
  box-shadow: 0 0 0 6px rgba(196, 130, 62, 0.15);
}

.line-node.active .node-dot {
  width: 20px;
  height: 20px;
  border-color: #a0602d;
}

.node-label {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  white-space: nowrap;
}

.node-label strong {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #8b7355;
  transition: color 0.3s;
}

.line-node.active .node-label strong,
.line-node.passed .node-label strong {
  color: #4a3f35;
}

.node-label small {
  font-size: 11px;
  color: #b0a090;
}

/* ===== 双栏布局 ===== */
.timeline-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
}

/* 左侧时期摘要 */
.timeline-bar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.period-nav {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  background: #f5f0e8;
}

.period-nav:hover {
  background: #ede5d8;
  border-color: #d9c9a5;
}

.period-nav.active {
  background: #3a8f7b;
  color: #fff;
  border-color: #3a8f7b;
}

.nav-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.nav-dot.初唐 { background: #b58c59; }
.nav-dot.盛唐 { background: #c4823e; }
.nav-dot.中唐 { background: #a0602d; }
.nav-dot.晚唐 { background: #8b1a1a; }

.period-nav.active .nav-dot {
  background: #fff;
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.5);
}

.nav-info {
  flex: 1;
  min-width: 0;
}

.nav-info strong {
  display: block;
  font-size: 14px;
  font-weight: 600;
}

.period-nav.active .nav-info strong {
  color: #fff;
}

.nav-info small {
  font-size: 11px;
  color: #8b7355;
}

.period-nav.active .nav-info small {
  color: #e8dcc8;
}

.nav-count {
  font-size: 12px;
  font-weight: 600;
  color: #c4823e;
}

.period-nav.active .nav-count {
  color: #f5edd8;
}

/* ===== 右侧内容区 ===== */
.timeline-content {
  min-height: 400px;
}

.status-tip {
  padding: 3rem;
  text-align: center;
  color: #8b7355;
  background: #f5f0e8;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.period-header {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0d5c5;
}

.period-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 8px;
}

.period-header h3 small {
  font-size: 14px;
  color: #8b7355;
  font-weight: 400;
}

.period-desc {
  color: #5a4d3f;
  font-size: 14px;
  margin: 0 0 8px;
  line-height: 1.6;
}

.period-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: #8b7355;
}

.period-event {
  display: flex;
  align-items: center;
  gap: 4px;
}

.period-total strong {
  color: #c4823e;
  font-weight: 600;
}

.artifact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 14px;
}

.artifact-card {
  background: #f5f0e8;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid #e0d5c5;
  transition: all 0.2s ease;
}

.artifact-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
  border-color: #c4823e;
}

.card-img {
  height: 160px;
  background: #ede5d8;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #b0a090;
  font-size: 13px;
}

.card-info {
  padding: 10px 12px;
}

.card-info h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #4a3f35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-source {
  font-size: 12px;
  color: #8b7355;
  margin: 0 0 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag {
  display: inline-block;
  font-size: 11px;
  background: #3a8f7b;
  color: #fff;
  padding: 2px 8px;
  border-radius: 3px;
}

.tag-museum {
  background: #c4823e;
}

@media (max-width: 768px) {
  .timeline-layout {
    grid-template-columns: 1fr;
  }

  .line-track {
    margin: 0 2%;
  }

  .artifact-grid {
    grid-template-columns: 1fr;
  }
}
</style>