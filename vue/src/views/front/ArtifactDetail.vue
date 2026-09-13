<template>
  <div class="detail-page" v-if="artifact">
    <!-- 固定顶栏 -->
    <header class="detail-nav">
      <div class="nav-inner">
        <router-link to="/" class="nav-brand">
          <img src="@/assets/imgs/logo2.png" alt="" class="brand-icon" />
          <span class="brand-text">唐三彩文物系统</span>
        </router-link>
        <div class="nav-actions">
          <router-link to="/appreciation" class="nav-back">
            <el-icon><ArrowLeft /></el-icon>
            返回鉴赏
          </router-link>
        </div>
      </div>
    </header>

    <!-- 主体 -->
    <main class="detail-main">
      <!-- 英雄区：大幅文物图 + 基础信息 -->
      <section class="hero-section">
        <div class="hero-bg-pattern"></div>
        <div class="hero-grid">
          <!-- 左侧：大图 -->
          <div class="hero-image-wrap">
            <div class="hero-image-frame">
              <img
                v-if="artifact.image_url"
                :src="getImageUrl(artifact.image_url)"
                :alt="artifact.name"
                class="hero-image"
              />
              <div v-else class="hero-placeholder">
                <el-icon :size="72"><Collection /></el-icon>
                <span>暂无图片</span>
              </div>
            </div>
            <!-- 图片底部的年代标签 -->
            <div class="hero-era-badge">
              <span class="era-line"></span>
              <span class="era-text">{{ artifact.era }}</span>
              <span class="era-line"></span>
            </div>
          </div>

          <!-- 右侧：标题 + 核心信息 -->
          <div class="hero-info">
            <div class="hero-tags">
              <span class="hero-tag tag-era">{{ artifact.era }}</span>
              <span class="hero-tag tag-type">{{ artifact.type }}</span>
              <span class="hero-tag tag-level" v-if="artifact.level">{{ artifact.level }}</span>
              <button
                class="hero-fav-btn"
                :class="{ 'is-fav': favorited }"
                @click="toggleFavorite"
                :title="favorited ? '取消收藏' : '收藏'"
              >
                <el-icon :size="20"><StarFilled /></el-icon>
                <span>{{ favorited ? '已收藏' : '收藏' }}</span>
              </button>
            </div>
            <h1 class="hero-title">
              <span class="title-deco title-deco-left">「</span>
              {{ artifact.name }}
              <span class="title-deco title-deco-right">」</span>
            </h1>
            <p class="hero-museum" v-if="artifact.museum">
              <el-icon><OfficeBuilding /></el-icon>
              {{ artifact.museum }}
            </p>
            <div class="hero-divider"></div>
            <p class="hero-desc" v-if="artifact.description">
              {{ artifact.description }}
            </p>
            <p class="hero-desc hero-desc-empty" v-else>
              此文物暂无详细描述。唐三彩是中国唐代低温铅釉陶器的总称，以黄、绿、白三色为主，造型多样，工艺精湛，是盛唐气象的生动写照。
            </p>
          </div>
        </div>
      </section>

      <!-- 详情信息区 -->
      <section class="info-section">
        <div class="info-section-inner">
          <!-- 左侧竖排装饰 -->
          <div class="info-vertical-label">
            <div class="vertical-line"></div>
            <span class="vertical-text">文 物 档 案</span>
            <div class="vertical-line"></div>
          </div>

          <!-- 右侧信息卡片网格 -->
          <div class="info-cards">
            <div class="info-card" v-for="(field, idx) in infoFields" :key="field.key" :style="{ '--card-delay': idx * 0.08 + 's' }">
              <div class="card-icon">
                <el-icon :size="22"><component :is="field.icon" /></el-icon>
              </div>
              <div class="card-content">
                <span class="card-label">{{ field.label }}</span>
                <span class="card-value">{{ field.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 底部分隔 -->
      <div class="section-divider">
        <div class="divider-ornament">
          <span class="ornament-dot"></span>
          <span class="ornament-line"></span>
          <span class="ornament-diamond"></span>
          <span class="ornament-line"></span>
          <span class="ornament-dot"></span>
        </div>
      </div>

      <!-- 釉色与工艺区 -->
      <section class="craft-section" v-if="artifact.glaze || artifact.size">
        <div class="craft-inner">
          <div class="craft-card" v-if="artifact.glaze">
            <div class="craft-header">
              <span class="craft-num">01</span>
              <span class="craft-title">釉色工艺</span>
            </div>
            <div class="craft-glaze-display">
              <div class="glaze-swatch" v-for="color in glazeColors" :key="color.name" :style="{ background: color.hex }">
                <span class="swatch-label">{{ color.name }}</span>
              </div>
            </div>
            <p class="craft-desc">{{ artifact.glaze }}</p>
          </div>

          <div class="craft-card" v-if="artifact.size">
            <div class="craft-header">
              <span class="craft-num">02</span>
              <span class="craft-title">器物尺寸</span>
            </div>
            <div class="craft-size-display">
              <span class="size-value">{{ artifact.size }}</span>
            </div>
          </div>

          <div class="craft-card" v-if="artifact.source">
            <div class="craft-header">
              <span class="craft-num">03</span>
              <span class="craft-title">出土地点</span>
            </div>
            <div class="craft-source-display">
              <el-icon :size="20"><MapLocation /></el-icon>
              <span class="source-text">{{ artifact.source }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 底部导航 -->
      <div class="detail-footer-nav">
        <router-link to="/appreciation" class="footer-nav-link">
          <el-icon><ArrowLeft /></el-icon>
          返回文物鉴赏
        </router-link>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="detail-footer">
      <div class="footer-inner">
        <span>唐三彩文物数字化管理系统</span>
        <span class="footer-sep">|</span>
        <span>守护千年文明 · 传承文化瑰宝</span>
      </div>
    </footer>
  </div>

  <!-- 加载态 -->
  <div v-else-if="loading" class="detail-loading">
    <div class="loading-inner">
      <div class="loading-ring">
        <div class="ring-inner"></div>
      </div>
      <span class="loading-text">正在加载文物信息...</span>
    </div>
  </div>

  <!-- 错误态 -->
  <div v-else class="detail-error">
    <div class="error-inner">
      <el-icon :size="64"><WarningFilled /></el-icon>
      <h2>文物未找到</h2>
      <p>该文物可能已被移除或链接无效</p>
      <router-link to="/appreciation" class="error-back">返回文物鉴赏</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeft, Collection, OfficeBuilding, MapLocation,
  Clock, Box, GoldMedal, School, Document, WarningFilled, StarFilled
} from '@element-plus/icons-vue'
import request from '@/utils/request'
import { getImageUrl } from '@/utils/imageUrl'

const route = useRoute()

const artifact = ref(null)
const loading = ref(true)
const favorited = ref(false)

// 釉色色板映射
const glazeColors = computed(() => {
  const glaze = artifact.value?.glaze || ''
  const colorMap = {
    '黄': { name: '黄釉', hex: '#c9a84c' },
    '绿': { name: '绿釉', hex: '#5a8a4a' },
    '白': { name: '白釉', hex: '#f0ede0' },
    '褐': { name: '褐釉', hex: '#8b6914' },
    '蓝': { name: '蓝釉', hex: '#3a5f8a' },
    '赭': { name: '赭釉', hex: '#8b4513' },
    '黑': { name: '黑釉', hex: '#3a3530' },
    '红': { name: '红釉', hex: '#a04030' },
  }
  const colors = []
  for (const [char, info] of Object.entries(colorMap)) {
    if (glaze.includes(char)) colors.push(info)
  }
  // 如果没有匹配到，用默认三彩
  if (colors.length === 0) {
    return [
      { name: '黄釉', hex: '#c9a84c' },
      { name: '绿釉', hex: '#5a8a4a' },
      { name: '白釉', hex: '#f0ede0' },
    ]
  }
  return colors
})

// 信息字段列表
const infoFields = computed(() => {
  const a = artifact.value
  if (!a) return []
  const fields = [
    { key: 'era', label: '年代', value: a.era, icon: 'Clock' },
    { key: 'type', label: '器型', value: a.type, icon: 'Box' },
    { key: 'size', label: '尺寸', value: a.size, icon: 'GoldMedal' },
    { key: 'glaze', label: '釉色', value: a.glaze, icon: 'GoldMedal' },
    { key: 'level', label: '文物等级', value: a.level, icon: 'GoldMedal' },
    { key: 'source', label: '出土地', value: a.source, icon: 'MapLocation' },
    { key: 'museum', label: '馆藏机构', value: a.museum, icon: 'School' },
  ]
  return fields.filter(f => f.value)
})

const toggleFavorite = () => {
  request.post('/favorites/toggle', { artifact_id: artifact.value.id }).then(res => {
    if (res.code === '200') {
      favorited.value = res.data.favorited
    }
  }).catch(() => {})
}

const loadData = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await request.get(`/artifacts/selectById/${id}`)
    if (res.code === '200') {
      artifact.value = res.data
      request.get(`/favorites/list`).then(favRes => {
        if (favRes.code === '200') {
          favorited.value = (favRes.data || []).includes(Number(id))
        }
      }).catch(() => {})
    }
  } catch (e) {
    // artifact stays null → error state
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700;900&display=swap');

.detail-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  background: linear-gradient(180deg, #1a1510 0%, #241e17 30%, #1e1913 100%);
  min-height: 100vh;
  color: #e8dcc8;
}

/* ========== 导航 ========== */
.detail-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(26, 21, 16, 0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(201, 168, 76, 0.12);
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
  border: 1px solid rgba(201, 168, 76, 0.35);
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-back:hover {
  background: rgba(201, 168, 76, 0.1);
  border-color: #c9a84c;
}

/* ========== 主体 ========== */
.detail-main {
  padding-top: 64px;
}

/* ========== 英雄区 ========== */
.hero-section {
  position: relative;
  padding: 60px 40px 80px;
  overflow: hidden;
}

.hero-bg-pattern {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(ellipse at 25% 30%, rgba(201, 168, 76, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse at 75% 60%, rgba(201, 168, 76, 0.04) 0%, transparent 50%);
  pointer-events: none;
}

.hero-grid {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

/* 左侧大图 */
.hero-image-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.hero-image-frame {
  position: relative;
  aspect-ratio: 1 / 1;
  background: linear-gradient(145deg, #2a231a 0%, #1e1913 100%);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(201, 168, 76, 0.2);
  box-shadow:
    0 24px 60px rgba(0, 0, 0, 0.5),
    inset 0 0 80px rgba(201, 168, 76, 0.03);
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.hero-image-frame:hover .hero-image {
  transform: scale(1.04);
}

.hero-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: rgba(201, 168, 76, 0.3);
}

.hero-placeholder span {
  font-size: 14px;
  letter-spacing: 2px;
}

.hero-era-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.era-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 168, 76, 0.4), transparent);
}

.era-text {
  font-size: 14px;
  color: #c9a84c;
  letter-spacing: 4px;
  font-weight: 500;
}

/* 右侧信息 */
.hero-info {
  animation: fadeSlideUp 0.8s 0.15s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.hero-tags {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.hero-tag {
  font-size: 12px;
  padding: 4px 14px;
  border-radius: 3px;
  letter-spacing: 1.5px;
}

.tag-era {
  color: #c9a84c;
  background: rgba(201, 168, 76, 0.1);
  border: 1px solid rgba(201, 168, 76, 0.2);
}

.tag-type {
  color: #a09080;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.tag-level {
  color: #e8dcc8;
  background: rgba(201, 168, 76, 0.12);
  border: 1px solid rgba(201, 168, 76, 0.3);
}

.hero-fav-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 16px;
  font-size: 13px;
  color: #a09080;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  cursor: pointer;
  font-family: 'Noto Serif SC', 'SimSun', serif;
  letter-spacing: 1px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.hero-fav-btn:hover {
  color: #c9a84c;
  border-color: rgba(201, 168, 76, 0.4);
  background: rgba(201, 168, 76, 0.08);
}

.hero-fav-btn.is-fav {
  color: #c9a84c;
  border-color: rgba(201, 168, 76, 0.4);
  background: rgba(201, 168, 76, 0.12);
}

.hero-title {
  font-size: 40px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 4px;
  margin: 0 0 16px;
  line-height: 1.3;
}

.title-deco {
  color: #c9a84c;
  font-weight: 300;
  opacity: 0.5;
}

.title-deco-left {
  margin-right: 4px;
}

.title-deco-right {
  margin-left: 4px;
}

.hero-museum {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: #8b7355;
  margin: 0 0 24px;
  letter-spacing: 1px;
}

.hero-divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, rgba(201, 168, 76, 0.4), transparent 70%);
  margin-bottom: 24px;
}

.hero-desc {
  font-size: 15px;
  color: rgba(232, 220, 200, 0.6);
  line-height: 2;
  letter-spacing: 0.5px;
  margin: 0;
}

.hero-desc-empty {
  font-style: italic;
  opacity: 0.4;
}

/* ========== 详情信息区 ========== */
.info-section {
  padding: 0 40px 60px;
}

.info-section-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

/* 左侧竖排装饰 */
.info-vertical-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding-top: 12px;
  flex-shrink: 0;
}

.vertical-line {
  width: 1px;
  height: 60px;
  background: linear-gradient(180deg, transparent, rgba(201, 168, 76, 0.3), transparent);
}

.vertical-text {
  writing-mode: vertical-rl;
  font-size: 14px;
  color: #8b7355;
  letter-spacing: 6px;
  font-weight: 500;
}

/* 信息卡片网格 */
.info-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  flex: 1;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 22px 20px;
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  opacity: 0;
  animation: fadeSlideUp 0.5s var(--card-delay) cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.info-card:hover {
  background: rgba(201, 168, 76, 0.06);
  border-color: rgba(201, 168, 76, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background: rgba(201, 168, 76, 0.08);
  border: 1px solid rgba(201, 168, 76, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c9a84c;
  flex-shrink: 0;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.card-label {
  font-size: 11px;
  color: #6b5d4d;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.card-value {
  font-size: 15px;
  color: #e8dcc8;
  font-weight: 500;
  letter-spacing: 0.5px;
  word-break: break-all;
}

/* ========== 分隔线 ========== */
.section-divider {
  padding: 0 40px 40px;
}

.divider-ornament {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
}

.ornament-dot {
  width: 5px;
  height: 5px;
  background: #c9a84c;
  border-radius: 50%;
  opacity: 0.4;
}

.ornament-line {
  width: 80px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 168, 76, 0.25), transparent);
}

.ornament-diamond {
  width: 8px;
  height: 8px;
  background: #c9a84c;
  transform: rotate(45deg);
  opacity: 0.5;
}

/* ========== 釉色与工艺区 ========== */
.craft-section {
  padding: 0 40px 60px;
}

.craft-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.craft-card {
  padding: 28px 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  transition: all 0.3s;
}

.craft-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(201, 168, 76, 0.15);
}

.craft-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 20px;
}

.craft-num {
  font-size: 20px;
  font-weight: 700;
  color: #c9a84c;
  opacity: 0.5;
  font-family: 'Georgia', serif;
}

.craft-title {
  font-size: 16px;
  font-weight: 600;
  color: #e8dcc8;
  letter-spacing: 2px;
}

.craft-desc {
  margin: 16px 0 0;
  font-size: 14px;
  color: rgba(232, 220, 200, 0.5);
  line-height: 1.7;
  letter-spacing: 0.5px;
}

/* 釉色色板 */
.craft-glaze-display {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.glaze-swatch {
  flex: 1;
  min-width: 70px;
  aspect-ratio: 1.4 / 1;
  border-radius: 6px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2);
}

.swatch-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.85);
  letter-spacing: 1px;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
}

