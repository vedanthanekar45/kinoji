<script>
  import "./app.css"
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</svelte:head>

<main class="landing">
  <a href="https://github.com/vedanthanekar45/kinoji" target="_blank" rel="noreferrer" class="github-link" aria-label="Visit GitHub profile">
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
  </a>

  <div class="content">
    <h1>Decoding the DNA of Cinema</h1>
    
    <div class="search-container">
      <input type="text" placeholder="Generate insights with AI or click one of the buttons below.." class="search-input" />
    </div>

    <div class="buttons-container">
      <button class="btn btn-primary">Go to Dashboard</button>
      <span class="or-text">or</span>
      <button class="btn btn-secondary">Curate your own movie</button>
    </div>
  </div>
</main>

<style>
  :global(*) {
    font-family: 'Funnel Display', sans-serif;
  }

  .landing {
    width: 100vw;
    height: 100vh;
    background-image: url('/kinoji.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  .content {
    text-align: center;
    z-index: 10;
    padding: 1rem;
    width: 100%;
    max-width: 800px;
  }

  h1 {
    font-size: clamp(1.75rem, 5vw, 3.5rem);
    font-weight: 700;
    color: white;
    margin-bottom: 1.5rem;
  }

  .search-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    padding: 0 1rem;
  }

  .search-input {
    width: 100%;
    max-width: 600px;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px 8px 8px 8px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
    outline: none;
    backdrop-filter: blur(4px);
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  /* Buttons */
  .buttons-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .btn-primary {
    background: transparent;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.5);
  }

  .btn-primary:hover {
    background: #f0f0f0;
    color: black;
  }

  .btn-secondary {
    background: transparent;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.5);
  }

  .btn-secondary:hover {
    background: #f0f0f0;
    color: black;
  }

  .or-text {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.9rem;
  }

  /* GitHub link */
  .github-link {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    color: rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
    z-index: 20;
  }

  .github-link:hover {
    color: white;
    transform: scale(1.1);
  }

  /* Mobile styles */
  @media (max-width: 600px) {
    h1 {
      margin-bottom: 1rem;
    }

    .search-input {
      font-size: 0.9rem;
      padding: 0.6rem 0.8rem;
    }

    .buttons-container {
      flex-direction: column;
      gap: 0.75rem;
    }

    .or-text {
      display: none;
    }

    .btn {
      width: 100%;
      max-width: 250px;
    }

    .github-link {
      top: 1rem;
      bottom: auto;
      right: auto;
      left: 50%;
      transform: translateX(-50%);
    }

    .github-link:hover {
      transform: translateX(-50%) scale(1.1);
    }
  }
</style>
