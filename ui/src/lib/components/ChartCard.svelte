<script>
  /** @type {{ title: string, description?: string, type?: 'line' | 'bar' | 'histogram' }} */
  let { title, description = '', type = 'line' } = $props();

  // Mock data for demonstration
  const mockLineData = [65, 72, 78, 85, 92, 98, 105, 110, 114, 118];
  const mockBarData = [85, 72, 68, 55, 48, 42, 35, 28];
  const mockHistData = [12, 25, 45, 78, 95, 88, 65, 42, 28, 15];

  const data = type === 'line' ? mockLineData : type === 'bar' ? mockBarData : mockHistData;
  const maxValue = Math.max(...data);
</script>

<div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-6 hover:bg-white/10 transition-all duration-300">
  <div class="mb-6">
    <h3 class="text-lg font-medium text-white mb-1">{title}</h3>
    {#if description}
      <p class="text-sm text-white/50">{description}</p>
    {/if}
  </div>

  <!-- Chart Visualization -->
  <div class="h-48 flex items-end justify-between gap-2 px-2">
    {#each data as value, i}
      <div class="flex-1 flex flex-col items-center gap-2">
        <div 
          class="w-full rounded-t-lg transition-all duration-500 hover:opacity-80 bg-purple-500"
          style="height: {(value / maxValue) * 100}%"
        ></div>
      </div>
    {/each}
  </div>

  <!-- X-axis labels -->
  <div class="flex justify-between mt-4 px-2">
    {#if type === 'line'}
      <span class="text-xs text-white/40">1990</span>
      <span class="text-xs text-white/40">2000</span>
      <span class="text-xs text-white/40">2024</span>
    {:else if type === 'bar'}
      <span class="text-xs text-white/40">Drama</span>
      <span class="text-xs text-white/40">Action</span>
      <span class="text-xs text-white/40">Horror</span>
    {:else}
      <span class="text-xs text-white/40">1-2</span>
      <span class="text-xs text-white/40">5-6</span>
      <span class="text-xs text-white/40">9-10</span>
    {/if}
  </div>
</div>
