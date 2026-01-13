<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  /** 
   * @type {{ 
   *   type: 'bar' | 'line' | 'pie' | 'list',
   *   data: Array<{label: string, value: number}>,
   *   title?: string 
   * }} 
   */
  let { type = 'bar', data = [], title = '' } = $props();

  let canvas: HTMLCanvasElement | null = $state(null);
  let chart: Chart | null = null;

  const colors = [
    '#a855f7', '#ec4899', '#06b6d4', '#10b981', '#f59e0b',
    '#8b5cf6', '#f43f5e', '#14b8a6', '#84cc16', '#eab308'
  ];

  function createChart() {
    if (!canvas || !data.length || type === 'list') return;
    
    if (chart) {
      chart.destroy();
    }

    const ctx = canvas.getContext('2d');

    const chartConfig = {
      bar: {
        type: 'bar' as const,
        data: {
          labels: data.map(d => d.label),
          datasets: [{
            label: title,
            data: data.map(d => d.value),
            backgroundColor: colors.slice(0, data.length).map(c => c + 'cc'),
            borderColor: colors.slice(0, data.length),
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleColor: '#fff',
              bodyColor: '#cbd5e1',
              padding: 12,
              cornerRadius: 8
            }
          },
          scales: {
            x: {
              border: { display: false },
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: 'rgba(255,255,255,0.5)', maxRotation: 45 }
            },
            y: {
              border: { display: false },
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: 'rgba(255,255,255,0.5)' },
              beginAtZero: true
            }
          }
        }
      },
      line: {
        type: 'line' as const,
        data: {
          labels: data.map(d => d.label),
          datasets: [{
            label: title,
            data: data.map(d => d.value),
            borderColor: '#a855f7',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.35,
            pointRadius: 3,
            pointHoverRadius: 6,
            pointBackgroundColor: '#a855f7'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleColor: '#fff',
              bodyColor: '#cbd5e1',
              padding: 12,
              cornerRadius: 8
            }
          },
          scales: {
            x: {
              border: { display: false },
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: 'rgba(255,255,255,0.5)' }
            },
            y: {
              border: { display: false },
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: 'rgba(255,255,255,0.5)' }
            }
          }
        }
      },
      pie: {
        type: 'doughnut' as const,
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
          cutout: '60%',
          plugins: {
            legend: {
              position: 'right' as const,
              labels: {
                color: 'rgba(255,255,255,0.7)',
                padding: 12,
                usePointStyle: true,
                pointStyle: 'circle',
                font: { size: 11 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleColor: '#fff',
              bodyColor: '#cbd5e1',
              padding: 12,
              cornerRadius: 8
            }
          }
        }
      }
    };

    const config = chartConfig[type];
    if (config) {
      chart = new Chart(canvas, config);
    }
  }

  onMount(() => {
    createChart();
  });

  onDestroy(() => {
    if (chart) chart.destroy();
  });

  $effect(() => {
    // Re-create chart when data or type changes
    if (data && type) {
      createChart();
    }
  });
</script>

{#if type === 'list'}
  <!-- Render as table for list type -->
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-slate-700/50">
          {#each Object.keys(data[0] || {}) as key}
            <th class="text-left py-3 px-4 text-xs font-medium text-slate-400 uppercase">{key}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each data.slice(0, 20) as row, i}
          <tr class="border-b border-slate-800/50 {i === Math.min(data.length, 20) - 1 ? 'border-b-0' : ''}">
            {#each Object.values(row) as value}
              <td class="py-3 px-4 text-slate-300">{value}</td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else}
  <canvas bind:this={canvas}></canvas>
{/if}
