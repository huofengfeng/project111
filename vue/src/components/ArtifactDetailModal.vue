<template>
  <Teleport to="body">
    <Transition name="heritage-fade">
      <div v-if="modelValue" class="artifact-detail-overlay" @click.self="close">
        <Transition name="heritage-scale">
          <div v-if="modelValue" class="artifact-detail-panel">
            <!-- 装饰边框 -->
            <div class="panel-corner corner-tl"></div>
            <div class="panel-corner corner-tr"></div>
            <div class="panel-corner corner-bl"></div>
            <div class="panel-corner corner-br"></div>

            <button class="panel-close" @click="close">
              <el-icon><Close /></el-icon>
            </button>

            <!-- 主内容 -->
            <div class="panel-body">
              <!-- 左侧：大图 -->
              <div class="panel-visual">
                <div class="image-frame">
                  <img v-if="item?.image_url" :src="getImageUrl(item.image_url)" :alt="item.name" />
                  <div v-else class="image-placeholder">
                    <el-icon :size="56"><Collection /></el-icon>
                    <span>暂无图片</span>
                  </div>
                </div>
                <div class="visual-caption">
                  <span class="caption-line"></span>
                  <span class="caption-text">{{ item?.name }}</span>
                  <span class="caption-line"></span>
                </div>
              </div>

              <!-- 右侧：信息 -->
              <div class="panel-info">
                <div class="info-header">
                  <span class="era-tag">{{ item?.era }}</span>
                  <span class="type-tag">{{ item?.type }}</span>
                </div>

                <h2 class="info-title">
                  <span class="title-bracket">〔</span>
                  {{ item?.name }}
                  <span class="title-bracket">〕</span>
                </h2>

                <p class="info-subtitle" v-if="item?.museum">
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ item.museum }}
                </p>

                <div class="info-divider">
                  <span class="divider-dot"></span>
                  <span class="divider-line"></span>
                  <span class="divider-dot"></span>
                </div>

                <div class="info-fields">
                  <div class="info-field">
                    <span class="field-name">年代</span>
                    <span class="field-value">{{ item?.era || '-' }}</span>
                  </div>
                  <div class="info-field">
                    <span class="field-name">器型</span>
                    <span class="field-value">{{ item?.type || '-' }}</span>
                  </div>
                  <div class="info-field">
                    <span class="field-name">尺寸</span>
                    <span class="field-value">{{ item?.size || '-' }}</span>
                  </div>
                  <div class="info-field">
                    <span class="field-name">釉色</span>
                    <span class="field-value">{{ item?.glaze || '-' }}</span>
                  </div>
                  <div class="info-field">
                    <span class="field-name">等级</span>
                    <span class="field-value">{{ item?.level || '-' }}</span>
                  </div>
                  <div class="info-field">
                    <span class="field-name">来源</span>
                    <span class="field-value">{{ item?.source || '-' }}</span>
                  </div>
                  <div class="info-field field-full">
                    <span class="field-name">馆藏</span>
                    <span class="field-value">{{ item?.museum || '-' }}</span>
                  </div>
                  <div class="info-field field-full" v-if="item?.description">
                    <span class="field-name">简介</span>
                    <span class="field-value field-desc">{{ item.description }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { Close, Collection, OfficeBuilding } from '@element-plus/icons-vue'
import { getImageUrl } from '@/utils/imageUrl'

defineProps({
  modelValue: Boolean,
  item: Object,
})

const emit = defineEmits(['update:modelValue'])

const close = () => {
  emit('update:modelValue', false)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.artifact-detail-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(26, 21, 16, 0.78);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.artifact-detail-panel {
  width: 100%;
  max-width: 960px;
  max-height: 90vh;
  overflow-y: auto;
  background:
    linear-gradient(145deg, #fbf7f0 0%, #f2ece0 50%, #e9e0d0 100%);
  border-radius: 8px;
  box-shadow:
    0 28px 90px rgba(0, 0, 0, 0.4),
    inset 0 0 0 1px rgba(201, 168, 76, 0.25);
  padding: 40px;
  position: relative;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

/* 四角装饰 */
.panel-corner {
  position: absolute;
  width: 34px;
  height: 34px;
  border: 2px solid rgba(201, 168, 76, 0.45);
}

.corner-tl {
  top: 14px;
  left: 14px;
  border-right: none;
  border-bottom: none;
  border-top-left-radius: 4px;
}

.corner-tr {
  top: 14px;
  right: 14px;
  border-left: none;
  border-bottom: none;
  border-top-right-radius: 4px;
}

.corner-bl {
  bottom: 14px;
  left: 14px;
  border-right: none;
  border-top: none;
  border-bottom-left-radius: 4px;
}

.corner-br {
  bottom: 14px;
  right: 14px;
  border-left: none;
  border-top: none;
  border-bottom-right-radius: 4px;
}

.panel-close {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(139, 115, 85, 0.3);
  background: transparent;
  border-radius: 50%;
  color: #8b7355;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}

.panel-close:hover {
  background: rgba(201, 168, 76, 0.1);
  border-color: #c9a84c;
  color: #5c4d3c;
  transform: rotate(90deg);
}

.panel-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
}

/* 左侧图片 */
.panel-visual {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.image-frame {
  flex: 1;
  min-height: 360px;
  background: #f5f0e8;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e8e0d4;
  box-shadow: inset 0 0 40px rgba(201, 168, 76, 0.06);
}

.image-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #c9a84c;
  opacity: 0.5;
}

.image-placeholder span {
  font-size: 13px;
  letter-spacing: 2px;
}

.visual-caption {
  display: flex;
  align-items: center;
  gap: 12px;
}

.caption-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 115, 85, 0.35), transparent);
}

.caption-text {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 2px;
  white-space: nowrap;
}

/* 右侧信息 */
.panel-info {
  display: flex;
  flex-direction: column;
}

.info-header {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}

.era-tag, .type-tag {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 3px;
  letter-spacing: 1px;
}

.era-tag {
  color: #c9a84c;
  background: rgba(201, 168, 76, 0.1);
  border: 1px solid rgba(201, 168, 76, 0.2);
}

.type-tag {
  color: #8b7355;
  background: #f5f0e8;
  border: 1px solid #e8e0d4;
}

.info-title {
  font-size: 26px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 3px;
  margin: 0 0 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-bracket {
  color: #c9a84c;
  font-size: 22px;
  font-weight: 400;
  opacity: 0.6;
}

.info-subtitle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #8b7355;
  margin: 0 0 20px;
  letter-spacing: 1px;
}

.info-divider {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 22px;
}

.divider-dot {
  width: 5px;
  height: 5px;
  background: #c9a84c;
  border-radius: 50%;
  opacity: 0.6;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, #c9a84c, transparent);
  opacity: 0.3;
}

.info-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.info-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 5px;
  border: 1px solid rgba(232, 224, 212, 0.8);
}

