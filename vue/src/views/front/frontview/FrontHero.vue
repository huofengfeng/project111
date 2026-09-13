<template>
  <section id="hero" class="hero-section">
    <!-- 轮播图背景 -->
    <div class="carousel-container">
      <div
        v-for="(slide, index) in carouselSlides"
        :key="index"
        class="carousel-slide"
        :class="{ active: currentSlide === index, prev: currentSlide === (index + 1) % carouselSlides.length }"
      >
        <img :src="slide.image" :alt="slide.title" class="carousel-image">
        <div class="carousel-overlay"></div>
      </div>
      <!-- 轮播指示器 -->
      <div class="carousel-indicators">
        <button
          v-for="(_, index) in carouselSlides"
          :key="index"
          class="indicator-dot"
          :class="{ active: currentSlide === index }"
          @click="goToSlide(index)"
        ></button>
      </div>
      <!-- 轮播箭头 -->
      <button class="carousel-arrow carousel-prev" @click="prevSlide">
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <button class="carousel-arrow carousel-next" @click="nextSlide">
        <el-icon><ArrowRight /></el-icon>
      </button>
    </div>

    <!-- Hero 内容 -->
    <div class="hero-content">
      <div class="hero-badge">
        <span class="badge-line"></span>
        <span class="badge-text">唐代 · 盛世华章</span>
        <span class="badge-line"></span>
      </div>
      <h1 class="hero-title">
        <span class="title-main">唐三彩</span>
        <span class="title-sub">文物数字化管理系统</span>
      </h1>
      <div class="hero-intro-wrap">
        <p class="hero-intro-lead">穿越千年时光，探寻盛唐气象。以数字化之力，守护华夏文明的璀璨瑰宝。</p>
        <div class="hero-intro-body">
          <p>唐三彩，全称"唐代三彩釉陶器"，盛行于唐代的低温铅釉陶器。以黄、绿、白三色为主釉，辅以褐、蓝、黑等色，在窑火中自然流淌交融，形成独一无二的斑斓效果。</p>
          <p>其采用二次烧成工艺，先以高岭土塑型经千度素烧，再施含铅釉料于八百度低温釉烧。铅釉流动性强，各色自然晕散浸润，形成"窑变"之妙，每件皆是孤品。</p>
          <p>题材包罗万象：武士俑、仕女俑、骏马、骆驼，生动再现盛唐风貌，更是研究唐代政治、经济、文化的珍贵实物资料。</p>
        </div>
      </div>
    </div>
    <div class="hero-scroll-hint">
      <div class="scroll-mouse">
        <div class="scroll-wheel"></div>
      </div>
      <span>向下探索</span>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const currentSlide = ref(0)
const carouselSlides = [
  {
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=A+stunning+Tang+Dynasty+sancai+glazed+pottery+camel+figurine+in+a+museum+display+case%2C+warm+amber+lighting%2C+deep+brown+and+gold+tones%2C+professional+photography%2C+shallow+depth+of+field%2C+ancient+Chinese+artifact&image_size=landscape_16_9',
    title: '三彩骆驼俑',
  },
  {
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Tang+Dynasty+sancai+glazed+horse+statue+with+rider%2C+intricate+details%2C+museum+setting%2C+warm+golden+lighting%2C+terracotta+and+green+glazes%2C+professional+archaeological+photography&image_size=landscape_16_9',
    title: '三彩骑马俑',
  },
  {
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Collection+of+Tang+Dynasty+sancai+pottery+figurines+arranged+on+display%2C+warriors+and+court+ladies%2C+rich+amber+and+jade+green+glazes%2C+dramatic+museum+spotlighting%2C+ancient+Chinese+art&image_size=landscape_16_9',
    title: '三彩人物俑群',
  },
  {
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=Close-up+of+Tang+sancai+glazed+pottery+surface+texture%2C+flowing+glaze+drips+in+amber+green+and+cream%2C+macro+photography%2C+warm+lighting%2C+ancient+ceramic+art+detail&image_size=landscape_16_9',
    title: '三彩釉色之美',
  },
]

