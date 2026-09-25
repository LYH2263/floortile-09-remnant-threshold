<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'
import TileGridPreview from '../components/TileGridPreview.vue'

const props = defineProps({ id: String })
const room = ref(null)
const tiles = ref([])
const tileId = ref(null)
const result = ref(null)
const err = ref('')

onMounted(async () => {
  const [roomData, tileData] = await Promise.all([
    getJSON(`/api/rooms/${props.id}`),
    getJSON('/api/tiles'),
  ])
  room.value = roomData
  tiles.value = tileData.items.filter(t => t.data_quality === 'clean')
  if (tiles.value.length) tileId.value = tiles.value[0].id
})

async function preview() {
  err.value = ''
  result.value = null
  try {
    result.value = await getJSON(
      `/api/estimate?room_id=${props.id}&tile_id=${tileId.value}&remainder_enabled=true`
    )
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page" v-if="room">
    <h1>{{ room.name }}</h1>
    <div v-if="room.data_quality === 'dirty'" class="alert">该房间尺寸异常：{{ room.note }}</div>
    <dl>
      <dt>长度</dt><dd>{{ room.length }} m</dd>
      <dt>宽度</dt><dd>{{ room.width }} m</dd>
      <dt>面积</dt><dd>{{ (room.length * room.width).toFixed(2) }} m²</dd>
    </dl>

    <h2>测算（余料门槛按全局默认）</h2>
    <label>砖型
      <select v-model.number="tileId">
        <option v-for="t in tiles" :key="t.id" :value="t.id">{{ t.name }}</option>
      </select>
    </label>
    <button class="primary" @click="preview">试算</button>
    <p v-if="err" class="alert">{{ err }}</p>
    <OrderSummary :result="result" />
    <TileGridPreview v-if="result?.layout" :cols="result.layout.cols" :rows="result.layout.rows" :grid-count="result.layout.grid_count" />

    <router-link to="/bench">去下单台</router-link>
  </div>
</template>
