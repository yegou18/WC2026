<template>
  <div class="login-container tech-bg">
    <!-- 3D Earth Container (Sketchfab Embed) -->
    <div class="earth-container">
      <iframe 
        id="api-frame"
        title="Earth" 
        frameborder="0" 
        allowfullscreen 
        mozallowfullscreen="true" 
        webkitallowfullscreen="true" 
        allow="autoplay; fullscreen; xr-spatial-tracking" 
        xr-spatial-tracking 
        execution-while-out-of-viewport 
        execution-while-not-rendered 
        web-share 
        src="https://sketchfab.com/models/37249acae18b406d8c1c160d7c0bc8e6/embed?autostart=1&ui_theme=dark&dnt=1&ui_controls=0&ui_infos=0&ui_inspector=0&ui_watermark=0&ui_hint=0&ui_help=0&camera=0&auto_spin=0.05"
      ></iframe>
    </div>
    
    <div class="login-box glass-panel">
      <div class="login-header">
        <h1 class="title-top">2026美加墨世界杯</h1>
        <h1 class="title-bottom">投注决策辅助系统</h1>
        <p>WC2026 DECISION SUPPORT ENGINE</p>
      </div>
      
      <el-form :model="form" class="login-form" @keyup.enter="handleLogin">
        <div class="input-group">
          <label>USER IDENTITY [用户标识]</label>
          <el-input 
              v-model="form.username" 
              placeholder="输入玩家ID " 
              class="cyber-input"
            >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="input-group">
          <label>SECURITY KEY [安全密钥]</label>
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="输入验证密钥" 
            class="cyber-input"
            show-password
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </div>
        
        <el-button type="primary" class="cyber-btn login-btn" :loading="loading" @click="handleLogin">
          <span>{{ loading ? '登入中...' : '登入系统' }}</span>
        </el-button>
      </el-form>
      
      <div class="login-footer">
        <p class="warning-text">免责声明：本系统各项预测及策略仅供内部测试与研究参考，严禁用于非法用途。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
let spinInterval: any = null

const form = ref({
  username: '',
  password: ''
})

