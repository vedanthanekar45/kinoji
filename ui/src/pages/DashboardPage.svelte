<script>
  import { onMount } from 'svelte';
  import LineChart from '../lib/components/LineChart.svelte';
  import BarChart from '../lib/components/BarChart.svelte';
  import DoughnutChart from '../lib/components/DoughnutChart.svelte';

  const API_BASE = 'https://kinoji.duckdns.org';  

  // State
  let loading = $state(true);
  let topRowStats = $state(null);
  let moviesPerYear = $state([]);
  let runtimePerYear = $state([]);
  let ratingPerDecade = $state([]);
  let genresByMovies = $state([]);
  let genresByRating = $state([]);
  let countriesByMovies = $state([]);

  // Fetch all data
  onMount(async () => {
    try {
      const [
        topRowRes,
        moviesYearRes,
        runtimeYearRes,
        ratingDecadeRes,
        genresMoviesRes,
        genresRatingRes,
        countriesRes
      ] = await Promise.all([
        fetch(`${API_BASE}/dashboard/top-row`),
        fetch(`${API_BASE}/dashboard/movies-per-year`),
        fetch(`${API_BASE}/dashboard/avg-runtime-year`),
        fetch(`${API_BASE}/dashboard/avg-rating-decade`),
        fetch(`${API_BASE}/dashboard/top_genres_by_movies`),
        fetch(`${API_BASE}/dashboard/top_genres_by_rating`),
        fetch(`${API_BASE}/dashboard/top_countries_by_movies`)
      ]);

      topRowStats = await topRowRes.json();
      moviesPerYear = await moviesYearRes.json();
      runtimePerYear = await runtimeYearRes.json();
      ratingPerDecade = await ratingDecadeRes.json();
      genresByMovies = await genresMoviesRes.json();
      genresByRating = await genresRatingRes.json();
      countriesByMovies = await countriesRes.json();
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
    } finally {
      loading = false;
    }
  });

  // Transform data for charts
  const moviesYearData = $derived(
    moviesPerYear
      .filter(d => d.year >= 1970)
      .map(d => ({ label: d.year, value: d.count }))
  );

  const runtimeYearData = $derived(
    runtimePerYear
      .filter(d => d.year >= 1970)
      .map(d => ({ label: d.year, value: d.runtime }))
  );

  const ratingDecadeData = $derived(
    ratingPerDecade.map(d => ({ label: `${d.decade}s`, value: d.runtime }))
  );

  const genreMoviesData = $derived(
    genresByMovies.map(d => ({ label: d.genre, value: d.count }))
  );

  const genreRatingData = $derived(
    genresByRating.map(d => ({ label: d.genre, value: Number(d.average_rating) }))
  );

  const countryData = $derived(
    countriesByMovies.map(d => ({ label: d.country, value: d.count }))
  );
</script>

