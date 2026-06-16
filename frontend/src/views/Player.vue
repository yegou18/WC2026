<template>
  <div class="player-container dashboard-fullscreen">
    <div class="tech-grid"></div>
    <div class="ethereal-glow"></div>

    <div class="header-nav">
      <div class="back-btn" @click="$router.push('/')">
        <el-icon><ArrowLeft /></el-icon> 返回大屏
      </div>
      <div class="page-title">SJB // AI DECISION & PROFIT SYSTEM</div>
      <div class="user-info" v-if="userData">
        <span class="role-badge" :class="userData.user.role">{{ userData.user.role.toUpperCase() }}</span>
        <span class="username">{{ userData.user.username }}</span>
        <el-button size="small" type="danger" plain @click="handleLogout">登出</el-button>
      </div>
    </div>

    <div class="content-wrapper" v-if="userData">
      <!-- 顶部资金数据仪表盘 -->
      <div class="finance-dashboard">
        <div class="finance-card glass-panel">
          <div class="card-icon"><el-icon><Wallet /></el-icon></div>
          <div class="card-data">
            <div class="label">可用余额 (本金+盈利)</div>
            <div class="value highlight">{{ formatMoney(userData.user.balance) }}</div>
          </div>
        </div>
        <div class="finance-card glass-panel">
          <div class="card-icon"><el-icon><DataLine /></el-icon></div>
          <div class="card-data">
            <div class="label">历史总投注</div>
            <div class="value">{{ formatMoney(userData.stats.total_bet) }}</div>
          </div>
        </div>
        <div class="finance-card glass-panel">
          <div class="card-icon"><el-icon><Money /></el-icon></div>
          <div class="card-data">
            <div class="label">累计净盈利</div>
            <div class="value success">{{ formatMoney(userData.stats.total_profit) }}</div>
          </div>
        </div>
        <div class="finance-card glass-panel">
          <div class="card-icon"><el-icon><TrendCharts /></el-icon></div>
          <div class="card-data">
            <div class="label">投注胜率</div>
            <div class="value warning">{{ (userData.stats.win_rate * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </div>

      <!-- 投注记录与策略分析 -->
      <div class="main-panels">
        <!-- 左侧：历史投注记录 -->
        <div class="panel left-panel glass-panel">
          <div class="panel-header">
            <h3>投注追踪记录 // BETTING HISTORY</h3>
          </div>
          <div class="panel-body">
            <el-table 
              :data="userData.bets" 
              style="width: 100%" 
              class="cyber-table"
              :row-class-name="tableRowClassName"
            >
              <el-table-column prop="created_at" label="时间" width="160">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column prop="description" label="项目" min-width="150" />
              <el-table-column prop="amount" label="投注金额" width="120">
                <template #default="scope">
                  <span class="highlight">{{ scope.row.amount }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <span :class="'status-' + scope.row.status">
                    {{ getStatusText(scope.row.status) }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="profit" label="盈利/返还" width="120">
                <template #default="scope">
                  <span :class="scope.row.profit > 0 ? 'text-success' : ''">
                    {{ scope.row.profit > 0 ? '+' + scope.row.profit : scope.row.profit }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <!-- 右侧：AI 策略中心 (预留位) -->
        <div class="panel right-panel glass-panel">
          <div class="panel-header">
            <h3>AI 决策引擎 // STRATEGY CENTER</h3>
          </div>
          <div class="panel-body ai-strategy">
            <div class="strategy-placeholder">
              <div class="radar-scan"></div>
              <p>正在监控赛事赔率波动...</p>
              <p class="sub-text">AI 决策模型将基于您的可用额度与实时赔率，动态生成投注策略。</p>
            </div>
            
            <div class="strategy-card">
              <div class="s-header">
                <span class="s-match">当前阶段建议</span>
                <span class="s-badge">系统提示</span>
              </div>
              <div class="s-content">
                目前系统以搭建数据和玩法框架为主。后期录入真实赔率数据后，AI 将在这里直接输出“重仓/轻仓”、“胜平负”等具体策略指令。
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Wallet, DataLine, Money, TrendCharts } from '@element-plus/icons-vue'

const router = useRouter()
const userData = ref<any>(null)

const fetchUserData = async () => {
  const token = localStorage.getItem('sjb_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const res = await axios.get('http://localhost:10086/api/user/me', {
      headers: { Authorization: token }
    })
    
    if (res.data.status === 'success') {
      userData.value = res.data.data
    } else {
      ElMessage.error(res.data.message)
      if (res.data.message === '未登录') router.push('/login')
    }
  } catch (error: any) {
    if (error.response && error.response.status === 401) {
      router.push('/login')
    } else {
      ElMessage.error('无法获取玩家数据')
    }
  }
}

const handleLogout = () => {
  localStorage.removeItem('sjb_token')
  localStorage.removeItem('sjb_user')
  router.push('/login')
}

const formatMoney = (val: number) => {
  return val ? val.toFixed(2) : '0.00'
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getMonth()+1}-${d.getDate()} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'pending': '未结算',
    'won': '已盈利',
    'lost': '未命中'
  }
  return map[status] || status
}

const tableRowClassName = ({ row }: { row: any }) => {
  if (row.status === 'won') return 'success-row'
  if (row.status === 'lost') return 'error-row'
  return ''
}

onMounted(() => {
  fetchUserData()
})
</script>

<style scoped>
.player-container {
  padding: 30px 40px;
  display: flex;
  flex-direction: column;
  gap: 25px;
  pointer-events: auto; /* 允许点击 */
}

/* 顶部导航 */
.header-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
  border-bottom: 1px solid rgba(210, 167, 109, 0.2);
  padding-bottom: 15px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #A0A0A0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.3s;
}
.back-btn:hover { color: #D2A76D; }

.page-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #D2A76D;
  letter-spacing: 3px;
  text-shadow: 0 0 10px rgba(210, 167, 109, 0.5);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.role-badge {
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: bold;
}
.role-badge.admin { background: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
.role-badge.player { background: rgba(52, 152, 219, 0.2); color: #3498db; border: 1px solid #3498db; }

.username {
  font-weight: bold;
  font-size: 1.1rem;
  color: #E6E6E6;
}

/* 内容区 */
.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 25px;
  z-index: 10;
  flex: 1;
}

/* 资金仪表盘 */
.finance-dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.finance-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 25px 20px;
  background: rgba(30, 26, 23, 0.7);
}

.card-icon {
  font-size: 2.5rem;
  color: #D2A76D;
  opacity: 0.8;
}

.card-data {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.card-data .label {
  color: #A0A0A0;
  font-size: 0.85rem;
}

.card-data .value {
  font-size: 1.8rem;
  font-weight: 900;
  font-family: 'Courier New', Courier, monospace;
}

.value.highlight { color: #D2A76D; text-shadow: 0 0 10px rgba(210, 167, 109, 0.5); }
.value.success { color: #2ecc71; text-shadow: 0 0 10px rgba(46, 204, 113, 0.5); }
.value.warning { color: #f39c12; }

/* 主面板区 */
.main-panels {
  display: flex;
  gap: 25px;
  flex: 1;
  min-height: 0;
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(20, 22, 26, 0.75);
}

.panel-header {
  padding: 15px 20px;
  border-bottom: 1px solid rgba(210, 167, 109, 0.2);
}

.panel-header h3 {
  margin: 0;
  color: #D2A76D;
  font-size: 1.1rem;
  letter-spacing: 1px;
}

.panel-body {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

/* 状态颜色 */
.status-pending { color: #f39c12; }
.status-won { color: #2ecc71; font-weight: bold; }
.status-lost { color: #e74c3c; }
.text-success { color: #2ecc71; font-weight: bold; }

/* AI 策略中心占位 */
.ai-strategy {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.strategy-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  border: 1px dashed rgba(210, 167, 109, 0.3);
  border-radius: 8px;
  background: rgba(30, 26, 23, 0.4);
  text-align: center;
}

.radar-scan {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid #D2A76D;
  position: relative;
  margin-bottom: 15px;
  box-shadow: 0 0 15px rgba(210, 167, 109, 0.4);
}

.radar-scan::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 50%; height: 2px;
  background: #D2A76D;
  transform-origin: left center;
  animation: radar-spin 2s linear infinite;
}

@keyframes radar-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.sub-text {
  font-size: 0.8rem;
  color: #888;
  margin-top: 5px;
}

.strategy-card {
  background: rgba(210, 167, 109, 0.05);
  border: 1px solid rgba(210, 167, 109, 0.2);
  border-radius: 6px;
  padding: 15px;
}

.s-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.s-match {
  font-weight: bold;
  color: #E6E6E6;
}

.s-badge {
  background: rgba(210, 167, 109, 0.2);
  color: #D2A76D;
  padding: 2px 6px;
  font-size: 0.7rem;
  border-radius: 4px;
}

.s-content {
  color: #A0A0A0;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* 覆盖表格样式 */
:deep(.cyber-table) {
  background: transparent !important;
}
:deep(.cyber-table th.el-table__cell) {
  background: rgba(30, 26, 23, 0.6) !important;
  color: #D2A76D !important;
  border-bottom: 1px solid rgba(210, 167, 109, 0.3) !important;
}
:deep(.cyber-table td.el-table__cell) {
  background: transparent !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  color: #E6E6E6;
}
:deep(.cyber-table tr:hover > td.el-table__cell) {
  background: rgba(210, 167, 109, 0.05) !important;
}
</style>
