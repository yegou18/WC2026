<template>
  <div class="bracket-page">
    <div class="tech-grid"></div>
    <div class="ethereal-glow"></div>
    
    <div class="header-action">
      <el-button type="info" plain @click="goBack" class="back-btn">&lt; 返回大屏指挥中心</el-button>
    </div>
    
    <div class="bracket-title">
      <h1 class="glow-text">WC2026 淘汰赛对阵形势</h1>
      <p>KNOCKOUT STAGE BRACKET</p>
    </div>

    <div class="bracket-container">
      <!-- LEFT HALF -->
      <div class="bracket-half left-half">
        <div class="round round-16">
          <div class="round-title">ROUND OF 16 <span class="sub-title">1/8决赛</span></div>
          <div class="match-pair" v-for="(match, i) in left16" :key="'l16-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="round round-8">
          <div class="round-title">QUARTER-FINALS <span class="sub-title">1/4决赛</span></div>
          <div class="match-pair" v-for="(match, i) in left8" :key="'l8-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="round round-4">
          <div class="round-title">SEMI-FINALS <span class="sub-title">半决赛</span></div>
          <div class="match-single" v-for="(match, i) in left4" :key="'l4-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CENTER FINAL -->
      <div class="bracket-center">
        <div class="trophy-container">
          <el-icon class="trophy-icon"><Trophy /></el-icon>
        </div>
        <div class="final-match glass-panel">
           <div class="round-title-final">FINAL <span class="sub-title">决赛</span></div>
           <div class="match-info-pill">
             <span class="group">A组</span>
             <span class="time">2026-07-19 03:00</span>
           </div>
           <div class="team-line">
             <div class="team-info">
               <img v-if="getFlagUrl(finalMatch.t1)" :src="getFlagUrl(finalMatch.t1)" class="team-flag" />
               <div v-else class="flag-placeholder"></div>
               <span class="t-name">{{ finalMatch.t1 }}</span>
             </div>
             <span class="t-vs">VS</span>
             <div class="team-info right-info">
               <span class="t-name">{{ finalMatch.t2 }}</span>
               <img v-if="getFlagUrl(finalMatch.t2)" :src="getFlagUrl(finalMatch.t2)" class="team-flag" />
               <div v-else class="flag-placeholder"></div>
             </div>
           </div>
           <el-button type="primary" class="cyber-btn" disabled>启动分析引擎</el-button>
        </div>
      </div>

      <!-- RIGHT HALF -->
      <div class="bracket-half right-half">
        <div class="round round-4">
          <div class="round-title">SEMI-FINALS <span class="sub-title">半决赛</span></div>
          <div class="match-single" v-for="(match, i) in right4" :key="'r4-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="round round-8">
          <div class="round-title">QUARTER-FINALS <span class="sub-title">1/4决赛</span></div>
          <div class="match-pair" v-for="(match, i) in right8" :key="'r8-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="round round-16">
          <div class="round-title">ROUND OF 16 <span class="sub-title">1/8决赛</span></div>
          <div class="match-pair" v-for="(match, i) in right16" :key="'r16-'+i">
            <div class="match-node">
              <div class="match-box glass-panel">
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t1)" :src="getFlagUrl(match.t1)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t1 }}</span>
                  </div>
                  <span class="t-score">{{ match.s1 }}</span>
                </div>
                <div class="team-line">
                  <div class="team-info">
                    <img v-if="getFlagUrl(match.t2)" :src="getFlagUrl(match.t2)" class="team-flag" />
                    <div v-else class="flag-placeholder"></div>
                    <span class="t-name">{{ match.t2 }}</span>
                  </div>
                  <span class="t-score">{{ match.s2 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Trophy } from '@element-plus/icons-vue'
import { getFlagUrl } from '../utils/countryMap'

const router = useRouter()

const goBack = () => {
  router.push('/')
}

// 模拟的淘汰赛数据，用于展示排版和国旗效果
const left16 = [
  { t1: '阿根廷', t2: '德国', s1: '-', s2: '-' },
  { t1: '巴西', t2: '意大利', s1: '-', s2: '-' },
  { t1: '美国', t2: '日本', s1: '-', s2: '-' },
  { t1: '法国', t2: '荷兰', s1: '-', s2: '-' }
]

const left8 = [
  { t1: '阿根廷', t2: '巴西', s1: '-', s2: '-' },
  { t1: '中国', t2: '中国', s1: '-', s2: '-' } // 效果图上的假数据
]

const left4 = [
  { t1: '阿根廷', t2: '中国', s1: '89', s2: '80' }
]

const right16 = [
  { t1: '西班牙', t2: '葡萄牙', s1: '-', s2: '-' },
  { t1: '英格兰', t2: '克罗地亚', s1: '-', s2: '-' },
  { t1: '比利时', t2: '瑞士', s1: '-', s2: '-' },
  { t1: '哥伦比亚', t2: '乌拉圭', s1: '-', s2: '-' }
]

const right8 = [
  { t1: '西班牙', t2: '英格兰', s1: '-', s2: '-' },
  { t1: '日本', t2: '韩国', s1: '-', s2: '-' }
]

const right4 = [
  { t1: '西班牙', t2: '日本', s1: '81', s2: '75' }
]

const finalMatch = { t1: '球队A', t2: '球队B', s1: '-', s2: '-' }

</script>

<style scoped>
.bracket-page {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  color: #fff;
  overflow: hidden;
  background: #0d1117; /* 兜底背景 */
}

/* 背景特效与大屏完全一致 */
.tech-grid {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: 
    linear-gradient(rgba(210, 167, 109, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(210, 167, 109, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
  pointer-events: none;
}

.ethereal-glow {
  position: absolute;
  top: -10%;
  left: 50%;
  transform: translateX(-50%);
  width: 1600px;
  height: 1200px;
  background: radial-gradient(ellipse at center, rgba(210, 167, 109, 0.08) 0%, transparent 60%);
  z-index: 0;
  pointer-events: none;
}

.header-action {
  position: relative;
  z-index: 10;
  padding: 20px 40px;
}

.back-btn {
  background: rgba(20, 22, 26, 0.8) !important;
  border: 1px solid rgba(210, 167, 109, 0.4) !important;
  color: #D2A76D !important;
  backdrop-filter: blur(10px);
}
.back-btn:hover {
  background: rgba(210, 167, 109, 0.2) !important;
  box-shadow: 0 0 15px rgba(210, 167, 109, 0.4);
}

.bracket-title {
  text-align: center;
  margin-top: -10px;
  margin-bottom: 20px;
  z-index: 10;
}
.bracket-title h1 {
  font-size: 28px;
  color: #D2A76D;
  margin: 0;
  letter-spacing: 3px;
  text-shadow: 0 0 20px rgba(210, 167, 109, 0.5);
}
.bracket-title p {
  margin: 5px 0 0 0;
  color: #A0A0A0;
  font-size: 14px;
  letter-spacing: 5px;
}

/* 核心支架区 */
.bracket-container {
  display: flex;
  justify-content: center;
  align-items: stretch;
  flex: 1;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  z-index: 10;
  padding: 0 40px 40px;
}

.bracket-half {
  display: flex;
  flex: 1;
}

.left-half { flex-direction: row; }
.right-half { flex-direction: row; }

.round {
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}

.round-title {
  text-align: left;
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
  opacity: 0.9;
  height: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 5px;
}
.right-half .round-title {
  text-align: right;
}
.sub-title {
  color: #A0A0A0;
  font-size: 12px;
  font-weight: normal;
  float: right;
}
.right-half .sub-title {
  float: left;
}

.match-pair {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex: 1;
  position: relative;
}

.left-half .match-pair { margin-right: 30px; }
.right-half .match-pair { margin-left: 30px; }

/* 连线逻辑 */
.left-half .match-pair::after {
  content: '';
  position: absolute;
  right: -15px;
  top: 25%;
  bottom: 25%;
  width: 15px;
  border-right: 2px solid rgba(210, 167, 109, 0.4);
  border-top: 2px solid rgba(210, 167, 109, 0.4);
  border-bottom: 2px solid rgba(210, 167, 109, 0.4);
  z-index: 0;
}
.left-half .match-pair::before {
  content: '';
  position: absolute;
  right: -30px;
  top: 50%;
  width: 15px;
  border-top: 2px solid rgba(210, 167, 109, 0.4);
  z-index: 0;
}

.right-half .match-pair::after {
  content: '';
  position: absolute;
  left: -15px;
  top: 25%;
  bottom: 25%;
  width: 15px;
  border-left: 2px solid rgba(210, 167, 109, 0.4);
  border-top: 2px solid rgba(210, 167, 109, 0.4);
  border-bottom: 2px solid rgba(210, 167, 109, 0.4);
  z-index: 0;
}
.right-half .match-pair::before {
  content: '';
  position: absolute;
  left: -30px;
  top: 50%;
  width: 15px;
  border-top: 2px solid rgba(210, 167, 109, 0.4);
  z-index: 0;
}

/* 半决赛单场连线 */
.match-single {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex: 1;
  position: relative;
}
.left-half .match-single { margin-right: 30px; }
.left-half .match-single::after {
  content: '';
  position: absolute;
  right: -30px;
  top: 50%;
  width: 30px;
  border-top: 2px solid rgba(210, 167, 109, 0.4);
}
.right-half .match-single { margin-left: 30px; }
.right-half .match-single::after {
  content: '';
  position: absolute;
  left: -30px;
  top: 50%;
  width: 30px;
  border-top: 2px solid rgba(210, 167, 109, 0.4);
}

.match-node {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
  height: 100%;
}

.match-box {
  width: 130px;
  background: rgba(20, 22, 26, 0.85);
  border: 1px solid rgba(210, 167, 109, 0.3);
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  cursor: pointer;
}
.match-box:hover {
  transform: scale(1.05);
  border-color: #D2A76D;
  box-shadow: 0 0 20px rgba(210, 167, 109, 0.5);
  background: rgba(30, 32, 38, 0.95);
  z-index: 10;
}

.team-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  font-size: 13px;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.team-flag {
  width: 24px;
  height: 16px;
  object-fit: cover;
  border-radius: 2px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.flag-placeholder {
  width: 24px;
  height: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}
.team-line:first-child {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.t-name {
  color: #fff;
}
.t-score {
  font-weight: bold;
  color: #D2A76D;
}

.bracket-center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
  min-width: 180px;
}

.trophy-container {
  margin-bottom: 30px;
  animation: float 4s ease-in-out infinite;
}

.trophy-icon {
  font-size: 80px;
  color: #D2A76D;
  filter: drop-shadow(0 0 20px rgba(210, 167, 109, 0.6));
}

.final-match {
  width: 220px;
  background: rgba(30, 32, 38, 0.9);
  border: 1px solid rgba(210, 167, 109, 0.5);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(210, 167, 109, 0.1);
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.round-title-final {
  font-size: 16px;
  font-weight: bold;
  color: #D2A76D;
  text-align: center;
}

.match-info-pill {
  display: flex;
  gap: 12px;
  background: rgba(20, 22, 26, 0.8);
  border: 1px solid rgba(210, 167, 109, 0.3);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.75rem;
}
.group { color: #A0A0A0; }
.time { color: #fff; }

.final-match .team-line {
  width: 100%;
  border-bottom: none;
}

.final-match .t-vs {
  color: #D2A76D;
  font-weight: bold;
  font-style: italic;
  padding: 0 10px;
}

.right-info {
  flex-direction: row-reverse;
}

.cyber-btn {
  background: rgba(210, 167, 109, 0.1);
  border: 1px solid #D2A76D;
  color: #D2A76D;
  margin-top: 10px;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
  100% { transform: translateY(0px); }
}
</style>