.field-full {
  grid-column: 1 / -1;
}

.field-name {
  font-size: 12px;
  color: #8b7355;
  letter-spacing: 2px;
}

.field-value {
  font-size: 15px;
  color: #4a3f35;
  font-weight: 500;
}

.field-desc {
  line-height: 1.7;
  font-weight: 400;
}

/* 动画 */
.heritage-fade-enter-active,
.heritage-fade-leave-active {
  transition: opacity 0.3s ease;
}

.heritage-fade-enter-from,
.heritage-fade-leave-to {
  opacity: 0;
}

.heritage-scale-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.heritage-scale-leave-active {
  transition: all 0.3s ease;
}

.heritage-scale-enter-from {
  opacity: 0;
  transform: scale(0.94) translateY(20px);
}

.heritage-scale-leave-to {
  opacity: 0;
  transform: scale(0.96);
}

/* 滚动条美化 */
.artifact-detail-panel::-webkit-scrollbar {
  width: 6px;
}

.artifact-detail-panel::-webkit-scrollbar-track {
  background: transparent;
}

.artifact-detail-panel::-webkit-scrollbar-thumb {
  background: rgba(201, 168, 76, 0.35);
  border-radius: 3px;
}

/* 响应式 */
@media (max-width: 900px) {
  .artifact-detail-panel {
    padding: 28px;
    max-height: 92vh;
  }

  .panel-body {
    grid-template-columns: 1fr;
  }

  .image-frame {
    min-height: 280px;
  }

  .info-title {
    font-size: 22px;
  }
}

@media (max-width: 520px) {
  .artifact-detail-overlay {
    padding: 12px;
  }

  .artifact-detail-panel {
    padding: 22px 18px;
  }

  .info-fields {
    grid-template-columns: 1fr;
  }

  .panel-corner {
    width: 24px;
    height: 24px;
  }
}
</style>