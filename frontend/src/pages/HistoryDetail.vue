<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'
import TileGridPreview from '../components/TileGridPreview.vue'

const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = e.message
  }
})

function mm(meters) {
  return meters == null ? '—' : `${Math.round(meters * 1000)} mm`
}
</script>
<template>
  <div class="page">
    <h1>历史详情 #{{ id }}</h1>
    <p v-if="err" class="alert">{{ err }}</p>
    <template v-if="run">
      <dl>
        <dt>时间</dt><dd>{{ run.created_at?.slice(0, 19) }}</dd>
        <dt>房间</dt><dd>{{ run.room_name }}</dd>
        <dt>砖型</dt><dd>{{ run.tile_name }}</dd>
        <dt>损耗</dt><dd>{{ run.waste_pct }}%</dd>
        <dt>备注</dt><dd>{{ run.note || '—' }}</dd>
      </dl>

      <!-- result shape mirrors the estimate payload, so OrderSummary renders the pinned snapshot as-is -->
      <OrderSummary :result="{ ...run.result, run_id: run.id }" />
      <TileGridPreview
        v-if="run.result?.layout"
        :cols="run.result.layout.cols"
        :rows="run.result.layout.rows"
        :grid-count="run.result.layout.grid_count"
      />

      <h2>加片明细（下单时钉住）</h2>
      <table class="tbl" v-if="run.result?.base_order_count != null">
        <tbody>
          <tr><th>余料门槛</th><td>{{ mm(run.result.remainder_threshold_m) }}</td></tr>
          <tr><th>沿长余料条</th><td>{{ mm(run.result.remainder_l_m) }}</td></tr>
          <tr><th>沿宽余料条</th><td>{{ mm(run.result.remainder_w_m) }}</td></tr>
          <tr><th>每条加片枚数</th><td>{{ run.result.remainder_extra_per_strip }}</td></tr>
          <tr><th>触发条数</th><td>{{ run.result.remainder_trigger_count }}</td></tr>
          <tr><th>加片总数</th><td>{{ run.result.remainder_extra_count }}</td></tr>
          <tr><th>基础订货</th><td>{{ run.result.base_order_count }} 片</td></tr>
          <tr><th>加片后订货</th><td><strong>{{ run.result.order_count }} 片</strong></td></tr>
        </tbody>
      </table>
      <p v-else class="muted">该单下于余料门槛功能上线前，未启用门槛，订货 {{ run.result?.order_count }} 片。</p>

      <router-link to="/history">返回列表</router-link>
    </template>
  </div>
</template>
