<script>
  let query = $state('');

  const suggestions = [
    "Find me a thriller like Inception but shorter",
    "Movies with plot twists that aren't horror",
    "Underrated 90s comedies with high ratings",
    "Something visually stunning but under 2 hours"
  ];

  const curatedResults = [
    { title: 'Memento', year: 2000, rating: 8.4, runtime: '113 min', genre: 'Mystery/Thriller' },
    { title: 'The Prestige', year: 2006, rating: 8.5, runtime: '130 min', genre: 'Drama/Mystery' },
    { title: 'Coherence', year: 2013, rating: 7.2, runtime: '89 min', genre: 'Sci-Fi/Mystery' },
  ];
</script>

<div class="min-h-screen pt-24 pb-12 px-6">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-12">
      <span class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/20 border border-purple-500/30 text-purple-400 text-sm mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
        </svg>
        AI-Powered
      </span>
      <h1 class="text-4xl md:text-5xl font-medium text-white mb-4">Curate Your Perfect Movie</h1>
      <p class="text-white/50 text-lg">Describe what you're in the mood for and let AI find the perfect match</p>
    </div>

    <!-- Search Input -->
    <div class="relative mb-8">
      <div class="bg-white/5 border border-white/20 rounded-xl p-2">
        <textarea 
          bind:value={query}
          placeholder="Describe your ideal movie... e.g., 'A mind-bending thriller from the 2000s with a strong female lead and a runtime under 2 hours'"
          class="w-full py-4 px-4 bg-transparent text-white text-lg outline-none resize-none placeholder:text-white/30 min-h-[120px]"
        ></textarea>
        <div class="flex items-center justify-between px-2 pb-2">
          <span class="text-xs text-white/40">Be as specific as you like</span>
          <button class="px-6 py-2 rounded-xl bg-purple-500 text-white font-medium hover:bg-purple-600 transition-colors cursor-pointer flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
            Find Movies
          </button>
        </div>
      </div>
    </div>

    <!-- Suggestions -->
    <div class="mb-12">
      <p class="text-sm text-white/40 mb-4">Try these suggestions:</p>
      <div class="flex flex-wrap gap-2">
        {#each suggestions as suggestion}
          <button 
            onclick={() => query = suggestion}
            class="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-white/50 hover:bg-white/10 hover:text-white hover:border-purple-500/30 transition-all cursor-pointer"
          >
            {suggestion}
          </button>
        {/each}
      </div>
    </div>

    <!-- Results -->
    <div>
      <h3 class="text-lg font-medium text-white mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-purple-500"></span>
        Curated for you
      </h3>
      
      <div class="space-y-4">
        {#each curatedResults as movie, i}
          <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-5 hover:bg-white/10 hover:border-purple-500/30 transition-all cursor-pointer group">
            <div class="flex items-start justify-between">
              <div class="flex items-start gap-4">
                <span class="text-2xl font-bold text-white/20 group-hover:text-purple-500/50 transition-colors">
                  {String(i + 1).padStart(2, '0')}
                </span>
                <div>
                  <h4 class="text-lg font-medium text-white group-hover:text-purple-400 transition-all">
                    {movie.title}
                  </h4>
                  <p class="text-sm text-white/50 mt-1">
                    {movie.year} • {movie.genre} • {movie.runtime}
                  </p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-lg font-bold text-purple-400">{movie.rating}</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="text-purple-400">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>
