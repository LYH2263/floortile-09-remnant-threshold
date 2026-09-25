<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数（加片后）</th><th>余料门槛</th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ r.result?.order_count }}</td>
          <td v-if="r.result?.remnant_enabled">
            启用（{{ r.result.remnant_threshold_mm }}mm）<template v-if="r.result.remnant?.extra_count">，加片 +{{ r.result.remnant.extra_count }}</template>
          </td>
          <td v-else>关闭</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
