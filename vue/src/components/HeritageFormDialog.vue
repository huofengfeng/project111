<template>
  <Teleport to="body">
    <Transition name="heritage-fade">
      <div v-if="modelValue" class="heritage-form-overlay" @click.self="handleClose">
        <Transition name="heritage-scale">
          <div v-if="modelValue" class="heritage-form-panel">
            <!-- 四角装饰 -->
            <div class="panel-corner corner-tl"></div>
            <div class="panel-corner corner-tr"></div>
            <div class="panel-corner corner-bl"></div>
            <div class="panel-corner corner-br"></div>

            <!-- 头部 -->
            <div class="panel-header">
              <div class="header-ornament">
                <span class="ornament-line"></span>
                <span class="ornament-icon">❖</span>
                <span class="ornament-line"></span>
              </div>
              <h3 class="header-title">
                <span class="title-bracket">〔</span>
                {{ title }}
                <span class="title-bracket">〕</span>
              </h3>
            </div>

            <!-- 表单内容 -->
            <div class="panel-body">
              <slot />
            </div>

            <!-- 底部按钮 -->
            <div class="panel-footer">
              <div class="footer-ornament">
                <span class="ornament-dot"></span>
                <span class="ornament-line short"></span>
                <span class="ornament-dot"></span>
              </div>
              <div class="footer-actions">
                <button class="heritage-btn btn-secondary" @click="handleClose">
                  {{ cancelText }}
                </button>
                <button class="heritage-btn btn-primary" @click="handleConfirm">
                  {{ confirmText }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  title: { type: String, default: '' },
  confirmText: { type: String, default: '保存' },
  cancelText: { type: String, default: '取消' },
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const handleClose = () => {
  emit('cancel')
  emit('update:modelValue', false)
}

const handleConfirm = () => {
  emit('confirm')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.heritage-form-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(26, 21, 16, 0.72);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.heritage-form-panel {
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  overflow-y: auto;
  background:
    linear-gradient(145deg, #fbf7f0 0%, #f2ece0 50%, #e9e0d0 100%);
  border-radius: 8px;
  box-shadow:
    0 24px 80px rgba(0, 0, 0, 0.35),
    inset 0 0 0 1px rgba(201, 168, 76, 0.25);
  padding: 32px;
  position: relative;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

/* 四角装饰 */
.panel-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 2px solid rgba(201, 168, 76, 0.4);
}

.corner-tl {
  top: 12px;
  left: 12px;
  border-right: none;
  border-bottom: none;
  border-top-left-radius: 4px;
}

.corner-tr {
  top: 12px;
  right: 12px;
  border-left: none;
  border-bottom: none;
  border-top-right-radius: 4px;
}

.corner-bl {
  bottom: 12px;
  left: 12px;
  border-right: none;
  border-top: none;
  border-bottom-left-radius: 4px;
}

.corner-br {
  bottom: 12px;
  right: 12px;
  border-left: none;
  border-top: none;
  border-bottom-right-radius: 4px;
}

/* 头部 */
.panel-header {
  text-align: center;
  margin-bottom: 24px;
}

.header-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 12px;
}

.ornament-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 115, 85, 0.4), transparent);
}

.ornament-line.short {
  width: 40px;
}

.ornament-icon {
  font-size: 11px;
  color: rgba(201, 168, 76, 0.6);
  letter-spacing: 2px;
}

.ornament-dot {
  width: 5px;
  height: 5px;
  background: #c9a84c;
  border-radius: 50%;
  opacity: 0.5;
}

.header-title {
  font-size: 22px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 3px;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.title-bracket {
  color: #c9a84c;
  font-size: 20px;
  font-weight: 400;
  opacity: 0.6;
}

/* 内容 */
.panel-body {
  padding: 0 8px;
}

.panel-body :deep(.el-form-item__label) {
  color: #5c4d3c;
  font-weight: 500;
  letter-spacing: 1px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

.panel-body :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 0 0 1px #e0d5c5 inset;
  border-radius: 5px;
}

.panel-body :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #c9a84c inset;
}

.panel-body :deep(.el-input__inner) {
  color: #4a3f35;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

.panel-body :deep(.el-input__inner::placeholder) {
  color: #b0a090;
}

/* 底部 */
.panel-footer {
  margin-top: 24px;
}

.footer-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
}

.footer-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
}

.heritage-btn {
  min-width: 110px;
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 14px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.25s ease;
  border: 1px solid transparent;
}

.btn-primary {
  background: linear-gradient(135deg, #c9a84c, #b08d3e);
  color: #fff;
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.25);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #b08d3e, #9a7a35);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(201, 168, 76, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #8b7355;
  border-color: #d8cbb5;
}

.btn-secondary:hover {
  background: rgba(201, 168, 76, 0.08);
  border-color: #c9a84c;
  color: #5c4d3c;
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
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.heritage-scale-leave-active {
  transition: all 0.25s ease;
}

.heritage-scale-enter-from {
  opacity: 0;
  transform: scale(0.94) translateY(16px);
}

.heritage-scale-leave-to {
  opacity: 0;
  transform: scale(0.96);
}

/* 滚动条 */
.heritage-form-panel::-webkit-scrollbar {
  width: 5px;
}

.heritage-form-panel::-webkit-scrollbar-track {
  background: transparent;
}

.heritage-form-panel::-webkit-scrollbar-thumb {
  background: rgba(201, 168, 76, 0.3);
  border-radius: 3px;
}

@media (max-width: 520px) {
  .heritage-form-panel {
    padding: 24px 18px;
  }

  .header-title {
    font-size: 19px;
  }

  .footer-actions {
    flex-direction: column;
  }

  .heritage-btn {
    width: 100%;
  }
}
</style>