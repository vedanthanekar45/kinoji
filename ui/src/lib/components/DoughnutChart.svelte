<script>
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  /** @type {{ data: Array<{label: string, value: number}>, title?: string }} */
  let { data = [], title = '' } = $props();

  let canvas;
  let chart;

  const colors = [
    '#a855f7', '#ec4899', '#06b6d4', '#10b981', '#f59e0b',
    '#8b5cf6', '#f43f5e', '#14b8a6', '#84cc16', '#eab308'
  ];

  onMount(() => {
    if (!data.length) return;

    chart = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          data: data.map(d => d.value),
          backgroundColor: colors.slice(0, data.length).map(c => c + 'dd'),
          borderColor: '#0f172a',
          borderWidth: 3,
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: 'rgba(255,255,255,0.7)',
              padding: 16,
              usePointStyle: true,
              pointStyle: 'circle',
              font: { size: 12 }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleColor: '#fff',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8
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
