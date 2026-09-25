<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'

const settings = ref({})
const thresholdMm = ref(100)
const extraPieces = ref(2)
const err = ref('')
const okMsg = ref('')

onMounted(async () => {
  settings.value = await getJSON('/api/settings')
  thresholdMm.value = Number(settings.value.remainder_threshold_mm)
  extraPieces.value = Number(settings.value.remainder_extra_pieces)
})

async function save() {
  err.value = ''
  okMsg.value = ''
  const threshold = Math.trunc(Number(thresholdMm.value))
  const extra = Math.trunc(Number(extraPieces.value))
  if (!(threshold > 0)) {
    err.value = '余料门槛必须为大于 0 的整数（mm）'
    return
  }
  if (!(extra >= 1)) {
    err.value = '每条加片枚数必须为不小于 1 的整数'
    return
  }
  try {
    settings.value = await postJSON('/api/settings', {
      remainder_threshold_mm: threshold,
      remainder_extra_pieces: extra,
    })
    okMsg.value = '已保存，新默认值仅作用于之后新下的单。'
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按面积法向上取整后再乘 (1+损耗%)。</p>
    <p>当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>

    <h2>余料门槛与加片</h2>
    <p>沿长、沿宽对砖边取模得到余料条；某条余料 &gt;0 且小于门槛时，订货片数再加固定加片枚数，两条独立判定、各加一次。关闭门槛时订货数回到仅计损耗。</p>
    <label class="field-inline">余料门槛
      <input type="number" min="1" step="1" v-model.number="thresholdMm"> mm
    </label>
    <label class="field-inline">每条加片
      <input type="number" min="1" step="1" v-model.number="extraPieces"> 枚
    </label>
    <button class="primary" @click="save">保存默认值</button>
    <p v-if="err" class="alert">{{ err }}</p>
    <p v-if="okMsg" class="ok">{{ okMsg }}</p>

    <p class="muted">网格预览块数可能大于面积法片数，下单以面积法 order_count 为准。</p>
  </div>
</template>
