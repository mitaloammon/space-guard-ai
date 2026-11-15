<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const telemetry = ref({
  oxygen: 86,
  pressure_psi: 4.3,
  temperature_celsius: 28.1,
  battery_level: 62,
  radiation_rate_msv_h: 0.42,
  communication_status: 'connected',
})

const status = ref({
  mode: 'manual',
  active_scenario: null,
  scenario_status: 'idle',
  execution_start_time: null,
  telemetry: { ...telemetry.value },
  thresholds: {},
})

const scenarios = ref<any[]>([])
const alerts = ref<any[]>([])
const manualForm = ref({ ...telemetry.value })
const socketState = ref('disconnected')

const manualFields = [
  { key: 'oxygen', label: 'Oxygen', unit: '%', min: 0, max: 100, step: 1 },
  { key: 'pressure_psi', label: 'Pressure', unit: 'psi', min: 0, max: 20, step: 0.1 },
  { key: 'temperature_celsius', label: 'Temperature', unit: '°C', min: -80, max: 120, step: 0.1 },
  { key: 'battery_level', label: 'Battery', unit: '%', min: 0, max: 100, step: 1 },
  { key: 'radiation_rate_msv_h', label: 'Radiation', unit: 'mSv/h', min: 0, max: 25, step: 0.1 },
  { key: 'communication_status', label: 'Communication', unit: '', options: ['connected', 'disconnected'] },
] as const

let socket: WebSocket | null = null

async function fetchJson(path: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || 'Request failed')
  }

  return response.json()
}

async function refreshState() {
  const [statusResult, scenarioResult, alertResult] = await Promise.all([
    fetchJson('/api/v1/simulation/status'),
    fetchJson('/api/v1/simulation/scenarios'),
    fetchJson('/api/v1/alerts'),
  ])

  status.value = statusResult
  telemetry.value = statusResult.telemetry
  manualForm.value = { ...statusResult.telemetry }
  scenarios.value = scenarioResult.scenarios
  alerts.value = alertResult.alerts
}

function startSocket() {
  if (socket) return

  const wsUrl = `${API_BASE.replace(/^http/, 'ws')}/ws/telemetry`
  socket = new WebSocket(wsUrl)

  socket.addEventListener('open', () => {
    socketState.value = 'connected'
  })

  socket.addEventListener('close', () => {
    socketState.value = 'disconnected'
    socket = null
  })

  socket.addEventListener('message', (event) => {
    const payload = JSON.parse(event.data)
    if (
      payload.type === 'telemetry.updated' ||
      payload.type === 'simulation.started' ||
      payload.type === 'simulation.paused' ||
      payload.type === 'simulation.resumed' ||
      payload.type === 'simulation.stopped' ||
      payload.type === 'simulation.reset' ||
      payload.type === 'connection_established'
    ) {
      refreshState()
    }
  })
}

async function startScenario(scenarioId: string) {
  await fetchJson(`/api/v1/simulation/scenarios/${scenarioId}/start`, { method: 'POST' })
  await refreshState()
}

async function pauseScenario() {
  if (!status.value.active_scenario) return
  await fetchJson(`/api/v1/simulation/scenarios/${status.value.active_scenario}/pause`, { method: 'POST' })
  await refreshState()
}

async function resumeScenario() {
  if (!status.value.active_scenario) return
  await fetchJson(`/api/v1/simulation/scenarios/${status.value.active_scenario}/resume`, { method: 'POST' })
  await refreshState()
}

async function stopScenario() {
  await fetchJson('/api/v1/simulation/stop', { method: 'POST' })
  await refreshState()
}

async function resetSimulation() {
  await fetchJson('/api/v1/simulation/reset', { method: 'POST' })
  await refreshState()
}

async function submitManualUpdate() {
  const payload: Record<string, any> = {}

  for (const field of manualFields) {
    if (field.key === 'communication_status') {
      payload.communication_status = manualForm.value.communication_status
      continue
    }

    const value = manualForm.value[field.key] as number | string | null | undefined
    const isBlankString = typeof value === 'string' && value.trim() === ''
    if (value !== undefined && value !== null && !isBlankString) {
      payload[field.key] = Number(value)
    }
  }

  await fetchJson('/api/v1/simulation/telemetry', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })

  await refreshState()
}

const activeAlerts = computed(() => alerts.value.filter((alert) => alert.status === 'active'))

onMounted(() => {
  refreshState()
  startSocket()
})

