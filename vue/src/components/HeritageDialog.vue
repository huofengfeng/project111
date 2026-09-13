<template>
  <Teleport to="body">
    <Transition name="heritage-fade">
      <div v-if="modelValue" class="heritage-overlay" @click.self="onCancel">
        <Transition name="heritage-scale">
          <div v-if="modelValue" class="heritage-dialog">
            <!-- 顶部装饰 -->
            <div class="dialog-ornament ornament-top">
              <div class="ornament-line"></div>
              <div class="ornament-center">❖</div>
              <div class="ornament-line"></div>
            </div>

            <!-- 内容 -->
            <div class="dialog-body">
              <h3 class="dialog-title">
                <span class="title-bracket bracket-left">〔</span>
                {{ title }}
                <span class="title-bracket bracket-right">〕</span>
              </h3>
              <p class="dialog-message">{{ message }}</p>
            </div>

            <!-- 按钮 -->
            <div class="dialog-actions">
              <button class="heritage-btn btn-secondary" @click="onCancel">
                {{ cancelText }}
              </button>
              <button class="heritage-btn btn-primary" @click="onConfirm">
                {{ confirmText }}
              </button>
            </div>

            <!-- 底部装饰 -->
            <div class="dialog-ornament ornament-bottom">
              <div class="ornament-line"></div>
              <div class="ornament-center">❖</div>
              <div class="ornament-line"></div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: '提示' },
  message: { type: String, default: '' },
  confirmText: { type: String, default: '确认' },
  cancelText: { type: String, default: '取消' },
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const onConfirm = () => {
  emit('confirm')
  emit('update:modelValue', false)
}

const onCancel = () => {
  emit('cancel')
  emit('update:modelValue', false)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.heritage-overlay {
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

.heritage-dialog {
  width: 100%;
  max-width: 420px;
  background:
    linear-gradient(145deg, #f9f5ed 0%, #f0e8d8 50%, #e8dcc8 100%);
  border-radius: 6px;
  box-shadow:
    0 24px 80px rgba(0, 0, 0, 0.35),
    inset 0 0 0 1px rgba(201, 168, 76, 0.25),
    inset 0 0 60px rgba(201, 168, 76, 0.08);
  padding: 36px 32px 30px;
  position: relative;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

/* 四角回纹装饰 */
.heritage-dialog::before,
.heritage-dialog::after {
  content: '';
  position: absolute;
  width: 28px;
  height: 28px;
  border: 2px solid rgba(201, 168, 76, 0.5);
}

.heritage-dialog::before {
  top: 12px;
  left: 12px;
  border-right: none;
  border-bottom: none;
}

.heritage-dialog::after {
  bottom: 12px;
  right: 12px;
  border-left: none;
  border-top: none;
}

.dialog-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(201, 168, 76, 0.6);
}

.ornament-top {
  margin-bottom: 22px;
}

.ornament-bottom {
  margin-top: 26px;
}

.ornament-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 115, 85, 0.4), transparent);
}

.ornament-center {
  font-size: 12px;
  letter-spacing: 2px;
}

.dialog-body {
  text-align: center;
}

.dialog-title {
  font-size: 22px;
  font-weight: 700;
  color: #5c4d3c;
  margin: 0 0 16px;
  letter-spacing: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.title-bracket {
  color: #c9a84c;
  font-size: 20px;
  font-weight: 400;
  opacity: 0.7;
}

.dialog-message {
  font-size: 15px;
  color: #7a6b5a;
  line-height: 1.8;
  margin: 0;
  letter-spacing: 1px;
}

.dialog-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  margin-top: 28px;
}

.heritage-btn {
  min-width: 120px;
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
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #b08d3e, #9a7a35);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(201, 168, 76, 0.35);
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
  transform: scale(0.92) translateY(12px);
}

.heritage-scale-leave-to {
  opacity: 0;
  transform: scale(0.96);
}

@media (max-width: 480px) {
  .heritage-dialog {
    padding: 30px 22px 24px;
  }

  .dialog-title {
    font-size: 20px;
  }

  .heritage-btn {
    flex: 1;
    min-width: 0;
  }
}
</style>