<div class="min-h-screen pt-20 pb-16 px-4 sm:px-6 lg:px-8">
  <div class="max-w-7xl mx-auto">
    
    <!-- Header -->
    <header class="mb-8 sm:mb-12">
      <h1 class="text-3xl sm:text-4xl font-semibold text-white mb-2">Dashboard</h1>
      <p class="text-slate-400 text-sm sm:text-base">Your movie collection at a glance</p>
    </header>

    {#if loading}
      <!-- Loading State -->
      <div class="flex items-center justify-center h-96">
        <div class="text-center">
          <div class="w-12 h-12 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-slate-400">Loading dashboard...</p>
        </div>
      </div>
    {:else}
      
      <!-- Top Stats Row -->
      <section class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
        <article class="bg-gradient-to-br from-purple-500/20 to-purple-600/5 border border-purple-500/20 rounded-2xl p-5 sm:p-6">
          <div class="flex items-center gap-3 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/></svg>
            <span class="text-xs uppercase tracking-wider text-slate-400 font-medium">Library Size</span>
          </div>
          <p class="text-2xl sm:text-3xl font-bold text-white">
            {topRowStats?.library_size?.toLocaleString() || '—'}
          </p>
          <p class="text-xs text-slate-500 mt-1">total movies</p>
        </article>

        <article class="bg-gradient-to-br from-cyan-500/20 to-cyan-600/5 border border-cyan-500/20 rounded-2xl p-5 sm:p-6">
          <div class="flex items-center gap-3 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-cyan-400"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span class="text-xs uppercase tracking-wider text-slate-400 font-medium">Watch Time</span>
          </div>
          <p class="text-xl sm:text-2xl font-bold text-white leading-tight">
            {topRowStats?.total_watch_time || '—'}
          </p>
          <p class="text-xs text-slate-500 mt-1">combined runtime</p>
        </article>

        <article class="bg-gradient-to-br from-amber-500/20 to-amber-600/5 border border-amber-500/20 rounded-2xl p-5 sm:p-6">
          <div class="flex items-center gap-3 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" class="text-amber-400"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <span class="text-xs uppercase tracking-wider text-slate-400 font-medium">Avg Rating</span>
          </div>
          <p class="text-2xl sm:text-3xl font-bold text-white">
            {topRowStats?.global_rating || '—'}
          </p>
          <p class="text-xs text-slate-500 mt-1">out of 5.0</p>
        </article>

        <article class="bg-gradient-to-br from-rose-500/20 to-rose-600/5 border border-rose-500/20 rounded-2xl p-5 sm:p-6">
          <div class="flex items-center gap-3 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-rose-400"><path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></svg>
            <span class="text-xs uppercase tracking-wider text-slate-400 font-medium">Oldest Film</span>
          </div>
          <p class="text-lg sm:text-xl font-bold text-white leading-tight truncate" title={topRowStats?.oldest_movie?.title}>
            {topRowStats?.oldest_movie?.title || '—'}
          </p>
          <p class="text-xs text-slate-500 mt-1">{topRowStats?.oldest_movie?.year || ''}</p>
        </article>
      </section>

      <!-- Main Charts Grid -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 mb-8 sm:mb-12">
        
        <!-- Movies Per Year -->
        <article class="bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Movie Releases Over Time</h2>
            <p class="text-sm text-slate-500">Number of movies released each year since 1970</p>
          </header>
          <div class="h-64 sm:h-72">
            {#if moviesYearData.length}
              <LineChart data={moviesYearData} title="Movies" color="#a855f7" />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>

        <!-- Average Runtime Per Year -->
        <article class="bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Runtime Trend</h2>
            <p class="text-sm text-slate-500">Average movie runtime in minutes by year</p>
          </header>
          <div class="h-64 sm:h-72">
            {#if runtimeYearData.length}
              <LineChart data={runtimeYearData} title="Minutes" color="#06b6d4" />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>
      </section>

      <!-- Secondary Charts -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 mb-8 sm:mb-12">
        
        <!-- Ratings by Decade -->
        <article class="bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Ratings by Decade</h2>
            <p class="text-sm text-slate-500">How movie ratings evolved</p>
          </header>
          <div class="h-56 sm:h-64">
            {#if ratingDecadeData.length}
              <BarChart data={ratingDecadeData} title="Avg Rating" colors={['#f59e0b']} />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>

        <!-- Top Genres by Movies -->
        <article class="lg:col-span-2 bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Most Popular Genres</h2>
            <p class="text-sm text-slate-500">Top 10 genres by number of movies</p>
          </header>
          <div class="h-56 sm:h-64">
            {#if genreMoviesData.length}
              <BarChart data={genreMoviesData} title="Movies" />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>
      </section>

      <!-- Bottom Row -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
        
        <!-- Genre Ratings -->
        <article class="bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Highest Rated Genres</h2>
            <p class="text-sm text-slate-500">Average ratings by genre</p>
          </header>
          <div class="h-64 sm:h-72">
            {#if genreRatingData.length}
              <BarChart data={genreRatingData} title="Rating" horizontal={true} colors={['#10b981']} />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>

        <!-- Top Countries -->
        <article class="bg-slate-900/50 border border-slate-700/50 rounded-2xl p-5 sm:p-6">
          <header class="mb-6">
            <h2 class="text-lg font-medium text-white">Movies by Country</h2>
            <p class="text-sm text-slate-500">Top producing countries</p>
          </header>
          <div class="h-64 sm:h-72">
            {#if countryData.length}
              <DoughnutChart data={countryData} title="Movies" />
            {:else}
              <div class="h-full flex items-center justify-center text-slate-500">No data</div>
            {/if}
          </div>
        </article>
      </section>

    {/if}
  </div>
</div>
