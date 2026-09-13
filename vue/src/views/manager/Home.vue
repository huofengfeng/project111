<template>
  <div class="home-page">
    <!-- 欢迎语 -->
    <div class="welcome-section">
      <h1 class="welcome-title">
        欢迎回来，<span class="name">{{ data.user.name }}</span>
      </h1>
      <p class="welcome-desc">唐三彩文物数字化管理系统 — 守护千年文明，传承文化瑰宝</p>
    </div>

    <!-- 数据概览卡片 -->
    <div class="stats-grid">
      <div class="stat-card" @click="goTo('/manager/artifact')">
        <div class="stat-icon artifact">
          <el-icon :size="28"><Collection /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.artifactCount }}</div>
          <div class="stat-label">文物总数</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+12%</span>
          <span class="trend-label">较上月</span>
        </div>
      </div>

      <div class="stat-card" @click="goTo('/manager/tombsMap')">
        <div class="stat-icon location">
          <el-icon :size="28"><MapLocation /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.tombCount }}</div>
          <div class="stat-label">出土地点</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+5%</span>
          <span class="trend-label">较上月</span>
        </div>
      </div>

      <div class="stat-card" @click="goTo('/manager/timeline')">
        <div class="stat-icon period">
          <el-icon :size="28"><Timer /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.periodCount }}</div>
          <div class="stat-label">历史时期</div>
        </div>
        <div class="stat-trend">
          <span class="trend-stable">—</span>
          <span class="trend-label">持续更新</span>
        </div>
      </div>

      <div class="stat-card" @click="goTo('/manager/admin')">
        <div class="stat-icon admin">
          <el-icon :size="28"><User /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.adminCount }}</div>
          <div class="stat-label">管理员</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+1</span>
          <span class="trend-label">新增</span>
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="quick-section">
      <h3 class="section-title">快捷入口</h3>
      <div class="quick-grid">
        <div class="quick-item" @click="goTo('/manager/artifact')">
          <div class="quick-icon">
            <el-icon :size="22"><Collection /></el-icon>
          </div>
          <span>文物信息</span>
        </div>
        <div class="quick-item" @click="goTo('/manager/tombsMap')">
          <div class="quick-icon">
            <el-icon :size="22"><MapLocation /></el-icon>
          </div>
          <span>出土分布</span>
        </div>
        <div class="quick-item" @click="goTo('/manager/timeline')">
          <div class="quick-icon">
            <el-icon :size="22"><Timer /></el-icon>
          </div>
          <span>年代演变</span>
        </div>
        <div class="quick-item" @click="goTo('/manager/admin')">
          <div class="quick-icon">
            <el-icon :size="22"><User /></el-icon>
          </div>
          <span>管理员</span>
        </div>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="home-footer">
      <span>唐三彩文物数字化管理系统 v1.0</span>
      <span class="footer-sep">|</span>
      <span>数据最后更新：{{ currentDate }}</span>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import router from "@/router";
import request from "@/utils/request";
import { Collection, MapLocation, Timer, User } from "@element-plus/icons-vue";

const data = reactive({
  user: JSON.parse(sessionStorage.getItem('system-user') || '{}'),
});

const stats = reactive({
  artifactCount: 0,
  tombCount: 0,
  periodCount: 4,
  adminCount: 0,
});

const currentDate = ref('');

function goTo(path) {
  router.push(path);
}

onMounted(async () => {
  // 当前日期
  const now = new Date();
  currentDate.value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  // 加载统计数据
  try {
    // 文物总数
    const artRes = await request.get('/artifacts/selectPage', { params: { pageNum: 1, pageSize: 1 } });
    if (artRes.code === '200') {
      stats.artifactCount = artRes.data?.total || 0;
    }
  } catch (e) { /* ignore */ }

  try {
    // 出土地点数
    const tombRes = await request.get('/tombs/map/locations');
    if (tombRes.code === '200') {
      const locations = new Set((tombRes.data || []).map(t => t.location));
      stats.tombCount = locations.size;
    }
  } catch (e) { /* ignore */ }

  try {
    // 管理员数
    const adminRes = await request.get('/admin/selectAll');
    if (adminRes.code === '200') {
      stats.adminCount = (adminRes.data || []).length;
    }
  } catch (e) { /* ignore */ }
});
</script>

<style scoped>
.home-page {
  max-width: 1200px;
}

/* 欢迎语 */
.welcome-section {
  margin-bottom: 28px;
}

.welcome-title {
  font-size: 24px;
  font-weight: 700;
  color: #4a3f35;
  margin: 0 0 6px;
  letter-spacing: 1px;
}

.welcome-title .name {
  color: #c4823e;
}

.welcome-desc {
  font-size: 14px;
  color: #8b7355;
  margin: 0;
  letter-spacing: 0.5px;
}

/* 数据概览卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  border: 1px solid #ede5d8;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  border-radius: 12px 12px 0 0;
  opacity: 0;
  transition: opacity 0.25s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: #e0d5c5;
}

.stat-card:hover::after {
  opacity: 1;
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
}

.stat-icon.artifact {
  background: linear-gradient(135deg, #c4823e, #a0602d);
}

.stat-icon.artifact::after {
  background: linear-gradient(90deg, #c4823e, #a0602d);
}

.stat-icon.location {
  background: linear-gradient(135deg, #3a8f7b, #2d6b5c);
}

.stat-icon.period {
  background: linear-gradient(135deg, #b58c59, #8b6b3e);
}

.stat-icon.admin {
  background: linear-gradient(135deg, #8b7355, #6b5d4d);
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #4a3f35;
  line-height: 1.2;
  font-family: 'Noto Serif SC', serif;
}

.stat-label {
  font-size: 13px;
  color: #8b7355;
  margin-top: 2px;
}

.stat-trend {
  text-align: right;
  flex-shrink: 0;
}

.trend-up {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #3a8f7b;
}

.trend-stable {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #8b7355;
}

.trend-label {
  font-size: 11px;
  color: #b0a090;
}

/* 快捷入口 */
.quick-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #4a3f35;
  margin: 0 0 14px;
  letter-spacing: 1px;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.quick-item {
  background: #fff;
  border-radius: 10px;
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  border: 1px solid #ede5d8;
  transition: all 0.2s ease;
}

.quick-item:hover {
  background: #faf6f0;
  border-color: #d9c9a5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.quick-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #f5f0e8;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c4823e;
  flex-shrink: 0;
}

.quick-item span {
  font-size: 14px;
  font-weight: 500;
  color: #5a4d3f;
}

/* 底部信息 */
.home-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #e0d5c5;
  font-size: 12px;
  color: #b0a090;
}

.footer-sep {
  color: #d4c5b0;
}

/* 响应式 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-grid {
    grid-template-columns: 1fr;
  }
}
</style>
