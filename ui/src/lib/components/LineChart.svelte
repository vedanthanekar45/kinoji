<script>
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  /** @type {{ data: Array<{label: string|number, value: number}>, title?: string, color?: string, fill?: boolean }} */
  let { data = [], title = '', color = '#a855f7', fill = true } = $props();

  let canvas;
  let chart;

  onMount(() => {
    if (!data.length) return;
    
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, color + '40');
    gradient.addColorStop(1, color + '00');

    chart = new Chart(canvas, {
      type: 'line',
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          label: title,
          data: data.map(d => d.value),
          borderColor: color,
          backgroundColor: fill ? gradient : 'transparent',
          borderWidth: 2,
          fill: fill,
          tension: 0.35,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: color,
          pointHoverBorderColor: '#fff',
          pointHoverBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: 'index'
        },
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
            ticks: { color: 'rgba(255,255,255,0.4)', maxRotation: 0, autoSkipPadding: 20 }
          },
          y: {
            border: { display: false },
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: 'rgba(255,255,255,0.4)' },
            beginAtZero: false
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
