<template>
  <div class="appreciation-page">
    <!-- 顶部导航 -->
    <header class="app-nav">
      <div class="nav-inner">
        <router-link to="/" class="nav-brand">
          <img src="../../assets/imgs/logo2.png" alt="" class="brand-icon">
          <span class="brand-text">唐三彩文物系统</span>
        </router-link>
        <div class="nav-actions">
          <router-link to="/" class="nav-back">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero 区域 -->
    <section class="app-hero">
      <div class="hero-pattern"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-line"></span>
          <span class="badge-text">文物鉴赏</span>
          <span class="badge-line"></span>
        </div>
        <h1 class="hero-title">千载流彩</h1>
        <p class="hero-subtitle">唐三彩文物数字典藏</p>
        <p class="hero-desc">
          穿越千年时光，探寻盛唐气象。以数字化之力，守护华夏文明的璀璨瑰宝。
        </p>
      </div>
    </section>

    <!-- 筛选栏 -->
    <section class="filter-section">
      <div class="filter-inner">
        <div class="filter-group">
          <el-select v-model="filters.era" placeholder="全部年代" clearable size="large" @change="search">
            <el-option v-for="e in filterOptions.eras" :key="e" :label="e" :value="e" />
          </el-select>
          <el-select v-model="filters.type" placeholder="全部器型" clearable size="large" @change="search">
            <el-option v-for="t in filterOptions.types" :key="t" :label="t" :value="t" />
          </el-select>
          <el-select v-model="filters.museum" placeholder="全部馆藏" clearable size="large" @change="search">
            <el-option v-for="m in filterOptions.museums" :key="m" :label="m" :value="m" />
          </el-select>
        </div>
        <div class="filter-search">
          <el-input v-model="filters.name" placeholder="搜索文物名称..." clearable size="large" @keyup.enter="search" @clear="search">
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
    </section>

    <!-- 文物列表 -->
    <section class="gallery-section">
      <div v-if="loading" class="gallery-loading">
        <div class="loading-spinner"></div>
        <span>正在加载文物数据...</span>
      </div>

      <div v-else-if="list.length === 0" class="gallery-empty">
        <el-icon :size="64"><Collection /></el-icon>
        <p>暂无符合条件的文物</p>
      </div>

      <div v-else class="gallery-grid">
        <div
          v-for="(item, index) in list"
          :key="item.id"
          class="gallery-card"
          :style="{ '--delay': index * 0.05 + 's' }"
          @click="goDetail(item)"
        >
          <div class="card-image">
            <img v-if="item.image_url" :src="getImageUrl(item.image_url)" :alt="item.name" />
            <div v-else class="card-placeholder">
              <el-icon :size="40"><Collection /></el-icon>
            </div>
            <div class="card-overlay">
              <span class="overlay-hint">点击查看详情</span>
            </div>
            <button
              class="card-fav"
              :class="{ 'is-fav': favoriteIds.has(item.id) }"
              @click="(e) => toggleFavorite(e, item)"
              :title="favoriteIds.has(item.id) ? '取消收藏' : '收藏'"
            >
              <el-icon :size="18"><StarFilled /></el-icon>
            </button>
          </div>
          <div class="card-body">
            <div class="card-tags">
              <span class="tag-era">{{ item.era }}</span>
              <span class="tag-type">{{ item.type }}</span>
            </div>
            <h3 class="card-name">{{ item.name }}</h3>
            <div class="card-meta">
              <span class="meta-museum">{{ item.museum || '-' }}</span>
              <span class="meta-level" v-if="item.level">{{ item.level }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="total > pageSize" class="gallery-pagination">
        <el-pagination
          v-model:current-page="pageNum"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          background
          @current-change="loadData"
        />
      </div>
    </section>

    <!-- 详情弹窗 -->
    <!-- 已改为独立详情页 /artifact/:id -->

    <!-- 页脚 -->
    <footer class="app-footer">
      <div class="footer-inner">
        <span>唐三彩文物数字化管理系统 v1.0</span>
        <span class="footer-sep">|</span>
        <span>守护千年文明，传承文化瑰宝</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Search, Collection, StarFilled } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { getImageUrl } from '@/utils/imageUrl'

const router = useRouter()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const pageNum = ref(1)
const pageSize = 12
const favoriteIds = ref(new Set())

const filters = reactive({
  name: '',
  era: '',
  type: '',
  museum: '',
})

const filterOptions = reactive({
  eras: [],
  types: [],
  museums: [],
})

const loadFilters = () => {
  request.get('/artifacts/filters').then(res => {
    if (res.code === '200') {
      filterOptions.eras = res.data.eras || []
      filterOptions.types = res.data.types || []
      filterOptions.museums = res.data.museums || []
    }
  }).catch(() => {})
}

const loadFavorites = () => {
  request.get('/favorites/list').then(res => {
    if (res.code === '200') {
      favoriteIds.value = new Set(res.data || [])
    }
  }).catch(() => {})
}

const toggleFavorite = (e, artifact) => {
  e.stopPropagation()
  request.post('/favorites/toggle', { artifact_id: artifact.id }).then(res => {
    if (res.code === '200') {
      if (res.data.favorited) {
        favoriteIds.value.add(artifact.id)
      } else {
        favoriteIds.value.delete(artifact.id)
      }
      favoriteIds.value = new Set(favoriteIds.value)
    }
  }).catch(() => {})
}

const loadData = () => {
  loading.value = true
  request.get('/artifacts/selectPage', {
    params: {
      name: filters.name,
      era: filters.era,
      type: filters.type,
      museum: filters.museum,
      pageNum: pageNum.value,
      pageSize,
    }
  }).then(res => {
    if (res.code === '200') {
      list.value = res.data?.list || []
      total.value = res.data?.total || 0
    }
  }).catch(() => {}).finally(() => {
    loading.value = false
  })
}

