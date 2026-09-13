<template>
  <div class="quiz-page">
    <!-- 导航 -->
    <header class="quiz-nav">
      <div class="nav-inner">
        <router-link to="/" class="nav-brand">
          <img src="../../assets/imgs/logo2.png" alt="" class="brand-icon">
          <span class="brand-text">唐三彩文物系统</span>
        </router-link>
        <router-link to="/" class="nav-back">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </router-link>
      </div>
    </header>

    <!-- Hero -->
    <section class="quiz-hero">
      <div class="hero-pattern"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-line"></span>
          <span class="badge-text">文物猜谜</span>
          <span class="badge-line"></span>
        </div>
        <h1 class="hero-title">唐风识珍</h1>
        <p class="hero-subtitle">5 题挑战 · 根据提示猜出文物名称</p>
      </div>
    </section>

    <!-- 主区域 -->
    <section class="quiz-main">
      <div class="quiz-container">
        <!-- 加载中 -->
        <div class="quiz-loading" v-if="loading">
          <div class="loading-spinner"></div>
          <span>正在出题中...</span>
        </div>

        <!-- 游戏进行中 -->
        <template v-if="!loading && !finished">
          <!-- 进度条 -->
          <div class="progress-section">
            <div class="progress-info">
              <span class="progress-label">第 {{ currentIndex + 1 }} / 5 题</span>
              <span class="progress-score">
                <span class="score-icon">✦</span>
                {{ totalScore }} 分
              </span>
            </div>
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: ((currentIndex + (result ? 1 : 0)) / 5 * 100) + '%' }"></div>
            </div>
          </div>

          <!-- 得分提示 -->
          <div class="score-hint-bar">
            <span class="score-hint-item" :class="{ active: revealedHints === 0 }">100分</span>
            <span class="score-hint-arrow">→</span>
            <span class="score-hint-item" :class="{ active: revealedHints === 1 }">75分</span>
            <span class="score-hint-arrow">→</span>
            <span class="score-hint-item" :class="{ active: revealedHints === 2 }">50分</span>
            <span class="score-hint-arrow">→</span>
            <span class="score-hint-item" :class="{ active: revealedHints === 3 }">25分</span>
          </div>

          <!-- 关卡标签 -->
          <div class="level-tag" v-if="currentQuestion">
            <span class="level-text">{{ currentQuestion.level }}</span>
          </div>

          <!-- 提示区域 -->
          <div class="hints-panel">
            <div class="hints-title">
              <span class="ornament-line"></span>
              <span class="ornament-dot">❖</span>
              <span class="hints-label">线索提示</span>
              <span class="ornament-dot">❖</span>
              <span class="ornament-line"></span>
            </div>

            <div class="hints-list">
              <div
                v-for="(hint, i) in currentHints"
                :key="i"
                class="hint-card"
                :class="{
                  'hint-revealed': revealedHints >= i,
                  'hint-peek': revealedHints >= i - 1 && revealedHints <= i,
                }"
                @click="revealHint(i)"
              >
                <div class="hint-header">
                  <span class="hint-num">{{ i + 1 }}</span>
                  <span class="hint-label">{{ hint.label }}</span>
                  <span v-if="revealedHints < i" class="hint-status">
                    <el-icon><Lock /></el-icon>
                    点击展开
                  </span>
                  <span v-else class="hint-status revealed">
                    <el-icon><View /></el-icon>
                    已展开
                  </span>
                </div>
                <div class="hint-body" v-show="revealedHints >= i">
                  <p class="hint-text">{{ hint.text }}</p>
                  <div v-if="hint.image" class="hint-image">
                    <img :src="hint.image" alt="文物图片" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="guess-panel" v-if="!result">
            <div class="guess-input-row">
              <el-input
                v-model="guessInput"
                placeholder="输入文物名称..."
                size="large"
                clearable
                @keyup.enter="submitGuess"
                :disabled="submitting"
              >
                <template #prefix>
                  <el-icon><EditPen /></el-icon>
                </template>
              </el-input>
              <button
                class="guess-btn"
                @click="submitGuess"
                :disabled="!guessInput.trim() || submitting"
              >
                {{ submitting ? '校验中...' : '确认猜测' }}
              </button>
            </div>
            <div class="guess-actions">
              <button class="show-answer-btn" @click="revealAnswer" v-if="!showAnswer">
                <el-icon><View /></el-icon>
                显示答案
              </button>
              <div class="guess-hint-tip">
                <el-icon><InfoFilled /></el-icon>
                已揭示 {{ revealedHints + 1 }} 条线索，还有 {{ 4 - (revealedHints + 1) }} 条可展开
              </div>
            </div>
          </div>

          <!-- 显示答案区域 -->
          <div class="revealed-answer" v-if="showAnswer && revealedAnswerName">
            <div class="revealed-answer-card">
              <div class="revealed-answer-label">
                <el-icon><View /></el-icon>
                正确答案
              </div>
              <div class="revealed-answer-name">{{ revealedAnswerName }}</div>
            </div>
          </div>

          <!-- 答对撒花容器 -->
          <div class="confetti-container" v-if="showConfetti">
            <div
              v-for="i in 50"
              :key="i"
              class="confetti-piece"
              :style="{
                '--x': Math.random() * 100 + '%',
                '--delay': Math.random() * 0.5 + 's',
                '--rotation': Math.random() * 720 - 360 + 'deg',
                '--color': confettiColors[i % confettiColors.length],
                '--size': (Math.random() * 8 + 6) + 'px',
              }"
            ></div>
          </div>

          <!-- 结果面板 -->
          <div class="result-panel" v-if="result" :class="{ 'shake': resultShake }">
            <div class="result-card" :class="result.correct ? 'result-success' : 'result-fail'">
              <div class="result-icon">
                <el-icon v-if="result.correct" :size="40"><CircleCheckFilled /></el-icon>
                <el-icon v-else :size="40"><CircleCloseFilled /></el-icon>
              </div>
              <div class="result-body">
                <h3 class="result-title">
                  {{ result.correct ? '回答正确！' : '回答错误' }}
                </h3>
                <div class="result-score-badge" v-if="result.correct">
                  <span class="score-plus">+{{ result.score }}</span>
                  <span class="score-unit">分</span>
                </div>
                <p class="result-answer">
                  <span class="answer-label">正确答案：</span>
                  <span class="answer-name">{{ result.name }}</span>
                </p>
                <p class="result-meta" v-if="result.era">
                  {{ result.era }} · {{ result.type }}
                </p>
                <div class="result-image" v-if="result.image_url">
                  <img :src="getImageUrl(result.image_url)" alt="文物图片" />
                </div>
              </div>
            </div>
            <button class="next-btn" @click="nextQuestion">
              {{ currentIndex < 4 ? '下一题' : '查看结果' }}
              <el-icon><DArrowRight /></el-icon>
            </button>
          </div>
        </template>

        <!-- 最终评价 -->
        <div class="final-panel" v-if="finished">
          <div class="final-header">
            <div class="final-badge">{{ finalRating.emoji }}</div>
            <h2 class="final-title">{{ finalRating.title }}</h2>
            <p class="final-subtitle">{{ finalRating.subtitle }}</p>
          </div>

          <div class="final-score-card">
            <div class="final-score-big">{{ totalScore }}</div>
            <div class="final-score-label">总分</div>
            <div class="final-score-max">满分 500</div>
          </div>

          <div class="final-stats">
            <div class="final-stat">
              <span class="stat-num correct-num">{{ correctCount }}</span>
              <span class="stat-label">答对</span>
            </div>
            <div class="final-stat-divider"></div>
            <div class="final-stat">
              <span class="stat-num wrong-num">{{ 5 - correctCount }}</span>
              <span class="stat-label">答错</span>
            </div>
          </div>

          <div class="final-detail">
            <div class="detail-title">答题详情</div>
            <div
              v-for="(q, i) in questions"
              :key="i"
              class="detail-item"
              :class="{ 'detail-correct': q.userCorrect, 'detail-wrong': !q.userCorrect }"
            >
              <span class="detail-num">第{{ i + 1 }}题</span>
              <span class="detail-name">{{ q.answerName }}</span>
              <span class="detail-status" v-if="q.userCorrect">
                <el-icon><CircleCheckFilled /></el-icon>
                +{{ q.userScore }}分
              </span>
              <span class="detail-status wrong" v-else>
                <el-icon><CircleCloseFilled /></el-icon>
                0分
              </span>
            </div>
          </div>

          <button class="restart-btn" @click="restartGame">
            <el-icon><RefreshRight /></el-icon>
            再来一轮
          </button>
        </div>
      </div>
    </section>

    <footer class="quiz-footer">
      <div class="footer-inner">
        <span>唐三彩文物数字化管理系统 v1.0</span>
        <span class="footer-sep">|</span>
        <span>守护千年文明，传承文化瑰宝</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  ArrowLeft, Lock, View, EditPen, InfoFilled,
  CircleCheckFilled, CircleCloseFilled, DArrowRight, RefreshRight,
} from '@element-plus/icons-vue'
import request from '@/utils/request'
import { getImageUrl } from '@/utils/imageUrl'

