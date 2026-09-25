<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const props = defineProps({ id: String })
const room = ref(null)
const tiles = ref([])
const tileId = ref(null)
const calc = ref(null)
const err = ref('')

onMounted(async () => {
  room.value = await getJSON(`/api/rooms/${props.id}`)
  tiles.value = (await getJSON('/api/tiles')).items.filter(t => t.data_quality === 'clean')
  if (tiles.value.length) tileId.value = tiles.value[0].id
})

async function run() {
  err.value = ''
  calc.value = null
  try {
    const qs = new URLSearchParams({
      room_id: props.id,
      tile_id: tileId.value,
      remnant_enabled: 'true',
    })
    calc.value = await getJSON(`/api/estimate?${qs.toString()}`)
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

    <section class="calc-box">
      <h2>测算（含余料门槛）</h2>
      <label>砖型
        <select v-model.number="tileId">
          <option v-for="t in tiles" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
      </label>
      <button @click="run">测算</button>
      <p v-if="err" class="alert">{{ err }}</p>
      <div v-if="calc" class="calc-result">
        <p>净用量 {{ calc.raw_count }} 片；基础订货 {{ calc.base_order_count }} 片</p>
        <p v-if="calc.remnant?.extra_count > 0">
          余料条（沿长 {{ calc.remnant.along_length_mm }} mm / 沿宽 {{ calc.remnant.along_width_mm }} mm，
          门槛 {{ calc.remnant_threshold_mm }} mm）触发加片 +{{ calc.remnant.extra_count }}
        </p>
        <p v-else>余料条均不低于门槛（{{ calc.remnant_threshold_mm }} mm），不另加片。</p>
        <p class="final">加片后订货：<strong>{{ calc.order_count }}</strong> 片</p>
      </div>
    </section>

    <router-link to="/bench">去下单测算台</router-link>
  </div>
</template>
<style scoped>
.calc-box { background: #fff; border-left: 4px solid #27ae60; padding: 0.75rem 1rem; margin: 1rem 0; max-width: 560px; }
.final { font-size: 1.1rem; }
</style>