onMounted(() => {
  // Initialize Sketchfab Viewer API
  const iframe = document.getElementById('api-frame') as HTMLIFrameElement
  if (!iframe) return

  // 必须确保 iframe 完全加载后再初始化 API，避免 Uncaught No API 错误
  // @ts-ignore
  const client = new window.Sketchfab(iframe)

  client.init('37249acae18b406d8c1c160d7c0bc8e6', {
    success: function onSuccess(api: any) {
      api.start()
      api.addEventListener('viewerready', function() {
        console.log('Sketchfab viewer is ready')
        
        // 使用您指定的绝佳初始摄像机视角
        let defaultPos = [28501.8172, 41025.8881, 1964.6391]
        let defaultTgt = [5.1603, -453.4194, 455.0356]
        
        // 更改了缓存 key，以确保旧的缓存不会覆盖这次您新设置的完美视角
        const savedCamera = localStorage.getItem('sjb_earth_camera_v3')
        if (savedCamera) {
          try {
            const { position, target } = JSON.parse(savedCamera) 
            defaultPos = position
            defaultTgt = target
          } catch (e) {}
        }
        
        api.setCameraLookAt(defaultPos, defaultTgt, 0)

        // ==========================================
        // 实现 3D 复杂有机轨道自转（多轴随机漂浮感，固定中心）
        // ==========================================
        let currentPos = [...defaultPos]
        let currentTarget = [...defaultTgt]
        let isUserInteracting = false
        let interactionTimeout: any = null
        let orbitTime = 0
        
        // 基础球坐标参数
        let r = 0, baseTheta = 0, basePhi = 0;

        const updateSpherical = () => {
          let dx = currentPos[0] - currentTarget[0]
          let dy = currentPos[1] - currentTarget[1]
          let dz = currentPos[2] - currentTarget[2]
          r = Math.sqrt(dx*dx + dy*dy + dz*dz)
          baseTheta = Math.atan2(dz, dx)
          basePhi = Math.acos(dy / r)
        }
        updateSpherical()
        
        // 使用 DOM 事件精准判断用户是否在拖动地球
        const earthContainer = document.querySelector('.earth-container')
        if (earthContainer) {
          earthContainer.addEventListener('pointerdown', () => {
            isUserInteracting = true
            clearTimeout(interactionTimeout)
          })
          earthContainer.addEventListener('pointerup', () => {
            interactionTimeout = setTimeout(() => {
              // 恢复自转前，以用户最后停留的位置为新基准
              api.getCameraLookAt(function(err: any, camera: any) {
                if (!err) {
                  currentPos = camera.position
                  currentTarget = camera.target
                  updateSpherical()
                  orbitTime = 0 // 重置时间，使得动画平滑过渡不跳跃
                  isUserInteracting = false
                }
              })
            }, 2000)
          })
        }

        spinInterval = setInterval(() => {
          if (isUserInteracting) return
          
          orbitTime += 1
          
          // 水平持续基础旋转
          baseTheta -= 0.0015 
          
          // 引入多个不同周期的正弦波，创造出无规律、平滑的随机漂浮感（Lissajous 轨道）
          // 1. 对仰角 (Phi) 进行平滑的上下浮动
          let phiDrift = Math.sin(orbitTime * 0.002) * 0.15 + Math.sin(orbitTime * 0.0013) * 0.1
          let targetPhi = basePhi + phiDrift
          // 限制在两极视角内，避免发生万向节死锁翻转
          targetPhi = Math.max(0.1, Math.min(Math.PI - 0.1, targetPhi))

          // 2. 对半径 (Distance) 进行微小的呼吸缩放
          let rDrift = Math.sin(orbitTime * 0.0017) * (r * 0.03)
          let targetR = r + rDrift

          // 3. 对水平旋转速度增加一点点随机快慢变化
          let thetaDrift = Math.sin(orbitTime * 0.0025) * 0.08
          let targetTheta = baseTheta + thetaDrift
          
          let nextPos = [
            currentTarget[0] + targetR * Math.sin(targetPhi) * Math.cos(targetTheta),
            currentTarget[1] + targetR * Math.cos(targetPhi),
            currentTarget[2] + targetR * Math.sin(targetPhi) * Math.sin(targetTheta)
          ]

          // 即时生效，避免摄像机过渡动画造成的延迟和抖动
          api.setCameraLookAt(nextPos, currentTarget, 0)
        }, 30)

        // 监听摄像机移动事件，每次移动停止后将视角坐标输出到控制台
        api.addEventListener('camerastop', function() {
          api.getCameraLookAt(function(err: any, camera: any) {
            if (!err) {
              const pos = camera.position.map((v: number) => Number(v.toFixed(4)))
              const tgt = camera.target.map((v: number) => Number(v.toFixed(4)))
              console.log('============ 当前摄像机绝佳视角坐标 ============')
              console.log(`api.setCameraLookAt([${pos.join(', ')}], [${tgt.join(', ')}], 0)`)
              console.log('================================================')
              // 保存到本地存储 v3
              localStorage.setItem('sjb_earth_camera_v3', JSON.stringify({ position: pos, target: tgt }))
            }
          })
        })
      })
    },
    error: function onError() {
      console.log('Sketchfab API error')
    },
    autostart: 1,
    autospin: 0, // 彻底关闭自带动画，因为它的动画会同时驱动整个地球模型产生奇怪的旋转冲突
    animation_speed: 0.2, // 单独控制模型内部动画片段的播放速度（使得云层飘得非常慢）
    ui_theme: 'dark',
    dnt: 1,
    ui_controls: 0,
    ui_infos: 0,
    ui_inspector: 0,
    ui_watermark: 0,
    ui_hint: 0,
    ui_help: 0,
    transparent: 1
  })
})

onBeforeUnmount(() => {
  if (spinInterval) {
    clearInterval(spinInterval)
  }
})

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户ID和密钥')
    return
  }
  
  loading.value = true
  try {
    const res = await axios.post('http://localhost:10086/api/login', form.value)
    if (res.data.status === 'success') {
      ElMessage.success('连接已建立 / ACCESS GRANTED')
      localStorage.setItem('sjb_token', res.data.token)
      localStorage.setItem('sjb_user', JSON.stringify(res.data.user))
      router.push('/')
    } else {
      ElMessage.error(res.data.message || '验证失败')
    }
  } catch (error) {
    ElMessage.error('系统节点无法连接，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #05070a; /* Darker background to make earth pop */
  position: relative;
  overflow: hidden;
  pointer-events: none; /* 外层容器禁用指针事件 */
}

.earth-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: auto; /* 恢复鼠标交互，让用户可以拖动地球 */
}

