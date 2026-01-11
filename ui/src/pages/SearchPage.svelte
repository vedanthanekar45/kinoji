<script>
  import { Search, Filter, X, ChevronDown } from 'lucide-svelte';

  const API_BASE = 'http://127.0.0.1:8000';

  // State
  let searchQuery = $state('');
  let selectedGenres = $state([]);
  let minRating = $state('');
  let selectedYear = $state('');
  let results = $state([]);
  let isLoading = $state(false);
  let hasSearched = $state(false);
  let showFilters = $state(false);

  const genres = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
    'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music',
    'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War', 'Western'
  ];

  // Generate years from 2025 down to 1920
  const years = Array.from({ length: 106 }, (_, i) => 2025 - i);

  function toggleGenre(genre) {
    if (selectedGenres.includes(genre)) {
      selectedGenres = selectedGenres.filter(g => g !== genre);
    } else {
      selectedGenres = [...selectedGenres, genre];
    }
  }

  function clearFilters() {
    selectedGenres = [];
    minRating = '';
    selectedYear = '';
  }

  async function handleSearch() {
    isLoading = true;
    hasSearched = true;

    try {
      const params = new URLSearchParams();
      
      if (searchQuery.trim()) {
        params.append('title', searchQuery.trim());
      }
      
      selectedGenres.forEach(g => params.append('genres', g));
      
      if (minRating) {
        params.append('min_rating', minRating);
      }
      
      if (selectedYear) {
        params.append('year', selectedYear);
      }

      const response = await fetch(`${API_BASE}/search?${params.toString()}`);
      const data = await response.json();
      results = data;
    } catch (err) {
      console.error('Search failed:', err);
      results = [];
    } finally {
      isLoading = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return '—';
    const date = new Date(dateStr);
    return date.getFullYear();
  }

  function formatRuntime(minutes) {
    if (!minutes) return '—';
    const hrs = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hrs > 0 ? `${hrs}h ${mins}m` : `${mins}m`;
  }

  const activeFilterCount = $derived(
    selectedGenres.length + (minRating ? 1 : 0) + (selectedYear ? 1 : 0)
  );
</script>

<div class="min-h-screen pt-20 pb-16 px-4 sm:px-6 lg:px-8">
  <div class="max-w-7xl mx-auto">
    
    <!-- Header -->
    <header class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-semibold text-white mb-2">Search Movies</h1>
      <p class="text-slate-400">Find movies from our collection of 59,000+ titles</p>
    </header>

    <!-- Search Bar -->
    <div class="mb-6">
      <div class="flex gap-3">
        <div class="flex-1 relative">
          <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            bind:value={searchQuery}
            onkeydown={handleKeydown}
            placeholder="Search by movie title..."
            class="w-full py-3.5 pl-12 pr-4 bg-slate-900/60 border border-slate-700/60 rounded-xl text-white placeholder:text-slate-500 outline-none focus:border-purple-500/50 transition-colors"
          />
        </div>
        <button
          onclick={() => showFilters = !showFilters}
          class="px-4 py-3.5 bg-slate-900/60 border border-slate-700/60 rounded-xl text-slate-300 hover:text-white hover:border-slate-600 transition-all flex items-center gap-2 relative"
        >
          <Filter class="w-5 h-5" />
          <span class="hidden sm:inline">Filters</span>
          {#if activeFilterCount > 0}
            <span class="absolute -top-2 -right-2 w-5 h-5 bg-purple-500 rounded-full text-xs flex items-center justify-center text-white font-medium">
              {activeFilterCount}
            </span>
          {/if}
        </button>
        <button
          onclick={handleSearch}
          disabled={isLoading}
          class="px-6 py-3.5 bg-purple-600 hover:bg-purple-500 rounded-xl text-white font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          {#if isLoading}
            <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          {:else}
            <Search class="w-4 h-4" />
          {/if}
          Search
        </button>
      </div>
    </div>

    <!-- Filters Panel -->
    {#if showFilters}
      <div class="mb-6 p-5 bg-slate-900/60 border border-slate-700/60 rounded-xl animate-in slide-in-from-top-2 duration-200">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-medium text-white">Filters</h3>
          {#if activeFilterCount > 0}
            <button onclick={clearFilters} class="text-xs text-slate-400 hover:text-white flex items-center gap-1">
              <X class="w-3 h-3" />
              Clear all
            </button>
          {/if}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Genres -->
          <div>
            <label class="block text-xs text-slate-500 mb-2">Genres</label>
            <div class="flex flex-wrap gap-2 max-h-32 overflow-y-auto pr-2">
              {#each genres as genre}
                <button
                  onclick={() => toggleGenre(genre)}
                  class="px-2.5 py-1 rounded-lg text-xs transition-all {selectedGenres.includes(genre) 
                    ? 'bg-purple-500 text-white' 
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'}"
                >
                  {genre}
                </button>
              {/each}
            </div>
          </div>

          <!-- Min Rating -->
          <div>
            <label class="block text-xs text-slate-500 mb-2">Minimum Rating</label>
            <select
              bind:value={minRating}
              class="w-full py-2.5 px-3 bg-slate-800 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-purple-500/50"
            >
              <option value="">Any rating</option>
              <option value="4.5">4.5+ ⭐</option>
              <option value="4.0">4.0+ ⭐</option>
              <option value="3.5">3.5+ ⭐</option>
              <option value="3.0">3.0+ ⭐</option>
              <option value="2.5">2.5+ ⭐</option>
            </select>
          </div>

          <!-- Year -->
          <div>
            <label class="block text-xs text-slate-500 mb-2">Release Year</label>
            <select
              bind:value={selectedYear}
              class="w-full py-2.5 px-3 bg-slate-800 border border-slate-700 rounded-lg text-white text-sm outline-none focus:border-purple-500/50"
            >
              <option value="">Any year</option>
              {#each years as year}
                <option value={year}>{year}</option>
              {/each}
            </select>
          </div>
        </div>
      </div>
    {/if}

    <!-- Results -->
    {#if isLoading}
      <div class="flex items-center justify-center h-64">
        <div class="text-center">
          <div class="w-10 h-10 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mx-auto mb-3"></div>
          <p class="text-slate-400 text-sm">Searching...</p>
        </div>
      </div>
    {:else if hasSearched && results.length === 0}
      <div class="flex items-center justify-center h-64">
        <div class="text-center">
          <p class="text-slate-400 mb-2">No movies found</p>
          <p class="text-slate-500 text-sm">Try adjusting your search or filters</p>
        </div>
      </div>
    {:else if results.length > 0}
      <div class="bg-slate-900/40 border border-slate-700/50 rounded-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-700/50">
                <th class="text-left py-4 px-5 text-xs font-medium text-slate-400 uppercase tracking-wider">Title</th>
                <th class="text-left py-4 px-5 text-xs font-medium text-slate-400 uppercase tracking-wider hidden sm:table-cell">Year</th>
                <th class="text-left py-4 px-5 text-xs font-medium text-slate-400 uppercase tracking-wider hidden md:table-cell">Runtime</th>
                <th class="text-left py-4 px-5 text-xs font-medium text-slate-400 uppercase tracking-wider">Rating</th>
              </tr>
            </thead>
            <tbody>
              {#each results as movie, i}
                <tr class="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors {i === results.length - 1 ? 'border-b-0' : ''}">
                  <td class="py-4 px-5">
                    <span class="text-white font-medium">{movie.name || '—'}</span>
                  </td>
                  <td class="py-4 px-5 text-slate-400 hidden sm:table-cell">
                    {formatDate(movie.release)}
                  </td>
                  <td class="py-4 px-5 text-slate-400 hidden md:table-cell">
                    {formatRuntime(movie.runtime_minutes)}
                  </td>
                  <td class="py-4 px-5">
                    {#if movie.rating}
                      <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-purple-500/20 text-purple-400 text-sm font-medium">
                        ⭐ {movie.rating.toFixed(1)}
                      </span>
                    {:else}
                      <span class="text-slate-500">—</span>
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
        
        <div class="px-5 py-3 border-t border-slate-700/50 bg-slate-900/60">
          <p class="text-xs text-slate-500">Showing {results.length} result{results.length !== 1 ? 's' : ''}</p>
        </div>
      </div>
    {:else}
      <!-- Empty State -->
      <div class="flex items-center justify-center h-64">
        <div class="text-center">
          <Search class="w-12 h-12 text-slate-700 mx-auto mb-4" />
          <p class="text-slate-400 mb-2">Start your search</p>
          <p class="text-slate-500 text-sm">Enter a movie title or apply filters to find movies</p>
        </div>
      </div>
    {/if}
  </div>
</div>
