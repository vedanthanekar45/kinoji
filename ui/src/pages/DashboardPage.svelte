<script>
  import MetricCard from '../lib/components/MetricCard.svelte';
  import ChartCard from '../lib/components/ChartCard.svelte';

  const metrics = [
    { title: 'Total Movies', value: '60,124', icon: '🎬', trend: '+2.4%' },
    { title: 'Avg Runtime', value: '114 min', icon: '⏱️', trend: '+8 min' },
    { title: 'Top Genre', value: 'Drama', icon: '🎭', trend: '28%' },
  ];

  const genreData = [
    { name: 'Drama', count: 18240, color: 'sky' },
    { name: 'Comedy', count: 12450, color: 'purple' },
    { name: 'Action', count: 9870, color: 'emerald' },
    { name: 'Horror', count: 6230, color: 'rose' },
    { name: 'Sci-Fi', count: 4120, color: 'amber' },
  ];

  const recentInsights = [
    { text: "Movies released in December have 12% higher box office", time: "2h ago" },
    { text: "Average budget increased 340% since 1990", time: "5h ago" },
    { text: "Sequels perform 23% worse in ratings", time: "1d ago" },
  ];
</script>

<div class="min-h-screen pt-24 pb-12 px-6">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-10">
      <h1 class="text-4xl font-medium text-white mb-2">Dashboard</h1>
      <p class="text-white/50">Overview of 60,000+ movies from 1920-2024</p>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      {#each metrics as metric}
        <MetricCard 
          title={metric.title} 
          value={metric.value} 
          icon={metric.icon}
          trend={metric.trend}
        />
      {/each}
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
      <ChartCard 
        title="Runtime Creep" 
        description="Average movie runtime by decade (1950-2024)"
        type="line"
      />
      <ChartCard 
        title="Genre Popularity" 
        description="Number of movies by genre"
        type="bar"
      />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Rating Distribution -->
      <div class="lg:col-span-2">
        <ChartCard 
          title="Rating Distribution" 
          description="Distribution of IMDB ratings (1-10)"
          type="histogram"
        />
      </div>

      <!-- Sidebar Stats -->
      <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-6">
        <h3 class="text-lg font-medium text-white mb-4 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-purple-500"></span>
          Top Genres
        </h3>
        <div class="space-y-4">
          {#each genreData as genre}
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-white/80">{genre.name}</span>
                <span class="text-white/50">{genre.count.toLocaleString()}</span>
              </div>
              <div class="h-2 bg-white/10 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-purple-500 rounded-full transition-all duration-1000"
                  style="width: {(genre.count / 18240) * 100}%"
                ></div>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <!-- Recent Insights -->
    <div class="mt-10">
      <h3 class="text-lg font-medium text-white mb-4 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-400">
          <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
        </svg>
        AI Insights
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {#each recentInsights as insight}
          <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-4 hover:bg-white/10 transition-all cursor-pointer group">
            <p class="text-sm text-white/70 mb-2 group-hover:text-white transition-colors">{insight.text}</p>
            <span class="text-xs text-white/40">{insight.time}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>
