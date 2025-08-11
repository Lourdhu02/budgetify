let expenseChart = null;

function createOrUpdateChart(labels = [], data = []) {
  const ctx = document.getElementById('expenseChart').getContext('2d');
  if (expenseChart) {
    expenseChart.data.labels = labels;
    expenseChart.data.datasets[0].data = data;
    expenseChart.update();
    return;
  }

  expenseChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Expenses',
        data: data,
        backgroundColor: '#4b4b4b',
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#fff' } }
      },
      scales: {
        y: {
          ticks: { color: "#fff" },
          grid: { color: "#222" }
        },
        x: {
          ticks: { color: "#fff" },
          grid: { color: "#222" }
        }
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", function(){
  // Initialize with server-passed data (if present)
  if (typeof expenseLabels !== 'undefined' && typeof expenseData !== 'undefined') {
    createOrUpdateChart(expenseLabels, expenseData);
  }
});
