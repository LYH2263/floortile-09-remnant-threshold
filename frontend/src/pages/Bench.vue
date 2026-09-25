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

const remnantEnabled = ref(false)
const thresholdMm = ref(100)
const extraPieces = ref(2)

function estimateParams(save, note = '') {
  const params = {
    room_id: roomId.value,
    tile_id: tileId.value,
    save,
    note,
    remnant_enabled: remnantEnabled.value,
  }
  if (remnantEnabled.value) {
    params.remnant_threshold_mm = Number(thresholdMm.value)
    params.extra_pieces = Number(extraPieces.value)
  }
  return params
}

onMounted(async () => {
  rooms.value = (await getJSON('/api/rooms')).items.filter(r => r.data_quality === 'clean')
  tiles.value = (await getJSON('/api/tiles')).items.filter(t => t.data_quality === 'clean')
  const settings = await getJSON('/api/settings')
  thresholdMm.value = Number(settings.remnant_threshold_mm)
  extraPieces.value = Number(settings.extra_pieces)
  if (rooms.value.length) roomId.value = rooms.value[0].id
  if (tiles.value.length) tileId.value = tiles.value[0].id
})

async function preview() {
  err.value = ''
  try {
    const p = estimateParams(false)
    const qs = new URLSearchParams({
      room_id: p.room_id,
      tile_id: p.tile_id,
      remnant_enabled: p.remnant_enabled,
    })
    if (p.remnant_threshold_mm !== undefined) qs.set('remnant_threshold_mm', p.remnant_threshold_mm)
    if (p.extra_pieces !== undefined) qs.set('extra_pieces', p.extra_pieces)
    result.value = await getJSON(`/api/estimate?${qs.toString()}`)
  } catch (e) {
    err.value = e.message
    result.value = null
  }
}

async function saveRun() {
  err.value = ''
  try {
    result.value = await postJSON('/api/estimate', estimateParams(true, '前端保存'))
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
    <fieldset class="remnant-box">
      <legend>余料门槛</legend>
      <label class="inline">
        <input type="checkbox" v-model="remnantEnabled"> 启用余料门槛加片
      </label>
      <div v-if="remnantEnabled" class="remnant-fields">
        <label>门槛（mm，&gt;0）
          <input type="number" v-model.number="thresholdMm" min="1" step="1">
        </label>
        <label>固定加片（枚）
          <input type="number" v-model.number="extraPieces" min="0" step="1">
        </label>
        <p class="hint">沿长/沿宽对砖边取模得到余料条；任一条 &gt;0 且小于门槛，订货加一次固定枚数。</p>
      </div>
    </fieldset>
    <button @click="preview">试算</button>
    <button @click="saveRun">保存记录</button>
    <p v-if="err" class="alert">{{ err }}</p>
    <OrderSummary :result="result" />
    <TileGridPreview v-if="result?.layout" :cols="result.layout.cols" :rows="result.layout.rows" :grid-count="result.layout.grid_count" />
  </div>
</template>
<style scoped>
.remnant-box { border: 1px solid #bbb; padding: 0.75rem 1rem; margin: 0.75rem 0; max-width: 560px; }
.inline { display: inline-flex; align-items: center; gap: 0.4rem; }
.remnant-fields { display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-start; margin-top: 0.5rem; }
.remnant-fields input { width: 110px; }
.hint { color: #666; font-size: 0.85rem; flex-basis: 100%; margin: 0.25rem 0 0; }
</style>
