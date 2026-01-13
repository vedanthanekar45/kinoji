<script>
  /** @type {{ title: string, value: string, icon?: string, trend?: string }} */
  let { title, value, icon = '', trend = '' } = $props();
</script>

<div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-6 hover:bg-white/10 transition-all duration-300 hover:border-purple-500/30 group">
  <div class="flex items-start justify-between mb-4">
    {#if icon}
      <span class="text-3xl">{@html icon}</span>
    {:else}
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>
    {/if}
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