const search = () => {
  pageNum.value = 1
  loadData()
}

const goDetail = (item) => {
  router.push(`/artifact/${item.id}`)
}

onMounted(() => {
  loadFilters()
  loadFavorites()
  loadData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.appreciation-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  background: #f5f0e8;
  min-height: 100vh;
}

/* ========== 导航 ========== */
.app-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(44, 36, 27, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(201, 168, 76, 0.2);
  padding: 0 40px;
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.brand-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid rgba(201, 168, 76, 0.4);
  padding: 2px;
}

.brand-text {
  color: #e8dcc8;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 2px;
}

.nav-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #c9a84c;
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 1px;
  padding: 8px 20px;
  border: 1px solid rgba(201, 168, 76, 0.4);
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-back:hover {
  background: rgba(201, 168, 76, 0.1);
}

/* ========== Hero ========== */
.app-hero {
  position: relative;
  padding: 120px 40px 80px;
  background: linear-gradient(180deg, #2c241b 0%, #1a1510 100%);
  text-align: center;
  overflow: hidden;
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a84c' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.badge-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 168, 76, 0.5), transparent);
}

.badge-text {
  color: #c9a84c;
  font-size: 14px;
  letter-spacing: 4px;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 12px;
  margin: 0 0 12px;
  text-shadow: 0 4px 30px rgba(201, 168, 76, 0.15);
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(232, 220, 200, 0.5);
  letter-spacing: 6px;
  margin: 0 0 20px;
}

.hero-desc {
  font-size: 15px;
  color: rgba(232, 220, 200, 0.35);
  letter-spacing: 1px;
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.8;
}

/* ========== 筛选栏 ========== */
.filter-section {
  padding: 0 40px;
  position: sticky;
  top: 64px;
  z-index: 50;
  background: rgba(245, 240, 232, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e8e0d4;
}

.filter-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 12px;
  flex: 1;
}

.filter-group :deep(.el-select) {
  width: 160px;
}

.filter-search {
  width: 200px;
}

.filter-inner :deep(.el-input__wrapper) {
  background: #fff;
  box-shadow: 0 0 0 1px #e8e0d4 inset;
  border-radius: 6px;
}

.filter-inner :deep(.el-select .el-input__wrapper) {
  background: #fff;
}

/* ========== 画廊 ========== */
.gallery-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 40px 80px;
}

.gallery-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 120px 0;
  color: #8b7355;
  font-size: 14px;
  letter-spacing: 1px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 2px solid #e8e0d4;
  border-top-color: #c9a84c;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.gallery-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 120px 0;
  color: #a09080;
}

.gallery-empty p {
  font-size: 15px;
  letter-spacing: 1px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.gallery-card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e8e0d4;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  opacity: 0;
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: var(--delay);
}

.gallery-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
  border-color: #c9a84c;
}

.card-image {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background: #f5f0e8;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.gallery-card:hover .card-image img {
  transform: scale(1.06);
}

.card-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c9a84c;
  opacity: 0.4;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26, 21, 16, 0.7) 0%, transparent 50%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 20px;
  opacity: 0;
  transition: opacity 0.3s;
}

.gallery-card:hover .card-overlay {
  opacity: 1;
}

.overlay-hint {
  color: #e8dcc8;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 6px 16px;
  border: 1px solid rgba(201, 168, 76, 0.5);
  border-radius: 20px;
}

.card-fav {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.85);
  color: #d0c8b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-fav:hover {
  color: #c9a84c;
  background: #fff;
  transform: scale(1.1);
}

.card-fav.is-fav {
  color: #c9a84c;
  background: rgba(201, 168, 76, 0.12);
  box-shadow: 0 0 0 2px rgba(201, 168, 76, 0.3);
}

.card-body {
  padding: 16px;
}

.card-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}

.tag-era {
  font-size: 11px;
  color: #c9a84c;
  padding: 2px 8px;
  background: rgba(201, 168, 76, 0.08);
  border-radius: 3px;
  letter-spacing: 1px;
}

.tag-type {
  font-size: 11px;
  color: #8b7355;
  padding: 2px 8px;
  background: #f5f0e8;
  border-radius: 3px;
  letter-spacing: 1px;
}

.card-name {
  font-size: 16px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 8px;
  letter-spacing: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-museum {
  font-size: 12px;
  color: #8b7355;
}

.meta-level {
  font-size: 11px;
  color: #c9a84c;
  padding: 1px 6px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 3px;
}

/* ========== 分页 ========== */
.gallery-pagination {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.gallery-pagination :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background: linear-gradient(135deg, #c9a84c, #a08040);
}

/* ========== 详情弹窗 ========== */
.detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.detail-image {
  aspect-ratio: 1 / 1;
  background: #f5f0e8;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== 页脚 ========== */
.app-footer {
  background: #1a1510;
  padding: 24px 40px;
  text-align: center;
}

.footer-inner {
  color: rgba(232, 220, 200, 0.3);
  font-size: 12px;
  letter-spacing: 1px;
}

.footer-sep {
  margin: 0 12px;
}

/* ========== 动画 ========== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-group {
    flex-wrap: wrap;
  }

  .filter-group :deep(.el-select) {
    width: 140px;
  }
}

@media (max-width: 600px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 36px;
    letter-spacing: 6px;
  }

  .app-nav {
    padding: 0 16px;
  }

  .app-hero {
    padding: 100px 20px 60px;
  }

  .gallery-section {
    padding: 24px 16px 60px;
  }

  .filter-section {
    padding: 0 16px;
  }
}
</style>