<template>
  <div class="prediction-page">
    <div class="header-action">
      <el-button type="info" plain @click="goBack" class="back-btn">&lt; 返回大屏指挥中心</el-button>
    </div>
    
    <div class="prediction-content">
      <!-- 顶部：对阵信息与刷新控制 -->
      <div class="top-bar">
        <div class="match-teams">
          <h1 class="team-text">{{ team1 }}</h1>
          <div class="vs-text">VS</div>
          <h1 class="team-text">{{ team2 }}</h1>
        </div>
        <div class="action-area">
          <el-button 
            type="primary" 
            @click="fetchAnalysis(true)" 
            :loading="loading" 
            class="cyber-btn"
            :disabled="isEnded"
            :title="isEnded ? '已结束比赛无法重新分析' : ''"
          >
            {{ isEnded ? '已结束比赛' : '启动智能深度分析' }}
          </el-button>
        </div>
      </div>
      
      <!-- 中部空出：两侧悬浮面板 -->
      <div class="side-panels-container">
        <!-- 左侧面板：核心结果与伤停 -->
        <div class="side-panel left-panel">
          <div class="stat-box glass-panel">
            <h4>预测比分</h4>
            <div v-if="loadingScore" class="mini-loader"></div>
            <div v-else class="stat-value highlight">{{ analysisResult.score || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>总进球数预测</h4>
            <div v-if="loadingGoals" class="mini-loader"></div>
            <div v-else class="stat-value">{{ analysisResult.total_goals || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>伤病与体能影响</h4>
            <div v-if="loadingInjury" class="mini-loader"></div>
            <div v-else class="stat-value text-md warning">{{ analysisResult.injury_impact || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>控球率与节奏预测</h4>
            <div v-if="loadingPossession" class="mini-loader"></div>
            <div v-else class="stat-value text-md">{{ analysisResult.possession_pace || '-' }}</div>
          </div>
        </div>

        <!-- 右侧面板：战术与犯规预警 -->
        <div class="side-panel right-panel">
          <div class="stat-box glass-panel">
            <h4>战术阵型克制分析</h4>
            <div v-if="loadingTactical" class="mini-loader"></div>
            <div v-else class="stat-value text-md">{{ analysisResult.tactical_restraint || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>核心对位优劣势</h4>
            <div v-if="loadingKeyPlayer" class="mini-loader"></div>
            <div v-else class="stat-value text-md">{{ analysisResult.key_player_duel || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>红牌概率预警</h4>
            <div v-if="loadingRedCards" class="mini-loader"></div>
            <div v-else class="stat-value warning">{{ analysisResult.red_cards || '-' }}</div>
          </div>
          
          <div class="stat-box glass-panel">
            <h4>点球预测</h4>
            <div v-if="loadingPenalties" class="mini-loader"></div>
            <div v-else class="stat-value text-md">{{ analysisResult.penalties || '-' }}</div>
          </div>
        </div>
      </div>

      <!-- 底部悬浮：专家建议与可视化图表 -->
      <div class="bottom-panel">
        <div class="advice-box glass-panel">
          <h4>专家投注执行单</h4>
          <div v-if="loadingAdvice" class="loading-box">
            <div class="loader"></div>
            <p>正在生成高精度量化投注方案...</p>
          </div>
          <div v-else-if="parsedAdvice" class="betting-dashboard">
            
            <!-- 左侧：雷达图与胜率图 -->
            <div class="charts-section">
              <div class="chart-container">
                <v-chart class="chart" :option="winRateOption" autoresize />
              </div>
              <div class="chart-container">
                <v-chart class="chart" :option="radarOption" autoresize />
              </div>
            </div>
            
            <!-- 右侧：执行单列表与总结 -->
            <div class="tickets-section">
              <div class="betting-ticket" v-for="(plan, idx) in parsedAdvice.betting_plan" :key="idx">
                <div class="ticket-header">
                  <span class="play-style">{{ plan.play_style }}</span>
                  <span class="confidence">信心指数: {{ plan.confidence }}%</span>
                </div>
                <div class="ticket-body">
                  <div class="t-row">
                    <span class="t-label">推荐:</span>
                    <span class="t-val highlight-gold">{{ plan.pick }}</span>
                  </div>
                  <div class="t-row">
                    <span class="t-label">比分:</span>
                    <span class="t-val">{{ plan.score }}</span>
                  </div>
                  <div class="t-row">
                    <span class="t-label">仓位:</span>
                    <span class="t-val warning">{{ plan.amount_advice }}</span>
                  </div>
                </div>
                <div class="ticket-footer">{{ plan.reason }}</div>
              </div>
              
              <div class="advice-summary">
                <strong>核心总评：</strong> {{ parsedAdvice.summary }}
              </div>
            </div>
          </div>
          <div v-else class="empty-box">暂无分析数据</div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 引入 ECharts
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, PieChart, RadarChart, TitleComponent, TooltipComponent, LegendComponent])

const route = useRoute()
const router = useRouter()

const team1 = computed(() => route.query.team1 || '主队')
const team2 = computed(() => route.query.team2 || '客队')
const isEnded = computed(() => route.query.ended === '1')

const loading = computed(() => loadingScore.value || loadingGoals.value || loadingRedCards.value || loadingPenalties.value || loadingAdvice.value || loadingTactical.value || loadingKeyPlayer.value || loadingInjury.value || loadingPossession.value)

const loadingScore = ref(false)
const loadingGoals = ref(false)
const loadingRedCards = ref(false)
const loadingPenalties = ref(false)
const loadingAdvice = ref(false)
const loadingTactical = ref(false)
const loadingKeyPlayer = ref(false)
const loadingInjury = ref(false)
const loadingPossession = ref(false)

const analysisResult = ref<any>({
  score: '',
  total_goals: '',
  red_cards: '',
  penalties: '',
  advice: '',
  tactical_restraint: '',
  key_player_duel: '',
  injury_impact: '',
  possession_pace: ''
})

const parsedAdvice = computed(() => {
  try {
    if (!analysisResult.value.advice) return null;
    // 尝试清理可能存在的 markdown json 代码块
    let raw = analysisResult.value.advice;
    raw = raw.replace(/```json\n?/g, '').replace(/```/g, '').trim();
    return JSON.parse(raw);
  } catch (e) {
    console.error("JSON parse error:", e);
    return null;
  }
})

const winRateOption = computed(() => {
  if (!parsedAdvice.value) return {};
  const rates = parsedAdvice.value.win_rates || {};
  return {
    title: { text: '胜负概率', left: 'center', textStyle: { color: '#D2A76D', fontSize: 14 } },
    tooltip: { trigger: 'item' },
    series: [
      {
        name: '概率',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 5,
          borderColor: '#121212',
          borderWidth: 2
        },
        label: { show: true, color: '#fff', formatter: '{b}\n{d}%' },
        data: [
          { value: rates.team1, name: team1.value, itemStyle: { color: '#D2A76D' } },
          { value: rates.draw, name: '平局', itemStyle: { color: '#6c757d' } },
          { value: rates.team2, name: team2.value, itemStyle: { color: '#409EFF' } }
        ]
      }
    ]
  };
})

const radarOption = computed(() => {
  if (!parsedAdvice.value) return {};
  const radar = parsedAdvice.value.radar_compare || {};
  return {
    title: { text: '核心能力对抗雷达', left: 'center', textStyle: { color: '#D2A76D', fontSize: 14 } },
    tooltip: {},
    legend: { bottom: 0, textStyle: { color: '#fff' } },
    radar: {
      indicator: [
        { name: '进攻', max: 100 },
        { name: '防守', max: 100 },
        { name: '控制', max: 100 },
        { name: '经验', max: 100 },
        { name: '状态', max: 100 }
      ],
      axisName: { color: '#A0A0A0' },
      splitLine: { lineStyle: { color: 'rgba(210, 167, 109, 0.2)' } },
      splitArea: { show: false }
    },
    series: [
      {
        name: '能力对比',
        type: 'radar',
        data: [
          {
            value: [radar.attack?.[0]||0, radar.defense?.[0]||0, radar.control?.[0]||0, radar.experience?.[0]||0, radar.form?.[0]||0],
            name: team1.value,
            itemStyle: { color: '#D2A76D' },
            areaStyle: { color: 'rgba(210, 167, 109, 0.3)' }
          },
          {
            value: [radar.attack?.[1]||0, radar.defense?.[1]||0, radar.control?.[1]||0, radar.experience?.[1]||0, radar.form?.[1]||0],
            name: team2.value,
            itemStyle: { color: '#409EFF' },
            areaStyle: { color: 'rgba(64, 158, 255, 0.3)' }
          }
        ]
      }
    ]
  };
})

const fetchField = async (field: string, endpoint: string, forceRefresh: boolean) => {
  const loadingRefs: Record<string, any> = {
    'score': loadingScore,
    'total_goals': loadingGoals,
    'red_cards': loadingRedCards,
    'penalties': loadingPenalties,
    'advice': loadingAdvice,
    'tactical_restraint': loadingTactical,
    'key_player_duel': loadingKeyPlayer,
    'injury_impact': loadingInjury,
    'possession_pace': loadingPossession
  }
  
  const loadingRef = loadingRefs[field]
  loadingRef.value = true
  
  try {
    const res = await axios.post(`http://localhost:10086/api/predict/${endpoint}`, {
      team1_name: team1.value,
      team2_name: team2.value,
      force_refresh: forceRefresh
    })
    if (res.data.status === 'success') {
      analysisResult.value[field] = res.data.data
    } else {
      analysisResult.value[field] = '分析失败'
    }
  } catch (e: any) {
    analysisResult.value[field] = '请求错误'
  } finally {
    loadingRef.value = false
  }
}

const fetchAnalysis = (forceRefresh = false) => {
  if (forceRefresh) {
    analysisResult.value = { 
      score: '', total_goals: '', red_cards: '', penalties: '', advice: '',
      tactical_restraint: '', key_player_duel: '', injury_impact: '', possession_pace: ''
    }
  }
  
  fetchField('score', 'score', forceRefresh)
  fetchField('total_goals', 'goals', forceRefresh)
  fetchField('red_cards', 'red_cards', forceRefresh)
  fetchField('penalties', 'penalties', forceRefresh)
  fetchField('tactical_restraint', 'tactical', forceRefresh)
  fetchField('key_player_duel', 'key_player', forceRefresh)
  fetchField('injury_impact', 'injury', forceRefresh)
  fetchField('possession_pace', 'possession', forceRefresh)
  fetchField('advice', 'advice', forceRefresh)
}

const goBack = () => {
  router.push('/')
}

onMounted(() => {
  fetchAnalysis() // 首次进入自动获取（非强制刷新，优先取缓存）
})
</script>

<style scoped>
/* 全局网格背景 - 复用大屏风格 */
.prediction-page::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: 
    linear-gradient(rgba(210, 167, 109, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(210, 167, 109, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
  pointer-events: none;
}

.prediction-page {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  color: #fff;
  pointer-events: none; /* 让鼠标可以穿透到底层 3D 模型 */
}

.header-action {
  position: absolute;
  top: 30px;
  left: 40px;
  z-index: 30;
  pointer-events: auto;
}

.back-btn {
  background: rgba(18, 18, 18, 0.75) !important;
  border: 1px solid rgba(210, 167, 109, 0.3) !important;
  color: #D2A76D !important;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
  font-weight: bold;
  letter-spacing: 1px;
}
.back-btn:hover {
  background: rgba(210, 167, 109, 0.15) !important;
  box-shadow: 0 0 15px rgba(210, 167, 109, 0.4);
  border-color: #D2A76D !important;
}

.prediction-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  z-index: 10;
  pointer-events: none;
  padding-top: 10px;
  width: 100%;
  height: 100%;
}

.top-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px; /* Reduced */
  pointer-events: auto;
}

.match-teams {
  display: flex;
  align-items: center;
  gap: 30px; /* Reduced */
  margin-bottom: 10px; /* Reduced */
}

.team-text {
  font-size: 3rem; /* Reduced */
  font-weight: 900;
  margin: 0;
  letter-spacing: 2px;
  color: #ffffff;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.4), 0 0 30px rgba(255, 255, 255, 0.2);
  white-space: nowrap;
}

.vs-text {
  font-size: 2.2rem; /* Reduced */
  font-style: italic;
  font-weight: 900;
  background: linear-gradient(135deg, #D2A76D 0%, #A67C41 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(210, 167, 109, 0.5);
  margin-top: 5px;
}

.cyber-btn {
  background: rgba(210, 167, 109, 0.1) !important;
  border: 1px solid #D2A76D !important; 
  color: #D2A76D !important;
  font-weight: bold;
  letter-spacing: 1px;
  padding: 8px 30px; /* Reduced */
  font-size: 1rem; /* Reduced */
  transition: all 0.3s ease;
  border-radius: 8px;
}
.cyber-btn:hover {
  background: rgba(210, 167, 109, 0.25) !important;
  box-shadow: 0 0 20px rgba(210, 167, 109, 0.5);
  transform: translateY(-2px);
}

.side-panels-container {
  display: flex;
  justify-content: space-between;
  flex-shrink: 0;
  width: 100%;
  padding: 0 40px; /* 两侧留白缩减 */
  pointer-events: none;
  margin-bottom: 10px; /* 减少下边距 */
}

.side-panel {
  width: 320px; /* 缩减宽度 */
  display: flex;
  flex-direction: column;
  gap: 12px; /* 缩减垂直间距 */
  pointer-events: auto;
}

.bottom-panel {
  width: 100%;
  padding: 0 40px 20px 40px; /* 上边距清零，紧贴上面 */
  pointer-events: auto;
  display: flex;
  flex: 1; /* 撑满剩余空间 */
  min-height: 0; /* 允许内部滚动而不撑破外层 */
}

.stat-box {
  background: rgba(18, 18, 18, 0.75); /* 黑曜石底色 */
  backdrop-filter: blur(12px);
  border-radius: 10px;
  padding: 12px 15px; /* 缩减内边距 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 85px; /* 缩减高度 */
}

.stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(210, 167, 109, 0.2);
}

.stat-box h4 {
  margin: 0 0 8px 0; /* 减少下边距 */
  color: #A0A0A0; /* 中灰色 */
  font-size: 0.85rem; /* 缩小标题字号 */
  letter-spacing: 1px;
}

.stat-value {
  font-size: 1.6rem; /* 缩小数字字号 */
  font-weight: bold;
  color: #FFFFFF;
}

.stat-value.text-md {
  font-size: 1rem; /* 缩小长文字号 */
  font-weight: normal;
  color: #c9d1d9;
  line-height: 1.4;
}

.stat-value.highlight {
  background: linear-gradient(135deg, #D2A76D 0%, #A67C41 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 2.2rem; /* 缩小高亮字号 */
  text-shadow: 0 0 15px rgba(210, 167, 109, 0.4);
}

.stat-value.warning {
  color: #FFC107; /* 琥珀黄警告色 */
  text-shadow: 0 0 15px rgba(255, 193, 7, 0.3);
}

.betting-dashboard {
  display: flex;
  flex-direction: row; /* 强制横向排列 */
  width: 100%;
  flex: 1; /* 撑满剩余高度 */
  gap: 20px; /* 缩减间距 */
  overflow: hidden; /* 防止内部元素撑破容器 */
}

.charts-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 缩减间距 */
  height: 100%;
}

.chart-container {
  flex: 1;
  background: rgba(30, 26, 23, 0.4);
  border-radius: 12px;
  padding: 5px; /* 缩减内边距 */
  position: relative;
  min-height: 150px; /* 缩减最小高度 */
  width: 100%;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 140px; /* 缩减 ECharts 最小高度 */
}

.tickets-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 10px; /* 缩减间距 */
  height: 100%;
  overflow-y: auto; /* 右侧允许独立滚动 */
  padding-right: 5px; /* 缩减留白 */
}

.betting-ticket {
  background: linear-gradient(135deg, rgba(210, 167, 109, 0.1) 0%, rgba(30, 26, 23, 0.8) 100%);
  border: 1px solid rgba(210, 167, 109, 0.3);
  border-radius: 12px;
  padding: 10px 15px; /* 缩减内边距 */
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.betting-ticket:hover {
  transform: translateX(-5px);
  box-shadow: 0 5px 20px rgba(210, 167, 109, 0.2);
  border-color: rgba(210, 167, 109, 0.6);
}

.betting-ticket::before {
  content: '';
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 4px;
  background: #D2A76D;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px; /* 缩减下边距 */
  border-bottom: 1px dashed rgba(210, 167, 109, 0.2);
  padding-bottom: 8px; /* 缩减内边距 */
}

.play-style {
  font-size: 1.1rem; /* 缩小字号 */
  font-weight: bold;
  color: #fff;
  letter-spacing: 1px;
}

.confidence {
  font-size: 0.85rem; /* 缩小字号 */
  color: #D2A76D;
  background: rgba(210, 167, 109, 0.1);
  padding: 3px 8px;
  border-radius: 20px;
}

.ticket-body {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px; /* 缩减边距 */
}

.t-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.t-label {
  font-size: 0.8rem;
  color: #A0A0A0;
}

.t-val {
  font-size: 1.1rem; /* 缩小字号 */
  font-weight: bold;
  color: #fff;
}

.highlight-gold {
  color: #D2A76D;
  text-shadow: 0 0 10px rgba(210, 167, 109, 0.4);
}

.ticket-footer {
  font-size: 0.9rem;
  color: #c9d1d9;
  line-height: 1.4;
  background: rgba(0, 0, 0, 0.2);
  padding: 8px;
  border-radius: 6px;
}

.advice-summary {
  margin-top: 5px; /* 缩减边距 */
  padding: 10px; /* 缩减内边距 */
  background: rgba(210, 167, 109, 0.05);
  border-left: 4px solid #D2A76D;
  border-radius: 4px;
  color: #fff;
  font-size: 1rem; /* 缩小字号 */
  line-height: 1.5;
}

.advice-box {
  background: rgba(18, 18, 18, 0.85);
  backdrop-filter: blur(16px);
  border-radius: 12px;
  padding: 15px 30px; /* 缩减内边距 */
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%; /* 撑满底部的 bottom-panel */
}

.advice-box h4 {
  margin: 0 0 10px 0; /* 缩减边距 */
  background: linear-gradient(135deg, #D2A76D 0%, #A67C41 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 1.2rem; /* 缩小字号 */
  letter-spacing: 1px;
}

.advice-content {
  flex: 1;
  overflow-y: auto;
  line-height: 2;
  font-size: 1.1rem;
  color: #c9d1d9;
  letter-spacing: 0.5px;
  padding-right: 15px;
}

.empty-box {
  text-align: center;
  padding: 40px;
  color: #A0A0A0;
}

/* 简单的加载动画 */
.loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 50px 0;
  color: #D2A76D;
  height: 100%;
}
.loader {
  border: 4px solid rgba(210, 167, 109, 0.1);
  border-top: 4px solid #D2A76D; /* 香槟金 */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

.mini-loader {
  border: 3px solid rgba(210, 167, 109, 0.1);
  border-top: 3px solid #D2A76D; /* 香槟金 */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 自定义滚动条 */
.analysis-panel::-webkit-scrollbar {
  width: 6px;
}
.analysis-panel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.analysis-panel::-webkit-scrollbar-thumb {
  background: rgba(210, 167, 109, 0.3);
  border-radius: 3px;
}
.analysis-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(210, 167, 109, 0.5);
}
</style>