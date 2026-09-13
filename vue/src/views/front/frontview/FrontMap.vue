<template>
  <!-- 出土分布 -->
  <section id="map" class="map-section">
    <div class="section-header">
      <div class="section-badge">
        <span class="badge-dot"></span>
        <span>地理脉络</span>
      </div>
      <h2 class="section-title">出土分布</h2>
      <p class="section-desc">探寻唐三彩的出土地点，追溯千年前的文明足迹</p>
    </div>
    <div class="map-container">
      <div class="map-visual">
        <div class="map-china">
          <div class="map-province" v-for="prov in provinces" :key="prov.name" :style="prov.style">
            <div class="province-dot" :class="{ 'dot-large': prov.count > 5 }"></div>
            <span class="province-name">{{ prov.name }}</span>
            <span class="province-count">{{ prov.count }}处</span>
          </div>
        </div>
      </div>
      <div class="map-info">
        <h3 class="map-info-title">主要出土地</h3>
        <div class="map-info-list">
          <div class="map-info-item" v-for="loc in topLocations" :key="loc.name">
            <span class="info-rank">{{ loc.rank }}</span>
            <span class="info-name">{{ loc.name }}</span>
            <div class="info-bar">
              <div class="info-bar-fill" :style="{ width: loc.percent + '%' }"></div>
            </div>
            <span class="info-count">{{ loc.count }}处</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const provinces = [
  { name: '洛阳', count: 12, style: { left: '52%', top: '45%' } },
  { name: '西安', count: 8, style: { left: '46%', top: '42%' } },
  { name: '乾县', count: 5, style: { left: '44%', top: '40%' } },
  { name: '巩义', count: 4, style: { left: '54%', top: '44%' } },
  { name: '扬州', count: 3, style: { left: '62%', top: '52%' } },
  { name: '太原', count: 2, style: { left: '50%', top: '35%' } },
]

const topLocations = [
  { rank: '01', name: '洛阳', count: 12, percent: 100 },
  { rank: '02', name: '西安', count: 8, percent: 67 },
  { rank: '03', name: '乾县', count: 5, percent: 42 },
  { rank: '04', name: '巩义', count: 4, percent: 33 },
  { rank: '05', name: '扬州', count: 3, percent: 25 },
]
</script>

<style scoped>
/* ========== 通用 Section 样式 ========== */
.section-header {
  text-align: center;
  margin-bottom: 60px;
}

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

.section-desc {
  font-size: 15px;
  color: #8b7355;
  letter-spacing: 1px;
}

/* ========== 出土分布 ========== */
.map-section {
  padding: 100px 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.map-container {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 32px;
  align-items: stretch;
}

.map-visual {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e8e0d4;
  padding: 32px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.map-visual::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #c9a84c, #a08040, #c9a84c);
  border-radius: 12px 12px 0 0;
}

.map-china {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 320px;
  background: linear-gradient(135deg, #f5f0e8 0%, #ede5d8 100%);
  border-radius: 8px;
  overflow: hidden;
}

.map-province {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.map-province:hover {
  transform: scale(1.15);
  z-index: 10;
}

.province-dot {
  width: 10px;
  height: 10px;
  background: #c9a84c;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.2);
  transition: all 0.3s ease;
}

.map-province:hover .province-dot {
  box-shadow: 0 0 0 5px rgba(201, 168, 76, 0.3);
}

.province-dot.dot-large {
  width: 14px;
  height: 14px;
}

.province-name {
  font-size: 11px;
  color: #4a3f35;
  font-weight: 600;
  letter-spacing: 1px;
  background: rgba(255, 255, 255, 0.8);
  padding: 1px 6px;
  border-radius: 4px;
}

.province-count {
  font-size: 10px;
  color: #8b7355;
  background: rgba(255, 255, 255, 0.6);
  padding: 0 4px;
  border-radius: 3px;
}

.map-info {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e8e0d4;
  padding: 28px;
  display: flex;
  flex-direction: column;
}

.map-info::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #c9a84c, #a08040, #c9a84c);
  border-radius: 12px 12px 0 0;
}

.map-info-title {
  font-size: 16px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 20px;
  letter-spacing: 1px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e8e0d4;
  display: flex;
  align-items: center;
  gap: 8px;
}

.map-info-title::before {
  content: '';
  width: 4px;
  height: 16px;
  background: linear-gradient(180deg, #c9a84c, #a08040);
  border-radius: 2px;
}

.map-info-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.map-info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f5f0e8;
}

.map-info-item:last-child {
  border-bottom: none;
}

.info-rank {
  width: 26px;
  font-size: 11px;
  font-weight: 700;
  color: #c9a84c;
  text-align: center;
  font-family: 'Georgia', serif;
}

.info-name {
  width: 50px;
  font-size: 13px;
  color: #4a3f35;
  font-weight: 500;
}

.info-bar {
  flex: 1;
  height: 5px;
  background: #f0ebe3;
  border-radius: 3px;
  overflow: hidden;
}

.info-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #c9a84c, #a08040);
  border-radius: 3px;
  transition: width 1s ease;
}

.info-count {
  width: 42px;
  font-size: 11px;
  color: #8b7355;
  text-align: right;
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .map-container {
    grid-template-columns: 1fr;
  }
}
</style>