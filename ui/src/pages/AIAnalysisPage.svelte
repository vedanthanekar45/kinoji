<script>
  import DynamicChart from '../lib/components/DynamicChart.svelte';
  const API_BASE = 'https://kinoji.duckdns.org';

  let { initialQuery = '' } = $props();

  let query = $state('');
  let isLoading = $state(false);
  let result = $state(null);
  let error = $state('');

  // Handle initial query from homepage
  $effect(() => {
    if (initialQuery) {
      query = initialQuery;
      handleSubmit();
    }
  });

  const suggestions = [
    "How many movies were released each year since 2000?",
    "What are the top 10 genres by movie count?",
    "Show average rating by decade",
    "Which studios produced the most movies?",
    "Top 10 highest rated movies of all time"
  ];

  function handleSuggestionClick(suggestion) {
    query = suggestion;
  }

  async function handleSubmit() {
    if (!query.trim()) return;
    
    isLoading = true;
    error = '';
    result = null;

    try {
      const response = await fetch(`${API_BASE}/generate/insight`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query.trim() })
      });

      if (!response.ok) {
        throw new Error('Failed to generate insight');
      }

      const data = await response.json();
      result = data;
    } catch (err) {
      console.error('AI Error:', err);
      error = 'Could not generate insight. Please try a different question.';
    } finally {
      isLoading = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  // Transform API data for chart
  const chartData = $derived(
    result?.data?.map(d => ({
      label: String(d.label || Object.values(d)[0]),
      value: Number(d.value || Object.values(d)[1] || 0)
    })) || []
  );
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
    <section class="mb-8">
      <div class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-3 sm:p-4">
        <textarea 
          bind:value={query}
          onkeydown={handleKeydown}
          placeholder="Ask a question about movies, trends, or patterns..."
          class="w-full py-3 px-3 bg-transparent text-white outline-none resize-none placeholder:text-slate-500 min-h-[80px] text-base sm:text-lg"
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
      <div class="mt-4">
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

    <!-- Loading State -->
    {#if isLoading}
      <section class="mb-10">
        <div class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-8">
          <div class="flex flex-col items-center justify-center py-12">
            <div class="relative mb-6">
              <div class="w-16 h-16 border-4 border-purple-500/20 rounded-full"></div>
              <div class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-purple-500 rounded-full animate-spin"></div>
            </div>
            <p class="text-white font-medium mb-2">Analyzing your question...</p>
            <p class="text-slate-500 text-sm text-center max-w-md">
              Our AI is querying the database and generating insights. This may take a few seconds.
            </p>
            <div class="flex items-center gap-1 mt-4">
              <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
              <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
            </div>
          </div>
        </div>
      </section>
    {/if}

    <!-- Error State -->
    {#if error}
      <section class="mb-10">
        <div class="bg-red-500/10 border border-red-500/30 rounded-2xl p-6">
          <div class="flex items-start gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-400 flex-shrink-0 mt-0.5"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
            <div>
              <p class="text-red-400 font-medium">Analysis Failed</p>
              <p class="text-red-400/70 text-sm mt-1">{error}</p>
            </div>
          </div>
        </div>
      </section>
    {/if}

    <!-- Result Section -->
    {#if result && !isLoading}
      <section class="mb-10 space-y-6">
        <!-- Summary Card -->
        <div class="bg-gradient-to-r from-purple-500/15 to-purple-600/5 border border-purple-500/30 rounded-2xl p-6">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400">
                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-medium text-purple-400 mb-1">AI Insight</h3>
              <p class="text-white text-lg leading-relaxed">{result.summary}</p>
            </div>
          </div>
        </div>

        <!-- Chart Card -->
        {#if chartData.length > 0}
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-6">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h3 class="text-white font-medium">Visualization</h3>
                <p class="text-slate-500 text-sm mt-1">
                  {result.type === 'line' ? 'Trend over time' : 
                   result.type === 'bar' ? 'Comparison' : 
                   result.type === 'pie' ? 'Distribution' : 'Data'}
                </p>
              </div>
              <span class="px-3 py-1 rounded-lg bg-slate-800 text-slate-400 text-xs uppercase tracking-wide">
                {result.type}
              </span>
            </div>
            <div class="h-72">
              <DynamicChart type={result.type} data={chartData} />
            </div>
          </div>
        {/if}
      </section>
    {/if}

  </div>
</div>