const loading = ref(false)
const submitting = ref(false)
const questions = ref([])
const currentIndex = ref(0)
const revealedHints = ref(0)
const guessInput = ref('')
const result = ref(null)
const showAnswer = ref(false)
const revealedAnswerName = ref('')
const showConfetti = ref(false)
const resultShake = ref(false)
const finished = ref(false)
const totalScore = ref(0)
const correctCount = ref(0)

const confettiColors = ['#c9a84c', '#e8b84b', '#67a15c', '#d4a76a', '#c07050', '#e8dcc8', '#b08d3e', '#8b7355']

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const currentHints = computed(() => currentQuestion.value?.hints || [])

const finalRating = computed(() => {
  const s = totalScore.value
  if (s >= 450) return { emoji: '👑', title: '唐三彩大师', subtitle: '你对唐三彩了如指掌，堪称大师！' }
  if (s >= 350) return { emoji: '🏆', title: '文物鉴赏家', subtitle: '学识渊博，令人钦佩！' }
  if (s >= 250) return { emoji: '🎖️', title: '文化爱好者', subtitle: '对唐三彩有不错的了解！' }
  if (s >= 150) return { emoji: '📖', title: '初窥门径', subtitle: '继续学习，你会越来越棒！' }
  return { emoji: '🌱', title: '初学乍练', subtitle: '多了解唐三彩文化，下次会更好！' }
})

