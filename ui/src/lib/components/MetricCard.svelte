<script>
  /** @type {{ title: string, value: string, icon?: string, trend?: string }} */
  let { title, value, icon = '📊', trend = '' } = $props();
</script>

<div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-6 hover:bg-white/10 transition-all duration-300 hover:border-purple-500/30 group">
  <div class="flex items-start justify-between mb-4">
    <span class="text-3xl">{icon}</span>
    {#if trend}
      <span class="text-xs px-2 py-1 rounded-full bg-purple-500/20 text-purple-400 font-medium">
        {trend}
      </span>
    {/if}
  </div>
  <p class="text-white/60 text-sm mb-1">{title}</p>
  <p class="text-3xl font-bold text-white group-hover:text-purple-400 transition-all">
    {value}
  </p>
</div>
