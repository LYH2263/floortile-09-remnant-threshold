<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'
import TileGridPreview from '../components/TileGridPreview.vue'

const rooms = ref([])
const tiles = ref([])
const roomId = ref(1)
const tileId = ref(1)
const result = ref(null)
const err = ref('')
const savedMsg = ref('')
const thresholdOn = ref(false)
const thresholdMm = ref(100)
const extraPieces = ref(2)

onMounted(async () => {
  const [roomData, tileData, settings] = await Promise.all([
    getJSON('/api/rooms'),
    getJSON('/api/tiles'),
    getJSON('/api/settings'),
  ])
  rooms.value = roomData.items.filter(r => r.data_quality === 'clean')
  tiles.value = tileData.items.filter(t => t.data_quality === 'clean')
  if (rooms.value.length) roomId.value = rooms.value[0].id
  if (tiles.value.length) tileId.value = tiles.value[0].id
  thresholdMm.value = Number(settings.remainder_threshold_mm)
  extraPieces.value = Number(settings.remainder_extra_pieces)
})

function remainderQuery() {
  if (!thresholdOn.value) return ''
  return `&remainder_enabled=true&remainder_threshold_mm=${thresholdMm.value}&remainder_extra_pieces=${extraPieces.value}`
}

function remainderBody() {
  if (!thresholdOn.value) return {}
  return {
    remainder_enabled: true,
    remainder_threshold_mm: Number(thresholdMm.value),
    remainder_extra_pieces: Number(extraPieces.value),
  }
}

async function preview() {
  err.value = ''
  savedMsg.value = ''
  try {
    result.value = await getJSON(`/api/estimate?room_id=${roomId.value}&tile_id=${tileId.value}${remainderQuery()}`)
  } catch (e) {
    err.value = e.message
    result.value = null
  }
}

async function saveRun() {
  err.value = ''
  savedMsg.value = ''
  try {
    result.value = await postJSON('/api/estimate', {
      room_id: roomId.value,
      tile_id: tileId.value,
      save: true,
      note: '前端保存',
      ...remainderBody(),
    })
    savedMsg.value = `已保存 #${result.value.run_id}`
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>下单测算</h1>
    <label>房间 <select v-model.number="roomId"><option v-for="r in rooms" :key="r.id" :value="r.id">{{ r.name }}</option></select></label>
    <label>砖型 <select v-model.number="tileId"><option v-for="t in tiles" :key="t.id" :value="t.id">{{ t.name }}</option></select></label>
    <label class="switch-row">
      <input type="checkbox" v-model="thresholdOn">
      启用余料门槛
    </label>
    <div v-if="thresholdOn" class="field-inline">
      <label>余料门槛 <input type="number" min="1" step="1" v-model.number="thresholdMm"> mm</label>
      <label>每条加片 <input type="number" min="1" step="1" v-model.number="extraPieces"> 枚</label>
    </div>
    <button class="primary" @click="preview">试算</button>
    <button @click="saveRun">保存记录</button>
    <p v-if="err" class="alert">{{ err }}</p>
    <p v-if="savedMsg" class="ok">{{ savedMsg }}</p>
    <OrderSummary :result="result" />
    <TileGridPreview v-if="result?.layout" :cols="result.layout.cols" :rows="result.layout.rows" :grid-count="result.layout.grid_count" />
  </div>
</template>