const loadRound = () => {
  loading.value = true
  finished.value = false
  currentIndex.value = 0
  totalScore.value = 0
  correctCount.value = 0
  questions.value = []
  result.value = null
  showAnswer.value = false
  revealedAnswerName.value = ''
  guessInput.value = ''
  revealedHints.value = 0

  request.get('/quiz/round').then(res => {
    if (res.code === '200') {
      questions.value = res.data.questions
    }
  }).catch(() => {}).finally(() => {
    loading.value = false
  })
}

const revealHint = (index) => {
  if (index <= revealedHints.value) return
  revealedHints.value = index
}

const submitGuess = () => {
  const val = guessInput.value.trim()
  if (!val || submitting.value || !currentQuestion.value) return

  submitting.value = true
  request.post('/quiz/guess', {
    artifact_id: currentQuestion.value.id,
    answer: val,
    revealed_hints: revealedHints.value,
  }).then(res => {
    if (res.code === '200') {
      result.value = res.data
      totalScore.value += res.data.score
      if (res.data.correct) {
        correctCount.value++
        showConfetti.value = true
        resultShake.value = false
        setTimeout(() => { showConfetti.value = false }, 2500)
      } else {
        resultShake.value = true
        setTimeout(() => { resultShake.value = false }, 600)
        showConfetti.value = false
      }
      // 保存答题记录
      questions.value[currentIndex.value].answerName = res.data.name
      questions.value[currentIndex.value].userCorrect = res.data.correct
      questions.value[currentIndex.value].userScore = res.data.score
    }
  }).catch(() => {}).finally(() => {
    submitting.value = false
  })
}

const revealAnswer = () => {
  showAnswer.value = true
  // 调用后端获取正确答案
  if (!currentQuestion.value) return
  request.post('/quiz/guess', {
    artifact_id: currentQuestion.value.id,
    answer: '',
    revealed_hints: 3,
  }).then(res => {
    if (res.code === '200') {
      revealedAnswerName.value = res.data.name
      // 记录答题信息
      questions.value[currentIndex.value].answerName = res.data.name
      questions.value[currentIndex.value].userCorrect = false
      questions.value[currentIndex.value].userScore = 0
    }
  }).catch(() => {})
}

