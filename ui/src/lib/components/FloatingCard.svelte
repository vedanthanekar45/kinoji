<script>
  /** @type {{ text: string, top?: string, left?: string, right?: string, bottom?: string, delay?: number }} */
  let { text, top = 'auto', left = 'auto', right = 'auto', bottom = 'auto', delay = 0 } = $props();
</script>

<div 
  class="absolute bg-white/5 border border-white/10 backdrop-blur-sm rounded-xl px-4 py-3 text-sm text-slate-400 opacity-20 hover:opacity-40 transition-opacity duration-500 max-w-[200px] pointer-events-none animate-float"
  style="top: {top}; left: {left}; right: {right}; bottom: {bottom}; animation-delay: {delay}s;"
>
  <div class="flex items-center gap-2">
    <div class="w-2 h-2 rounded-full bg-gradient-to-r from-sky-400 to-purple-500"></div>
    <span class="text-xs font-medium">{text}</span>
  </div>
</div>

<style>
  @keyframes float {
    0%, 100% {
      transform: translateY(0px);
    }
    50% {
      transform: translateY(-10px);
    }
  }
  
  .animate-float {
    animation: float 6s ease-in-out infinite;
  }
</style>
