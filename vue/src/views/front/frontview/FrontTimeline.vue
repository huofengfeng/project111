<template>
  <section id="timeline" class="timeline-section">
    <div class="section-header light">
      <div class="section-badge">
        <span class="badge-dot"></span>
        <span>历史长河</span>
      </div>
      <h2 class="section-title">年代演变</h2>
      <p class="section-desc">从初唐到晚唐，见证唐三彩艺术的兴衰与传承</p>
    </div>
    <div class="timeline-track">
      <div class="timeline-line"></div>
      <div
        v-for="(period, index) in periods"
        :key="period.name"
        class="timeline-node"
        :class="{ 'node-left': index % 2 === 0, 'node-right': index % 2 === 1 }"
        :style="{ '--delay': index * 0.2 + 's' }"
      >
        <div class="node-connector"></div>
        <div class="node-dot"></div>
        <div class="node-card">
          <div class="node-header">
            <span class="node-year">{{ period.year }}</span>
            <span class="node-event-tag">{{ period.event }}</span>
          </div>
          <h3 class="node-name">{{ period.name }}</h3>
          <p class="node-desc">{{ period.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const periods = [
  {
    name: '初唐',
    year: '618-712',
    description: '唐三彩开始出现，造型相对简单，釉色以黄、绿为主。',
    event: '唐朝建立',
  },
  {
    name: '盛唐',
    year: '713-766',
    description: '唐三彩鼎盛期，造型丰富多样，釉色鲜艳，人物俑和动物俑大量出现。',
    event: '开元盛世',
  },
  {
    name: '中唐',
    year: '766-835',
    description: '风格趋于写实，器型更加规整，部分出现绞胎工艺。',
    event: '安史之乱后',
  },
  {
    name: '晚唐',
    year: '836-907',
    description: '唐三彩逐渐衰落，产量减少，风格趋于简化。',
    event: '藩镇割据',
  },
]
</script>

<style scoped>
/* ========== 通用 Section 样式 ========== */
.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header.light .section-title,
.section-header.light .section-desc {
  color: #e8dcc8;
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

/* ========== 年代演变 ========== */
.timeline-section {
  padding: 100px 40px;
  background: linear-gradient(180deg, #2c241b 0%, #1a1510 100%);
}

.timeline-track {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  padding: 20px 0;
}

.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, transparent, rgba(201, 168, 76, 0.25), rgba(201, 168, 76, 0.25), transparent);
  transform: translateX(-50%);
}

.timeline-node {
  display: flex;
  align-items: center;
  margin-bottom: 48px;
  position: relative;
  opacity: 0;
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: var(--delay);
}

.timeline-node:last-child {
  margin-bottom: 0;
}

.node-left {
  flex-direction: row;
}

.node-left .node-card {
  margin-right: 48px;
  text-align: right;
}

.node-left .node-connector {
  right: 50%;
  margin-right: 7px;
}

.node-right {
  flex-direction: row-reverse;
}

.node-right .node-card {
  margin-left: 48px;
  text-align: left;
}

.node-right .node-connector {
  left: 50%;
  margin-left: 7px;
}

.node-connector {
  position: absolute;
  top: 50%;
  width: 48px;
  height: 1px;
  background: rgba(201, 168, 76, 0.25);
  transform: translateY(-50%);
}

.node-dot {
  width: 16px;
  height: 16px;
  background: #c9a84c;
  border-radius: 50%;
  border: 3px solid #2c241b;
  box-shadow: 0 0 0 4px rgba(201, 168, 76, 0.15);
  flex-shrink: 0;
  z-index: 2;
  transition: all 0.3s ease;
}

.timeline-node:hover .node-dot {
  transform: scale(1.3);
  box-shadow: 0 0 0 6px rgba(201, 168, 76, 0.25);
}

.node-card {
  flex: 1;
  max-width: 360px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(201, 168, 76, 0.1);
  border-radius: 8px;
  padding: 20px 24px;
  transition: all 0.3s ease;
}

.node-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(201, 168, 76, 0.2);
}

.node-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.node-left .node-header {
  justify-content: flex-end;
}

.node-year {
  font-size: 13px;
  color: #c9a84c;
  letter-spacing: 1px;
  font-weight: 600;
}

.node-event-tag {
  font-size: 11px;
  color: rgba(232, 220, 200, 0.5);
  padding: 2px 8px;
  border: 1px solid rgba(201, 168, 76, 0.2);
  border-radius: 12px;
  letter-spacing: 1px;
}

.node-name {
  font-size: 22px;
  font-weight: 700;
  color: #e8dcc8;
  margin: 0 0 10px;
  letter-spacing: 2px;
}

.node-desc {
  font-size: 13px;
  color: rgba(232, 220, 200, 0.4);
  line-height: 1.8;
  margin: 0;
}

/* ========== 动画 ========== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .node-left .node-header,
  .node-right .node-header {
    justify-content: center;
  }

  .timeline-node {
    flex-direction: column !important;
    text-align: center !important;
  }

  .timeline-node .node-card {
    margin: 20px 0 0 !important;
    text-align: center !important;
  }

  .timeline-line {
    display: none;
  }
}
</style>