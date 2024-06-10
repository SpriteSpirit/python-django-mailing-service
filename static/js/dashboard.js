// Graphs
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [
      [{{ ', '.join(dates) }}],
    datasets: [{
      label: 'Клиенты',
      data: [
        [{{ ', '.join(counts) }}]
      ],
      lineTension: 0,
      backgroundColor: 'transparent',
      borderColor: '#007bff',
      borderWidth: 4,
      pointBackgroundColor: '#007bff'
    }]
  },
  options: {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        boxPadding: 3
      }
    }
  }
});