let carouselTimer = null
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % carouselSlides.length
}
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + carouselSlides.length) % carouselSlides.length
}
const goToSlide = (index) => {
  currentSlide.value = index
  resetCarouselTimer()
}
const resetCarouselTimer = () => {
  if (carouselTimer) clearInterval(carouselTimer)
  carouselTimer = setInterval(nextSlide, 5000)
}

onMounted(() => {
  resetCarouselTimer()
})

onUnmounted(() => {
  if (carouselTimer) clearInterval(carouselTimer)
})
</script>

<style scoped>
/* ========== Hero 轮播图区域 ========== */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 轮播图容器 */
.carousel-container {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.carousel-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.carousel-slide.active {
  opacity: 1;
  z-index: 2;
}

.carousel-slide.prev {
  opacity: 0;
  z-index: 1;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
  transition: transform 6s ease;
}

.carousel-slide.active .carousel-image {
  transform: scale(1);
}

.carousel-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(26, 21, 16, 0.4) 0%,
    rgba(26, 21, 16, 0.2) 40%,
    rgba(26, 21, 16, 0.5) 70%,
    rgba(26, 21, 16, 0.85) 100%
  );
}

/* 轮播指示器 */
.carousel-indicators {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 10;
}

.indicator-dot {
  width: 40px;
  height: 3px;
  background: rgba(232, 220, 200, 0.3);
  border: none;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.indicator-dot::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 0;
  background: #c9a84c;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.indicator-dot.active {
  background: rgba(201, 168, 76, 0.3);
}

.indicator-dot.active::after {
  width: 100%;
  animation: indicatorProgress 5s linear forwards;
}

@keyframes indicatorProgress {
  from { width: 0; }
  to { width: 100%; }
}

.indicator-dot:hover {
  background: rgba(232, 220, 200, 0.5);
}

/* 轮播箭头 */
.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  background: rgba(26, 21, 16, 0.4);
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 50%;
  color: #c9a84c;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
  font-size: 18px;
}

.carousel-arrow:hover {
  background: rgba(201, 168, 76, 0.2);
  border-color: #c9a84c;
  transform: translateY(-50%) scale(1.1);
}

.carousel-prev {
  left: 40px;
}

.carousel-next {
  right: 40px;
}

/* Hero 内容层 */
.hero-content {
  position: relative;
  z-index: 5;
  text-align: center;
  max-width: 800px;
  padding: 0 24px;
}

.hero-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
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
  text-transform: uppercase;
}

.hero-title {
  margin-bottom: 24px;
}

.title-main {
  display: block;
  font-size: 72px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 12px;
  line-height: 1.2;
  text-shadow: 0 4px 30px rgba(201, 168, 76, 0.2);
}

.title-sub {
  display: block;
  font-size: 20px;
  font-weight: 400;
  color: rgba(232, 220, 200, 0.6);
  letter-spacing: 6px;
  margin-top: 12px;
}

.hero-intro-wrap {
  max-width: 680px;
  margin: 0 auto;
}

.hero-intro-lead {
  font-size: 17px;
  color: rgba(232, 220, 200, 0.7);
  line-height: 1.8;
  margin-bottom: 24px;
  letter-spacing: 1px;
  text-align: center;
}

.hero-intro-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero-intro-body p {
  font-size: 14px;
  color: rgba(232, 220, 200, 0.5);
  line-height: 1.9;
  margin: 0;
  text-align: justify;
  text-align-last: center;
}

.hero-scroll-hint {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(232, 220, 200, 0.3);
  font-size: 12px;
  letter-spacing: 2px;
}

.scroll-mouse {
  width: 22px;
  height: 34px;
  border: 1px solid rgba(232, 220, 200, 0.3);
  border-radius: 11px;
  display: flex;
  justify-content: center;
  padding-top: 6px;
}

.scroll-wheel {
  width: 2px;
  height: 6px;
  background: rgba(232, 220, 200, 0.4);
  border-radius: 1px;
  animation: scrollWheel 2s infinite;
}

@keyframes scrollWheel {
  0%, 100% { transform: translateY(0); opacity: 1; }
  50% { transform: translateY(8px); opacity: 0.3; }
}
</style>