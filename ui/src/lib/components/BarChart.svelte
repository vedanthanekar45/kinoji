<script>
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  /** @type {{ data: Array<{label: string, value: number}>, title?: string, horizontal?: boolean, colors?: string[] }} */
  let { data = [], title = '', horizontal = false, colors = null } = $props();

  let canvas;
  let chart;

  const defaultColors = [
    '#a855f7', '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6',
    '#c084fc', '#d946ef', '#e879f9', '#f0abfc', '#f5d0fe'
  ];

  onMount(() => {
    if (!data.length) return;

    const chartColors = colors || defaultColors.slice(0, data.length);

    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          label: title,
          data: data.map(d => d.value),
          backgroundColor: chartColors.map(c => c + 'cc'),
          borderColor: chartColors,
          borderWidth: 1,
          borderRadius: 6,
          borderSkipped: false
        }]
      },
      options: {
        indexAxis: horizontal ? 'y' : 'x',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleColor: '#fff',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false
          }
        },
        scales: {
          x: {
            border: { display: false },
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: 'rgba(255,255,255,0.4)', maxRotation: 45 }
          },
          y: {
            border: { display: false },
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: 'rgba(255,255,255,0.4)' },
            beginAtZero: true
          }
        }
      }
    });
  });

  onDestroy(() => {
    if (chart) chart.destroy();
  });

  $effect(() => {
    if (chart && data.length) {
      chart.data.labels = data.map(d => d.label);
      chart.data.datasets[0].data = data.map(d => d.value);
      chart.update('none');
    }
  });
</script>

<canvas bind:this={canvas}></canvas>
