<template>
  <section id="about" class="about-section">
    <div class="about-content">
      <div class="about-left">
        <div class="section-badge">
          <span class="badge-dot"></span>
          <span>关于系统</span>
        </div>
        <h2 class="section-title">守护千年文明<br>传承文化瑰宝</h2>
        <p class="about-desc">
          唐三彩文物数字化管理系统，致力于以现代信息技术守护和传承唐代三彩文化遗产。
          系统收录了来自全国各地的唐三彩文物信息，涵盖初唐、盛唐、中唐、晚唐四个历史时期，
          为文物研究、教育普及和文化传播提供数字化支撑。
        </p>
        <div class="about-features">
          <div class="about-feature">
            <div class="feature-icon">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="feature-text">
              <span class="feature-title">文物管理</span>
              <span class="feature-desc">数字化档案管理</span>
            </div>
          </div>
          <div class="about-feature">
            <div class="feature-icon">
              <el-icon><MapLocation /></el-icon>
            </div>
            <div class="feature-text">
              <span class="feature-title">地理分布</span>
              <span class="feature-desc">可视化出土地图</span>
            </div>
          </div>
          <div class="about-feature">
            <div class="feature-icon">
              <el-icon><Timer /></el-icon>
            </div>
            <div class="feature-text">
              <span class="feature-title">年代演变</span>
              <span class="feature-desc">时间线展示</span>
            </div>
          </div>
        </div>
      </div>
      <div class="about-right">
        <div class="about-image">
          <div class="image-frame">
            <div class="frame-corner tl"></div>
            <div class="frame-corner tr"></div>
            <div class="frame-corner bl"></div>
            <div class="frame-corner br"></div>
            <div class="image-placeholder">
              <el-icon :size="48"><Collection /></el-icon>
              <span>唐三彩 · 盛世华章</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Collection, MapLocation, Timer } from '@element-plus/icons-vue'
</script>

<style scoped>
/* ========== 通用 Section 样式 ========== */
.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #c9a84c;
  font-size: 13px;
  letter-spacing: 3px;
  margin-bottom: 16px;
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: #c9a84c;
  border-radius: 50%;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 4px;
  margin-bottom: 12px;
}

/* ========== 关于 ========== */
.about-section {
  padding: 100px 40px;
  background: linear-gradient(135deg, #f5f0e8 0%, #ede5d8 100%);
}

.about-content {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 64px;
  align-items: center;
}

.about-left .section-title {
  font-size: 30px;
  line-height: 1.4;
  margin-bottom: 20px;
}

.about-desc {
  font-size: 15px;
  color: #6b5d4d;
  line-height: 1.9;
  margin: 0 0 28px;
}

.about-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.about-feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  padding: 20px 12px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e8e0d4;
  transition: all 0.3s ease;
}

.about-feature:hover {
  border-color: #c9a84c;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.feature-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #c9a84c, #a08040);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  flex-shrink: 0;
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.feature-title {
  font-size: 14px;
  font-weight: 600;
  color: #4a3f35;
  letter-spacing: 1px;
}

.feature-desc {
  font-size: 11px;
  color: #8b7355;
}

.about-image {
  display: flex;
  justify-content: center;
}

.image-frame {
  position: relative;
  width: 360px;
  height: 360px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e8e0d4;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.06);
}

.frame-corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border-color: #c9a84c;
  border-style: solid;
}

.frame-corner.tl {
  top: 12px;
  left: 12px;
  border-width: 2px 0 0 2px;
}

.frame-corner.tr {
  top: 12px;
  right: 12px;
  border-width: 2px 2px 0 0;
}

.frame-corner.bl {
  bottom: 12px;
  left: 12px;
  border-width: 0 0 2px 2px;
}

.frame-corner.br {
  bottom: 12px;
  right: 12px;
  border-width: 0 2px 2px 0;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #c9a84c;
}

.image-placeholder span {
  font-size: 14px;
  letter-spacing: 2px;
  color: #8b7355;
}
</style>