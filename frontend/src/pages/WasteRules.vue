<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const settings = ref({})
const thresholdMm = ref(100)
const extraPieces = ref(2)
const msg = ref('')
const err = ref('')

onMounted(async () => {
  settings.value = await getJSON('/api/settings')
  thresholdMm.value = Number(settings.value.remnant_threshold_mm)
  extraPieces.value = Number(settings.value.extra_pieces)
})

async function save() {
  msg.value = ''
  err.value = ''
  if (!(thresholdMm.value > 0)) {
    err.value = '门槛必须 > 0，未保存。'
    return
  }
  if (extraPieces.value < 0 || !Number.isInteger(Number(extraPieces.value))) {
    err.value = '加片枚数必须为非负整数，未保存。'
    return
  }
  try {
    settings.value = await putJSON('/api/settings', {
      remnant_threshold_mm: Number(thresholdMm.value),
      extra_pieces: Number(extraPieces.value),
    })
    thresholdMm.value = Number(settings.value.remnant_threshold_mm)
    extraPieces.value = Number(settings.value.extra_pieces)
    msg.value = '已保存。新默认值只作用于之后的新单，历史单保持不变。'
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按面积法向上取整后再乘 (1+损耗%)。当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>

    <fieldset class="box">
      <legend>余料门槛默认值</legend>
      <p class="hint">沿长、沿宽对砖边取模得到余料条；任一条 &gt;0 且小于门槛时，订货片数加一次固定枚数。下单台可逐单开关与覆盖。</p>
      <label>默认门槛（mm，&gt;0）
        <input type="number" v-model.number="thresholdMm" min="1" step="1">
      </label>
      <label>默认加片枚数（枚，≥0 整数）
        <input type="number" v-model.number="extraPieces" min="0" step="1">
      </label>
      <button @click="save">保存默认值</button>
      <p v-if="msg" class="ok">{{ msg }}</p>
      <p v-if="err" class="alert">{{ err }}</p>
    </fieldset>

    <p>网格预览块数可能大于面积法片数，下单以面积法 order_count（加片后订货）为准。</p>
    <p>修改默认门槛/枚数只作用于之后的新单；历史详情保持下单当时加片后的数字。</p>
  </div>
</template>
<style scoped>
.box { border: 1px solid #bbb; padding: 0.75rem 1rem; margin: 1rem 0; max-width: 560px; }
.hint { color: #666; font-size: 0.85rem; }
.ok { color: #1e8449; }
</style>