const nextQuestion = () => {
  if (currentIndex.value >= 4) {
    finished.value = true
    return
  }
  currentIndex.value++
  result.value = null
  showAnswer.value = false
  revealedAnswerName.value = ''
  guessInput.value = ''
  revealedHints.value = 0
}

const restartGame = () => {
  loadRound()
}

onMounted(() => {
  loadRound()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.quiz-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  background: #f5f0e8;
  min-height: 100vh;
}

/* 导航 */
.quiz-nav {
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

/* Hero */
.quiz-hero {
  position: relative;
  padding: 100px 40px 50px;
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

.hero-content { position: relative; z-index: 1; }

.hero-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
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
  font-size: 48px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 10px;
  margin: 0 0 10px;
  text-shadow: 0 4px 30px rgba(201, 168, 76, 0.15);
}

.hero-subtitle {
  font-size: 16px;
  color: rgba(232, 220, 200, 0.45);
  letter-spacing: 4px;
  margin: 0;
}

/* 主区域 */
.quiz-main {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px 24px 80px;
}

.quiz-container { position: relative; }

/* 进度条 */
.progress-section {
  margin-bottom: 16px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  color: #4a3f35;
  font-weight: 600;
  letter-spacing: 1px;
}

.progress-score {
  font-size: 14px;
  color: #c9a84c;
  font-weight: 700;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.score-icon { font-size: 12px; }

.progress-track {
  height: 6px;
  background: #e8e0d4;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #c9a84c, #e8b84b);
  border-radius: 3px;
  transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 得分提示条 */
.score-hint-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px 16px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e8e0d4;
}

.score-hint-item {
  font-size: 13px;
  color: #b0a090;
  font-weight: 600;
  letter-spacing: 1px;
  transition: all 0.3s;
  padding: 2px 8px;
  border-radius: 4px;
}

.score-hint-item.active {
  color: #c9a84c;
  background: rgba(201, 168, 76, 0.1);
  transform: scale(1.1);
}

.score-hint-arrow {
  color: #d4c8b0;
  font-size: 12px;
}

/* 关卡标签 */
.level-tag {
  text-align: center;
  margin-bottom: 16px;
}

.level-text {
  display: inline-block;
  font-size: 13px;
  letter-spacing: 2px;
  color: #c9a84c;
  padding: 4px 16px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 20px;
  background: rgba(201, 168, 76, 0.06);
}

/* 提示面板 */
.hints-panel { margin-bottom: 20px; }

.hints-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}

.ornament-line {
  width: 50px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 115, 85, 0.35), transparent);
}

.ornament-dot {
  font-size: 10px;
  color: rgba(201, 168, 76, 0.5);
  letter-spacing: 2px;
}

.hints-label {
  font-size: 14px;
  color: #8b7355;
  letter-spacing: 2px;
}

.hints-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.hint-card {
  background: #fff;
  border: 1px solid #e8e0d4;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.hint-card:hover {
  border-color: #c9a84c;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.hint-card.hint-revealed {
  border-color: rgba(201, 168, 76, 0.3);
  background: linear-gradient(135deg, #fdfaf3, #f7f1e3);
}

.hint-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
}

.hint-num {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #f5f0e8;
  color: #8b7355;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hint-revealed .hint-num {
  background: rgba(201, 168, 76, 0.15);
  color: #c9a84c;
}

.hint-label {
  font-size: 14px;
  font-weight: 600;
  color: #4a3f35;
  letter-spacing: 1px;
  flex: 1;
}

.hint-status {
  font-size: 12px;
  color: #b0a090;
  display: flex;
  align-items: center;
  gap: 4px;
}

.hint-status.revealed { color: #67a15c; }

.hint-body {
  padding: 0 16px 16px 52px;
  animation: hintSlide 0.3s ease;
}

.hint-text {
  font-size: 15px;
  color: #5c4d3c;
  line-height: 1.7;
  margin: 0 0 12px;
  letter-spacing: 1px;
}

.hint-image {
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #e8e0d4;
  max-width: 320px;
}

.hint-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
}

/* 猜测输入 */
.guess-panel {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  border: 1px solid #e8e0d4;
}

.guess-input-row {
  display: flex;
  gap: 10px;
}

.guess-input-row :deep(.el-input__wrapper) {
  background: #faf8f4;
  box-shadow: 0 0 0 1px #e8e0d4 inset;
  border-radius: 6px;
}

.guess-input-row :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px #c9a84c inset;
}

