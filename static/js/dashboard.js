// Graphs
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [
      [{% for data in client_data %}'{{ data.date|date:"Y-m-d" }}',{% endfor %}],
    datasets: [{
      label: 'Клиенты',
      data: [
        [{% for data in client_data %}{{ data.count }},{% endfor %}]
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


