<script>
  import "./app.css";
  import Navbar from "./lib/components/Navbar.svelte";
  import HomePage from "./pages/HomePage.svelte";
  import DashboardPage from "./pages/DashboardPage.svelte";
  import SearchPage from "./pages/SearchPage.svelte";
  import AIAnalysisPage from "./pages/AIAnalysisPage.svelte";

  let currentPage = $state('home');

  function navigate(page) {
    currentPage = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Funnel+Display:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</svelte:head>

<div class="min-h-screen bg-slate-950 text-slate-200 font-['Funnel_Display',sans-serif]">
  <!-- Navbar (hidden on home page) -->
  {#if currentPage !== 'home'}
    <Navbar {currentPage} onNavigate={navigate} />
  {/if}

  <!-- Page Content -->
  <main>
    {#if currentPage === 'home'}
      <HomePage onNavigate={navigate} />
    {:else if currentPage === 'dashboard'}
      <DashboardPage />
    {:else if currentPage === 'search'}
      <SearchPage />
    {:else if currentPage === 'ai-analysis'}
      <AIAnalysisPage />
    {/if}
  </main>
</div>