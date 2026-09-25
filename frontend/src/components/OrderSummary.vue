<script setup>
const props = defineProps({
  result: { type: Object, default: null },
})

function mm(meters) {
  return meters == null ? '—' : Math.round(meters * 1000)
}

function stripPct(rem, edge) {
  if (!rem || !edge) return 0
  return Math.min(100, Math.max(0, (rem / edge) * 100))
}

function edgeLabel(rem, edge, thresholdM, enabled) {
  if (!rem || rem === 0) return '无余料'
  if (enabled && rem < thresholdM) return '加片'
  return '未达门槛'
}
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>

    <div v-if="result.base_order_count != null" class="remainder-box">
      <template v-if="result.remainder_enabled">
        <p class="remainder-title">
          余料门槛 {{ mm(result.remainder_threshold_mm) }} mm，余料 &gt;0 且小于门槛时每条加
          {{ result.remainder_extra_per_strip }} 枚
        </p>
        <div class="strip-row">
          <span class="strip-label">沿长余料 {{ mm(result.remainder_l_m) }} mm</span>
          <div class="strip">
            <div
              class="strip__offcut"
              :class="{ 'strip__offcut--safe': !result.remainder_l_triggered }"
              :style="{ width: stripPct(result.remainder_l_m, result.tile?.tile_l) + '%' }"
            ></div>
          </div>
          <span class="tag" :class="{ 'tag--hit': result.remainder_l_triggered }">
            {{ edgeLabel(result.remainder_l_m, result.tile?.tile_l, result.remainder_threshold_m, true) }}
          </span>
        </div>
        <div class="strip-row">
          <span class="strip-label">沿宽余料 {{ mm(result.remainder_w_m) }} mm</span>
          <div class="strip">
            <div
              class="strip__offcut"
              :class="{ 'strip__offcut--safe': !result.remainder_w_triggered }"
              :style="{ width: stripPct(result.remainder_w_m, result.tile?.tile_w) + '%' }"
            ></div>
          </div>
          <span class="tag" :class="{ 'tag--hit': result.remainder_w_triggered }">
            {{ edgeLabel(result.remainder_w_m, result.tile?.tile_w, result.remainder_threshold_m, true) }}
          </span>
        </div>
        <p class="order-breakdown">
          基础订货 <strong>{{ result.base_order_count }}</strong> 片
          + 加片 <strong>{{ result.remainder_extra_count }}</strong> 片
          （{{ result.remainder_trigger_count }} 条 × {{ result.remainder_extra_per_strip }} 枚）
          = <strong>{{ result.order_count }}</strong> 片
        </p>
      </template>
      <p v-else class="muted">余料门槛未启用，订货为损耗后 {{ result.base_order_count }} 片。</p>
    </div>
  </div>
</template>
