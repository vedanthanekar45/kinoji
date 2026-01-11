<script>
  let query = $state('');
  let isLoading = $state(false);

  const suggestions = [
    "What genres are underrepresented in the 2020s?",
    "Which director has the most consistent ratings?",
    "Find patterns in highest-rated movies under 90 minutes",
    "What makes a horror movie successful?",
    "Compare 80s vs 2010s action movies"
  ];

  // Blue Ocean data
  const genreOpportunities = [
    { g1: 'Horror', g2: 'Musical', count: 12, opportunity: 'high' },
    { g1: 'Sci-Fi', g2: 'Western', count: 8, opportunity: 'high' },
    { g1: 'Fantasy', g2: 'Documentary', count: 3, opportunity: 'high' },
    { g1: 'Romance', g2: 'Horror', count: 24, opportunity: 'high' },
    { g1: 'Comedy', g2: 'War', count: 18, opportunity: 'medium' },
    { g1: 'Animation', g2: 'Noir', count: 5, opportunity: 'high' },
  ];

  const aiInsights = [
    { 
      title: "Runtime Sweet Spot",
      insight: "Movies between 95-115 minutes have 12% higher ratings on average",
      icon: "⏱️"
    },
    { 
      title: "December Effect",
      insight: "Films released in December average 0.3 points higher in ratings",
      icon: "📅"
    },
    { 
      title: "Sequel Fatigue",
      insight: "Third installments drop 18% in ratings compared to originals",
      icon: "📉"
    },
    { 
      title: "Director Debut",
      insight: "First-time directors in horror outperform veterans by 8%",
      icon: "🎬"
    }
  ];

  function handleSuggestionClick(suggestion) {
    query = suggestion;
  }

  function handleSubmit() {
    if (!query.trim()) return;
    isLoading = true;
    // Simulate API call
    setTimeout(() => {
      isLoading = false;
    }, 1500);
  }
</script>

<div class="min-h-screen pt-20 pb-16 px-4 sm:px-6 lg:px-8">
  <div class="max-w-6xl mx-auto">
    
    <!-- Header -->
    <header class="text-center mb-10">
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/15 border border-purple-500/25 text-purple-400 text-sm mb-5">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
        </svg>
        AI-Powered Analysis
      </div>
      <h1 class="text-3xl sm:text-4xl font-semibold text-white mb-3">Ask Anything About Cinema</h1>
      <p class="text-slate-400 max-w-xl mx-auto">Explore patterns, discover insights, and uncover hidden trends in movie data</p>
    </header>

    <!-- Query Input -->
    <section class="mb-10">
      <div class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-3 sm:p-4">
        <textarea 
          bind:value={query}
          placeholder="Ask a question about movies, trends, or patterns..."
          class="w-full py-3 px-3 bg-transparent text-white outline-none resize-none placeholder:text-slate-500 min-h-[100px] text-base sm:text-lg"
        ></textarea>
        <div class="flex items-center justify-between pt-2 border-t border-slate-700/50">
          <span class="text-xs text-slate-500 hidden sm:block">Press Enter to analyze</span>
          <button 
            onclick={handleSubmit}
            disabled={isLoading || !query.trim()}
            class="px-5 py-2.5 rounded-xl bg-purple-600 text-white font-medium hover:bg-purple-500 transition-colors cursor-pointer flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if isLoading}
              <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              Analyzing...
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
              </svg>
              Analyze
            {/if}
          </button>
        </div>
      </div>

      <!-- Suggestions -->
      <div class="mt-5">
        <p class="text-xs text-slate-500 mb-3">Try asking:</p>
        <div class="flex flex-wrap gap-2">
          {#each suggestions as suggestion}
            <button 
              onclick={() => handleSuggestionClick(suggestion)}
              class="px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50 text-xs sm:text-sm text-slate-400 hover:bg-slate-700/60 hover:text-white hover:border-purple-500/40 transition-all cursor-pointer"
            >
              {suggestion}
            </button>
          {/each}
        </div>
      </div>
    </section>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 sm:gap-8">
      
      <!-- AI Insights Column -->
      <section class="lg:col-span-2">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-2 h-2 rounded-full bg-purple-500"></div>
          <h2 class="text-base font-medium text-white">AI Insights</h2>
        </div>
        
        <div class="space-y-3">
          {#each aiInsights as item}
            <article class="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 hover:border-purple-500/30 transition-all cursor-pointer group">
              <div class="flex items-start gap-3">
                <span class="text-xl">{item.icon}</span>
                <div>
                  <h3 class="text-sm font-medium text-white group-hover:text-purple-400 transition-colors">{item.title}</h3>
                  <p class="text-xs text-slate-400 mt-1 leading-relaxed">{item.insight}</p>
                </div>
              </div>
            </article>
          {/each}
        </div>
      </section>

      <!-- Blue Ocean Detector -->
      <section class="lg:col-span-3">
        <div class="flex items-center gap-2 mb-4">
          <span class="text-lg">🌊</span>
          <h2 class="text-base font-medium text-white">Blue Ocean Detector</h2>
        </div>
        <p class="text-xs text-slate-500 mb-4">Genre combinations with untapped potential</p>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {#each genreOpportunities as combo}
            <article class="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 hover:border-purple-500/30 transition-all cursor-pointer">
              <div class="flex items-center gap-2 mb-3">
                <span class="px-2 py-1 rounded-md bg-purple-500/20 text-purple-400 text-xs font-medium">{combo.g1}</span>
                <span class="text-slate-600">×</span>
                <span class="px-2 py-1 rounded-md bg-slate-700/60 text-slate-300 text-xs font-medium">{combo.g2}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-slate-500">Only {combo.count} movies exist</span>
                <span class="text-xs px-2 py-0.5 rounded-full {combo.opportunity === 'high' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}">
                  {combo.opportunity === 'high' ? '🔥 High' : '📊 Medium'} opportunity
                </span>
              </div>
            </article>
          {/each}
        </div>

        <!-- CTA -->
        <div class="mt-6 p-4 bg-gradient-to-r from-purple-500/10 to-transparent border border-purple-500/20 rounded-xl">
          <p class="text-sm text-slate-300">
            <span class="text-purple-400 font-medium">Pro tip:</span> 
            Horror + Musical has only 12 films ever made. The last one was in 2019.
          </p>
        </div>
      </section>
    </div>

  </div>
</div>