.earth-container iframe {
  width: 100%;
  height: 100%;
  border: none;
  /* 使用 scale 放大 iframe 内容，去除 Sketchfab 上下自带的控制栏空白区域 */
  transform: scale(1.1);
  transform-origin: center center;
}

/* Add a subtle dark vignette overlay to blend edges */
.earth-container::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle, transparent 40%, rgba(5, 7, 10, 0.8) 100%);
  pointer-events: none; /* 暗角遮罩必须穿透鼠标事件 */
}

.login-box {
  width: 384px; /* 缩小 20% (480px * 0.8) */
  background: rgba(20, 22, 26, 0.85);
  padding: 40px; /* 缩小 20% (50px * 0.8) */
  border-radius: 12px;
  border: 1px solid rgba(210, 167, 109, 0.3);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(210, 167, 109, 0.05);
  z-index: 10;
  position: relative;
  backdrop-filter: blur(15px);
  pointer-events: auto; /* 确保登录框自身也能正常点击输入 */
}

.login-box::before {
  content: '';
  position: absolute;
  top: -1px; left: -1px; right: -1px; bottom: -1px;
  border-radius: 12px;
  padding: 1px;
  background: linear-gradient(135deg, #D2A76D 0%, transparent 40%, transparent 60%, #D2A76D 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.login-header {
  text-align: center;
  margin-bottom: 28px; /* 缩小 20% */
  border-bottom: 1px solid rgba(210, 167, 109, 0.2);
  padding-bottom: 20px; /* 缩小 20% */
}

.login-header h1 {
  margin: 0;
  color: #D2A76D;
  text-shadow: 0 0 10px rgba(210, 167, 109, 0.5);
}

.title-top {
  font-size: 1.1rem;
  letter-spacing: 4px;
  opacity: 0.9;
  margin-bottom: 6px !important;
}

.title-bottom {
  font-size: 1.4rem;
  letter-spacing: 2px;
  font-weight: 600;
}

.login-header p {
  margin: 8px 0 0;
  color: #A0A0A0;
  font-size: 0.75rem; /* 缩小 20% */
  letter-spacing: 1.5px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 缩小 20% */
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  color: #D2A76D;
  font-size: 0.8rem;
  letter-spacing: 2px;
}

:deep(.cyber-input .el-input__wrapper) {
  background-color: rgba(10, 12, 15, 0.6) !important;
  box-shadow: 0 0 0 1px rgba(210, 167, 109, 0.2) inset !important;
  padding: 0 12px;
}

:deep(.cyber-input .el-input__inner) {
  color: #E6E6E6 !important;
  height: 36px; /* 缩小 20% (45px * 0.8) */
  font-size: 0.8rem;
}

:deep(.cyber-input .el-input__prefix) {
  color: #D2A76D;
  font-size: 1.2rem;
}

.login-btn {
  margin-top: 16px;
  height: 40px; /* 缩小 20% (50px * 0.8) */
  font-size: 0.88rem; /* 缩小 20% (1.1rem * 0.8) */
  letter-spacing: 2.4px;
  background: linear-gradient(90deg, rgba(210, 167, 109, 0.1), rgba(210, 167, 109, 0.3), rgba(210, 167, 109, 0.1));
  border: 1px solid #D2A76D;
  color: #D2A76D;
}

.login-btn:hover {
  background: rgba(210, 167, 109, 0.3);
  box-shadow: 0 0 15px rgba(210, 167, 109, 0.5);
  color: #fff;
}

.login-footer {
  margin-top: 25px; /* 缩小 20% */
  text-align: center;
  padding-top: 15px; /* 缩小 20% */
  border-top: 1px dashed rgba(210, 167, 109, 0.2);
}

.warning-text {
  color: #8c8c8c; /* 改为柔和的灰色，符合免责声明的常规视觉 */
  font-size: 0.65rem; /* 缩小 20% */
  letter-spacing: 1px;
  margin-bottom: 0;
}
</style>