onUnmounted(() => {
  if (socket) {
    socket.close()
    socket = null
  }
})
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand-block">
        <p class="eyebrow">Mission systems</p>
        <h1>SPACE GUARD AI</h1>
      </div>
      <nav class="topnav" aria-label="Primary navigation">
        <a href="#overview">Overview</a>
        <a href="#telemetry">Telemetry</a>
        <a href="#simulation">Simulation</a>
        <a href="#alerts">Alerts</a>
        <a href="#sources">Sources</a>
      </nav>
    </header>

    <main class="content">
      <section id="overview" class="hero-panel panel">
        <div>
          <p class="eyebrow">Mission context</p>
          <h2>Simulation foundation</h2>
        </div>
        <div class="status-grid">
          <article>
            <span>Mission</span>
            <strong>Mission-001</strong>
          </article>
          <article>
            <span>Body</span>
            <strong>Mars</strong>
          </article>
          <article>
            <span>Telemetry</span>
            <strong>Simulated</strong>
          </article>
          <article>
            <span>Simulation</span>
            <strong>{{ status.mode }}</strong>
          </article>
        </div>
      </section>

      <section id="telemetry" class="panel metrics-panel">
        <div class="section-header">
          <p class="eyebrow">Telemetry</p>
          <h3>Core parameters</h3>
        </div>
        <div class="metric-grid">
          <div class="metric-card">
            <label>Oxygen</label>
            <strong>{{ telemetry.oxygen.toFixed(1) }}%</strong>
          </div>
          <div class="metric-card">
            <label>Pressure</label>
            <strong>{{ telemetry.pressure_psi.toFixed(1) }} psi</strong>
          </div>
          <div class="metric-card">
            <label>Temperature</label>
            <strong>{{ telemetry.temperature_celsius.toFixed(1) }} °C</strong>
          </div>
          <div class="metric-card">
            <label>Battery</label>
            <strong>{{ telemetry.battery_level.toFixed(1) }}%</strong>
          </div>
          <div class="metric-card">
            <label>Radiation</label>
            <strong>{{ telemetry.radiation_rate_msv_h.toFixed(2) }} mSv/h</strong>
          </div>
          <div class="metric-card">
            <label>Link</label>
            <strong>{{ telemetry.communication_status }}</strong>
          </div>
        </div>
      </section>

      <section id="simulation" class="panel simulation-panel">
        <div class="section-header">
          <p class="eyebrow">Simulation Control</p>
          <h3>Mission sandbox</h3>
        </div>

        <div class="simulation-layout">
          <div class="scenario-box">
            <div class="sim-state-row">
              <span class="state-badge">{{ status.mode }}</span>
              <span class="state-meta">{{ status.active_scenario || 'No scenario' }} · {{ status.scenario_status }}</span>
            </div>

            <div class="scenario-actions">
              <button type="button" class="secondary" @click="resetSimulation">Reset baseline</button>
              <button type="button" class="secondary" @click="pauseScenario" :disabled="!status.active_scenario || status.scenario_status !== 'running'">Pause</button>
              <button type="button" class="secondary" @click="resumeScenario" :disabled="!status.active_scenario || status.scenario_status !== 'paused'">Resume</button>
              <button type="button" class="secondary danger" @click="stopScenario">Stop</button>
            </div>

            <ul class="scenario-list">
              <li v-for="scenario in scenarios" :key="scenario.id">
                <div>
                  <strong>{{ scenario.name }}</strong>
                  <small>{{ scenario.description }}</small>
                </div>
                <button type="button" class="scenario-start" @click="startScenario(scenario.id)">Start</button>
              </li>
            </ul>
          </div>

          <div class="manual-box">
            <div class="manual-header">
              <div>
                <p class="eyebrow">Manual adjustment</p>
                <h4>Telemetry controls</h4>
              </div>
              <span class="ws-indicator" :class="{ connected: socketState === 'connected' }">WS {{ socketState }}</span>
            </div>

            <form class="manual-form" @submit.prevent="submitManualUpdate">
              <div class="field-grid">
                <label v-for="field in manualFields" :key="field.key" class="field">
                  <span>{{ field.label }}</span>

                  <select v-if="field.key === 'communication_status'" v-model="manualForm.communication_status">
                    <option value="connected">Connected</option>
                    <option value="disconnected">Disconnected</option>
                  </select>

                  <input
                    v-else
                    v-model.number="manualForm[field.key]"
                    type="number"
                    :min="field.min"
                    :max="field.max"
                    :step="field.step"
                  />
                </label>
              </div>

              <button type="submit" class="primary-button">Apply manual update</button>
            </form>
          </div>
        </div>
      </section>

      <div class="lower-grid">
        <section id="alerts" class="panel">
          <div class="section-header">
            <p class="eyebrow">Alert status</p>
            <h3>Operational watch</h3>
          </div>
          <ul class="alert-list">
            <li v-for="alert in activeAlerts" :key="alert.id">
              <span class="dot" :class="alert.severity === 'critical' ? 'warning' : 'info'"></span>
              <div>
                <strong>{{ alert.alert_type }}</strong>
                <small>{{ alert.description }}</small>
              </div>
            </li>
            <li v-if="activeAlerts.length === 0"><span class="dot ok"></span>No active alerts</li>
          </ul>
        </section>

        <section id="sources" class="panel">
          <div class="section-header">
            <p class="eyebrow">External sources</p>
            <h3>Integration registry</h3>
          </div>
          <ul class="source-list">
            <li><span>MEDA</span><em>Mock adapter</em></li>
            <li><span>HiRISE</span><em>Architected</em></li>
            <li><span>PDS</span><em>Registry only</em></li>
          </ul>
        </section>
      </div>
    </main>
  </div>
</template>