.guess-btn {
  flex-shrink: 0;
  padding: 0 28px;
  background: linear-gradient(135deg, #c9a84c, #b08d3e);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.25);
}

.guess-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #b08d3e, #9a7a35);
  transform: translateY(-1px);
}

.guess-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.guess-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.show-answer-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  background: transparent;
  border: 1px solid rgba(192, 112, 80, 0.3);
  border-radius: 6px;
  color: #c07050;
  font-size: 13px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.25s;
}

.show-answer-btn:hover {
  background: rgba(192, 112, 80, 0.08);
  border-color: rgba(192, 112, 80, 0.5);
}

.guess-hint-tip {
  font-size: 12px;
  color: #b0a090;
  display: flex;
  align-items: center;
  gap: 6px;
  letter-spacing: 1px;
}

/* 显示答案卡片 */
.revealed-answer {
  margin-top: 16px;
  animation: resultUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.revealed-answer-card {
  background: linear-gradient(135deg, #fef9f0, #fdf3e2);
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 10px;
  padding: 20px 24px;
  text-align: center;
}

.revealed-answer-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #c07050;
  letter-spacing: 2px;
  margin-bottom: 10px;
  padding: 3px 14px;
  border: 1px solid rgba(192, 112, 80, 0.2);
  border-radius: 20px;
  background: rgba(192, 112, 80, 0.05);
}

.revealed-answer-name {
  font-size: 24px;
  font-weight: 700;
  color: #c9a84c;
  letter-spacing: 3px;
  text-shadow: 0 2px 8px rgba(201, 168, 76, 0.15);
}

/* 撒花容器 */
.confetti-container {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 200;
  overflow: hidden;
}

.confetti-piece {
  position: absolute;
  top: -20px;
  left: var(--x);
  width: var(--size);
  height: var(--size);
  background: var(--color);
  animation: confettiFall 2.5s var(--delay) ease-out forwards;
  border-radius: 2px;
  opacity: 0;
}

@keyframes confettiFall {
  0% {
    opacity: 1;
    transform: translateY(0) rotate(0deg) scale(0);
  }
  10% {
    opacity: 1;
    transform: translateY(100px) rotate(var(--rotation)) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(100vh) rotate(calc(var(--rotation) + 360deg)) scale(0.3);
  }
}

/* 结果面板 */
.result-panel {
  text-align: center;
}

.result-panel.shake {
  animation: shake 0.5s ease;
}

.result-card {
  border-radius: 12px;
  padding: 28px 24px;
  margin-bottom: 20px;
  border: 1px solid;
  animation: resultUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.result-success {
  background: linear-gradient(135deg, #f5faf0, #edf5e6);
  border-color: rgba(103, 161, 92, 0.2);
}

.result-fail {
  background: linear-gradient(135deg, #faf6f0, #f5ede0);
  border-color: rgba(192, 112, 80, 0.2);
}

.result-icon { margin-bottom: 12px; }
.result-success .result-icon { color: #67a15c; }
.result-fail .result-icon { color: #c07050; }

.result-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 2px;
  margin: 0 0 10px;
}

.result-success .result-title { color: #4a7a3e; }
.result-fail .result-title { color: #8b5a3e; }

.result-score-badge {
  display: inline-flex;
  align-items: baseline;
  gap: 2px;
  background: linear-gradient(135deg, #c9a84c, #b08d3e);
  color: #fff;
  padding: 4px 14px;
  border-radius: 20px;
  margin-bottom: 10px;
  box-shadow: 0 2px 10px rgba(201, 168, 76, 0.3);
  animation: scorePop 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.score-plus {
  font-size: 20px;
  font-weight: 700;
}

.score-unit {
  font-size: 12px;
  opacity: 0.9;
}

.result-answer {
  font-size: 16px;
  margin: 0 0 8px;
}

.answer-label { color: #8b7355; }

.answer-name {
  color: #c9a84c;
  font-weight: 700;
  font-size: 20px;
  letter-spacing: 2px;
}

.result-meta {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
  margin: 0;
}

.result-image {
  margin-top: 16px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e8e0d4;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.result-image img {
  width: 100%;
  height: auto;
  display: block;
}

.next-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 36px;
  background: linear-gradient(135deg, #c9a84c, #b08d3e);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.25);
}

.next-btn:hover {
  background: linear-gradient(135deg, #b08d3e, #9a7a35);
  transform: translateY(-1px);
  box-shadow: 0 6px 22px rgba(201, 168, 76, 0.3);
}

/* 最终评价面板 */
.final-panel {
  text-align: center;
  padding: 20px 0;
  animation: resultUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.final-header {
  margin-bottom: 24px;
}

.final-badge {
  font-size: 56px;
  margin-bottom: 12px;
  animation: scorePop 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.final-title {
  font-size: 32px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 4px;
  margin: 0 0 8px;
}

.final-subtitle {
  font-size: 15px;
  color: #8b7355;
  letter-spacing: 2px;
  margin: 0;
}

.final-score-card {
  background: linear-gradient(135deg, #2c241b, #1a1510);
  border-radius: 16px;
  padding: 32px 24px;
  margin-bottom: 20px;
  border: 1px solid rgba(201, 168, 76, 0.2);
  position: relative;
  overflow: hidden;
}

.final-score-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a84c' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}

.final-score-big {
  font-size: 72px;
  font-weight: 700;
  color: #e8dcc8;
  letter-spacing: 4px;
  position: relative;
  z-index: 1;
}

.final-score-label {
  font-size: 14px;
  color: rgba(232, 220, 200, 0.5);
  letter-spacing: 3px;
  margin-top: 4px;
  position: relative;
  z-index: 1;
}

.final-score-max {
  font-size: 12px;
  color: rgba(232, 220, 200, 0.3);
  letter-spacing: 2px;
  margin-top: 4px;
  position: relative;
  z-index: 1;
}

.final-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  background: #fff;
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 20px;
  border: 1px solid #e8e0d4;
}

.final-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}

.stat-num {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 1px;
}

.correct-num { color: #67a15c; }
.wrong-num { color: #c07050; }

.stat-label {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
  margin-top: 2px;
}

.final-stat-divider {
  width: 1px;
  height: 48px;
  background: #e8e0d4;
  margin: 0 24px;
}

/* 答题详情 */
.final-detail {
  background: #fff;
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 24px;
  border: 1px solid #e8e0d4;
  text-align: left;
}

.detail-title {
  font-size: 14px;
  font-weight: 600;
  color: #4a3f35;
  letter-spacing: 2px;
  margin-bottom: 14px;
  text-align: center;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f5f0e8;
}

.detail-item:last-child { border-bottom: none; }

.detail-num {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
  min-width: 48px;
}

.detail-name {
  font-size: 14px;
  color: #4a3f35;
  font-weight: 600;
  letter-spacing: 1px;
  flex: 1;
}

.detail-status {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #67a15c;
}

.detail-status.wrong {
  color: #c07050;
}

.restart-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 40px;
  background: linear-gradient(135deg, #c9a84c, #b08d3e);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 20px rgba(201, 168, 76, 0.3);
}

.restart-btn:hover {
  background: linear-gradient(135deg, #b08d3e, #9a7a35);
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(201, 168, 76, 0.35);
}

/* 加载 */
.quiz-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
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

/* 页脚 */
.quiz-footer {
  background: #1a1510;
  padding: 24px 40px;
  text-align: center;
}

.footer-inner {
  color: rgba(232, 220, 200, 0.3);
  font-size: 12px;
  letter-spacing: 1px;
}

.footer-sep { margin: 0 12px; }

/* 动画 */
@keyframes hintSlide {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes resultUp {
  from { opacity: 0; transform: translateY(16px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes scorePop {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 50%, 90% { transform: translateX(-6px); }
  30%, 70% { transform: translateX(6px); }
}

@keyframes spin { to { transform: rotate(360deg); } }

/* 响应式 */
@media (max-width: 600px) {
  .quiz-nav { padding: 0 16px; }
  .quiz-hero { padding: 90px 20px 40px; }
  .hero-title { font-size: 36px; letter-spacing: 6px; }
  .guess-input-row { flex-direction: column; }
  .guess-btn { padding: 12px; }
  .hint-body { padding-left: 20px; }
  .guess-actions { flex-direction: column; gap: 8px; align-items: stretch; }
  .show-answer-btn { justify-content: center; }
  .final-score-big { font-size: 52px; }
  .final-title { font-size: 24px; }
  .score-hint-bar { flex-wrap: wrap; gap: 4px; }
}
</style>