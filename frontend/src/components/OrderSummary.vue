<script setup>
defineProps({
  result: { type: Object, default: null },
})

function fmtMm(v) {
  return v > 0 ? `${v} mm` : '整砖（无余料）'
}
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li v-if="result.remnant_enabled">
        基础订货 {{ result.base_order_count }} 片
        <template v-if="result.remnant?.extra_count > 0">
          → 余料加片 +{{ result.remnant.extra_count }}（{{ result.extra_pieces }} 枚/单）
        </template>
        → 加片后订货 <strong>{{ result.order_count }}</strong> 片
      </li>
      <li v-else>基础订货（即最终订货）{{ result.base_order_count ?? result.order_count }} 片（余料门槛关闭）</li>
      <li v-if="result.remnant">
        余料条：沿长 {{ fmtMm(result.remnant.along_length_mm) }}
        <span :class="{ hit: result.remnant.hit_length }">{{ result.remnant.hit_length ? '⚠ 低于门槛' : '' }}</span>
        ；沿宽 {{ fmtMm(result.remnant.along_width_mm) }}
        <span :class="{ hit: result.remnant.hit_width }">{{ result.remnant.hit_width ? '⚠ 低于门槛' : '' }}</span>
        <template v-if="result.remnant_enabled">（门槛 {{ result.remnant_threshold_mm }} mm）</template>
      </li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>
  </div>
</template>
<style scoped>
.hit { color: #c0392b; margin-left: 0.25rem; }
</style>
