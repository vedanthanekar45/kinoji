<script>
  /** @type {{ onNavigate?: (page: string) => void }} */
  let { onNavigate = () => {} } = $props();
</script>

<main class="w-screen h-screen bg-[url('/kinoji.jpg')] max-sm:bg-[url('/kinoji_mob.png')] bg-cover bg-center bg-no-repeat flex items-center justify-center relative overflow-hidden font-['Funnel_Display',sans-serif]">
  <!-- Kinoji Logo -->
  <h1 class="absolute top-6 left-1/2 -translate-x-1/2 text-2xl font-medium text-white z-20">Kinoji</h1>

  <!-- GitHub Icon -->
  <a href="https://github.com/vedanthanekar45/kinoji" target="_blank" rel="noreferrer" class="absolute top-6 right-6 max-sm:top-4 max-sm:right-4 text-white hover:text-white/80 transition-all duration-300 ease-in-out z-20 hover:scale-110" aria-label="Visit GitHub profile">
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
  </a>

  <div class="text-center z-10 p-4 w-full max-w-[800px]">
    <h1 class="text-[clamp(1.75rem,5vw,3.5rem)] font-thin text-white mb-6 max-sm:mb-4">Decoding the DNA of Cinema</h1>
    
    <div class="flex items-center justify-center mb-6 px-4">
      <div class="relative w-full max-w-[600px]">
        <input type="text" placeholder="Generate insights with AI.." class="w-full py-3 pr-12 pl-4 max-sm:py-2.5 max-sm:px-3 max-sm:text-sm border border-white/30 rounded-lg bg-white/10 text-white text-base outline-none backdrop-blur-sm placeholder:text-white/50" />
        <button class="absolute right-2 top-1/2 -translate-y-1/2 bg-transparent border-none text-white/50 hover:text-white cursor-pointer p-1 flex items-center justify-center transition-colors duration-200 ease-in-out" aria-label="Send">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>

    <p class="text-white/60 text-[0.95rem] mb-4">Or choose one of the options below</p>

    <div class="flex items-center justify-center gap-4 flex-wrap max-sm:flex-col max-sm:gap-3">
      <button 
        onclick={() => onNavigate('dashboard')}
        class="py-3 px-6 rounded-lg text-base font-medium cursor-pointer transition-all duration-200 whitespace-nowrap bg-transparent text-white border border-white/50 hover:bg-white hover:text-black max-sm:w-full max-sm:max-w-[250px]"
      >
        Go to Dashboard
      </button>
      <span class="text-white/60 text-sm max-sm:hidden">or</span>
      <button 
        onclick={() => onNavigate('ai-analysis')}
        class="py-3 px-6 rounded-lg text-base font-medium cursor-pointer transition-all duration-200 whitespace-nowrap bg-transparent text-white border border-white/50 hover:bg-white hover:text-black max-sm:w-full max-sm:max-w-[250px]"
      >
        AI Analysis
      </button>
    </div>
  </div>
</main>
