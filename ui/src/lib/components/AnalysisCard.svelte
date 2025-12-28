<script>
  /** @type {{ title: string, description: string, icon: string, onSelect?: () => void }} */
  let { title, description, icon, onSelect = () => {} } = $props();
</script>

<button 
  onclick={onSelect}
  class="w-full text-left bg-white/5 backdrop-blur-md rounded-xl p-6 border border-white/10 transition-all duration-300 hover:bg-white/10 hover:border-purple-500/30 group cursor-pointer"
>
  <div class="flex items-start gap-4">
    <div class="w-12 h-12 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-2xl flex-shrink-0">
      {icon}
    </div>
    <div class="flex-1">
      <h3 class="text-lg font-medium text-white mb-2 group-hover:text-purple-400 transition-all">
        {title}
      </h3>
      <p class="text-sm text-white/50 leading-relaxed">{description}</p>
    </div>
    <div class="text-white/30 group-hover:text-purple-400 transition-colors">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h14"/>
        <path d="m12 5 7 7-7 7"/>
      </svg>
    </div>
  </div>
</button>
