<script>
  import AnalysisCard from '../lib/components/AnalysisCard.svelte';

  let selectedTool = $state(null);
  let titleInput = $state('');
  let directorInput = $state('');

  const analysisTools = [
    {
      id: 'title-doctor',
      title: 'The Title Doctor',
      description: 'Input a movie title and our AI predicts its rating based on keywords, genre patterns, and historical data.',
      icon: '🩺'
    },
    {
      id: 'blue-ocean',
      title: 'Blue Ocean Detector',
      description: 'Discover untapped genre combinations. Find the "Sci-Fi Western" or "Horror Musical" gaps in cinema.',
      icon: '🌊'
    },
    {
      id: 'director-dna',
      title: 'Director DNA',
      description: 'Explore a director\'s career timeline, rating trends, genre preferences, and collaboration patterns.',
      icon: '🧬'
    }
  ];

  // Mock heatmap data for Blue Ocean
  const genreMatrix = [
    { g1: 'Action', g2: 'Romance', count: 245, opportunity: 'low' },
    { g1: 'Horror', g2: 'Musical', count: 12, opportunity: 'high' },
    { g1: 'Sci-Fi', g2: 'Western', count: 8, opportunity: 'high' },
    { g1: 'Comedy', g2: 'Thriller', count: 156, opportunity: 'medium' },
    { g1: 'Drama', g2: 'Animation', count: 89, opportunity: 'medium' },
    { g1: 'Fantasy', g2: 'Documentary', count: 3, opportunity: 'high' },
  ];

  function selectTool(id) {
    selectedTool = selectedTool === id ? null : id;
  }
</script>

<div class="min-h-screen pt-24 pb-12 px-6">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-10">
      <h1 class="text-4xl font-medium text-white mb-2">Analysis Tools</h1>
      <p class="text-white/50">AI-powered insights to decode cinema patterns</p>
    </div>

    <!-- Tool Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      {#each analysisTools as tool}
        <AnalysisCard 
          title={tool.title}
          description={tool.description}
          icon={tool.icon}
          onSelect={() => selectTool(tool.id)}
        />
      {/each}
    </div>

    <!-- Expanded Tool Panels -->
    {#if selectedTool === 'title-doctor'}
      <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-8 animate-fadeIn">
        <h3 class="text-2xl font-medium text-white mb-6 flex items-center gap-3">
          <span class="text-3xl">🩺</span>
          The Title Doctor
        </h3>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <label class="block text-sm text-white/50 mb-2">Enter your movie title</label>
            <input 
              type="text"
              bind:value={titleInput}
              placeholder="e.g., The Dark Knight Returns"
              class="w-full py-3 px-4 border border-white/20 rounded-xl bg-white/5 text-white outline-none focus:border-purple-500/50 transition-all placeholder:text-white/30"
            />
            <button class="mt-4 px-6 py-3 rounded-xl bg-purple-500 text-white font-medium hover:bg-purple-600 transition-colors cursor-pointer">
              Analyze Title
            </button>
          </div>
          
          <div class="bg-white/5 rounded-xl p-6 border border-white/10">
            <h4 class="text-sm text-white/50 mb-4">Prediction Results</h4>
            <div class="space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-white/70">Predicted Rating</span>
                <span class="text-2xl font-bold text-purple-400">7.8</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-white/70">Confidence</span>
                <span class="text-purple-400">High (87%)</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-white/70">Similar to</span>
                <span class="text-white/50">The Dark Knight (2008)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}

    {#if selectedTool === 'blue-ocean'}
      <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-8 animate-fadeIn">
        <h3 class="text-2xl font-medium text-white mb-6 flex items-center gap-3">
          <span class="text-3xl">🌊</span>
          Blue Ocean Detector
        </h3>
        
        <p class="text-white/50 mb-6">Genre combinations with the least competition (highest opportunity)</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {#each genreMatrix as combo}
            <div class="bg-white/5 rounded-xl p-4 border border-white/10 hover:border-purple-500/30 transition-all cursor-pointer">
              <div class="flex items-center gap-2 mb-3">
                <span class="px-2 py-1 rounded-lg bg-purple-500/20 text-purple-400 text-xs font-medium">{combo.g1}</span>
                <span class="text-white/30">+</span>
                <span class="px-2 py-1 rounded-lg bg-white/10 text-white/70 text-xs font-medium">{combo.g2}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-white/40">{combo.count} movies</span>
                <span class="text-xs px-2 py-1 rounded-full {combo.opportunity === 'high' ? 'bg-purple-500/20 text-purple-400' : 'bg-white/10 text-white/50'}">
                  {combo.opportunity} opportunity
                </span>
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    {#if selectedTool === 'director-dna'}
      <div class="bg-white/5 border border-white/10 backdrop-blur-md rounded-xl p-8 animate-fadeIn">
        <h3 class="text-2xl font-medium text-white mb-6 flex items-center gap-3">
          <span class="text-3xl">🧬</span>
          Director DNA
        </h3>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <label class="block text-sm text-white/50 mb-2">Search for a director</label>
            <input 
              type="text"
              bind:value={directorInput}
              placeholder="e.g., Christopher Nolan"
              class="w-full py-3 px-4 border border-white/20 rounded-xl bg-white/5 text-white outline-none focus:border-purple-500/50 transition-all placeholder:text-white/30"
            />
          </div>
          
          <div class="bg-white/5 rounded-xl p-6 border border-white/10">
            <h4 class="text-lg font-medium text-white mb-4">Christopher Nolan</h4>
            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-white/50">Total Films</span>
                <span class="text-white">12</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-white/50">Avg Rating</span>
                <span class="text-purple-400">8.2</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-white/50">Favorite Genre</span>
                <span class="text-white">Sci-Fi / Thriller</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-white/50">Avg Runtime</span>
                <span class="text-purple-400">152 min (+38 above avg)</span>
              </div>
            </div>
            
            <!-- Mini Timeline -->
            <div class="mt-6 pt-4 border-t border-white/10">
              <h5 class="text-xs text-white/40 mb-3">Career Timeline</h5>
              <div class="flex items-center gap-1">
                {#each [6.8, 7.2, 8.5, 8.8, 8.4, 8.6, 8.8, 8.4, 7.4, 8.5, 8.3, 7.8] as rating, i}
                  <div 
                    class="flex-1 rounded-sm bg-purple-500 transition-all hover:opacity-80"
                    style="height: {(rating / 10) * 40}px"
                    title="Film {i + 1}: {rating}"
                  ></div>
                {/each}
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .animate-fadeIn {
    animation: fadeIn 0.3s ease-out;
  }
</style>