/* 尺寸展示 */
.craft-size-display {
  text-align: center;
  padding: 20px 0;
}

.size-value {
  font-size: 28px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 2px;
}

/* 出土地展示 */
.craft-source-display {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 0;
  color: #8b7355;
}

.source-text {
  font-size: 15px;
  color: #e8dcc8;
  letter-spacing: 1px;
}

/* 空状态占位 */
.craft-card:only-child {
  grid-column: 1 / -1;
}

/* ========== 底部导航 ========== */
.detail-footer-nav {
  display: flex;
  justify-content: center;
  padding: 0 40px 60px;
}

.footer-nav-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #c9a84c;
  text-decoration: none;
  font-size: 15px;
  letter-spacing: 2px;
  padding: 12px 32px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 4px;
  transition: all 0.3s;
}

.footer-nav-link:hover {
  background: rgba(201, 168, 76, 0.1);
  border-color: #c9a84c;
}

/* ========== 页脚 ========== */
.detail-footer {
  background: #14100c;
  padding: 24px 40px;
  text-align: center;
}

.footer-inner {
  color: rgba(232, 220, 200, 0.2);
  font-size: 12px;
  letter-spacing: 1px;
}

.footer-sep {
  margin: 0 10px;
}

/* ========== 加载态 ========== */
.detail-loading {
  min-height: 100vh;
  background: #1a1510;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.loading-ring {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid rgba(201, 168, 76, 0.15);
  border-top-color: #c9a84c;
  animation: spin 1s linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ring-inner {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid rgba(201, 168, 76, 0.1);
  border-bottom-color: #c9a84c;
  animation: spin 1.5s linear infinite reverse;
}

.loading-text {
  font-size: 14px;
  color: rgba(232, 220, 200, 0.4);
  letter-spacing: 2px;
  font-family: 'Noto Serif SC', 'SimSun', serif;
}

/* ========== 错误态 ========== */
.detail-error {
  min-height: 100vh;
  background: #1a1510;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-inner {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #8b7355;
}

.error-inner h2 {
  font-size: 24px;
  color: #e8dcc8;
  font-weight: 600;
  letter-spacing: 2px;
  margin: 0;
}

.error-inner p {
  font-size: 14px;
  margin: 0 0 8px;
  opacity: 0.6;
}

.error-back {
  display: inline-block;
  color: #c9a84c;
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 1px;
  padding: 10px 28px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 4px;
  transition: all 0.3s;
}

.error-back:hover {
  background: rgba(201, 168, 76, 0.1);
  border-color: #c9a84c;
}

/* ========== 动画 ========== */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========== 响应式 ========== */
@media (max-width: 1100px) {
  .hero-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-image-frame {
    max-width: 500px;
    margin: 0 auto;
  }

  .info-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .craft-inner {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .detail-nav {
    padding: 0 20px;
  }

  .hero-section {
    padding: 40px 20px 50px;
  }

  .hero-title {
    font-size: 28px;
    letter-spacing: 2px;
  }

  .info-section {
    padding: 0 20px 40px;
  }

  .info-section-inner {
    flex-direction: column;
  }

  .info-vertical-label {
    flex-direction: row;
    gap: 12px;
    padding-top: 0;
  }

  .vertical-line {
    width: 40px;
    height: 1px;
  }

  .vertical-text {
    writing-mode: horizontal-tb;
    font-size: 12px;
    letter-spacing: 4px;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .craft-section {
    padding: 0 20px 40px;
  }

  .craft-inner {
    grid-template-columns: 1fr;
  }

  .detail-footer-nav {
    padding: 0 20px 40px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 30px 16px 40px;
  }

  .hero-title {
    font-size: 24px;
  }

  .hero-tags {
    gap: 6px;
  }

  .hero-tag {
    font-size: 11px;
    padding: 3px 10px;
  }
}
</style>