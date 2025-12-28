<script>
  /** @type {{ currentPage?: string, onNavigate?: (page: string) => void }} */
  let { currentPage = 'home', onNavigate = () => {} } = $props();
  
  let scrolled = $state(false);

  const navLinks = [
    { name: 'Home', id: 'home' },
    { name: 'Dashboard', id: 'dashboard' },
    { name: 'AI Curator', id: 'curator' },
    { name: 'Analysis', id: 'analysis' }
  ];

  function handleScroll() {
    scrolled = window.scrollY > 20;
  }

  $effect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  });
</script>

<nav class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 {scrolled ? 'bg-slate-950/80 backdrop-blur-md border-b border-white/10' : 'bg-transparent'}">
  <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
    <!-- Logo -->
    <button 
      onclick={() => onNavigate('home')}
      class="text-2xl font-medium text-white hover:opacity-80 transition-opacity cursor-pointer"
    >
      Kinoji
    </button>

    <!-- Navigation Links -->
    <div class="flex items-center gap-8">
      {#each navLinks as link}
        <button
          onclick={() => onNavigate(link.id)}
          class="text-sm font-medium transition-all duration-200 cursor-pointer {currentPage === link.id ? 'text-white' : 'text-slate-400 hover:text-white'}"
        >
          {link.name}
          {#if currentPage === link.id}
            <div class="h-0.5 mt-1 bg-purple-500 rounded-full"></div>
          {/if}
        </button>
      {/each}
    </div>

    <!-- GitHub Link -->
    <a 
      href="https://github.com/vedanthanekar45/kinoji" 
      target="_blank" 
      rel="noreferrer"
      class="text-slate-400 hover:text-white transition-colors"
      aria-label="GitHub"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
      </svg>
    </a>
  </div>
</nav>
