import Chart from 'chart.js/auto'


export default async function densityChart() {
  const data = [
    { year: 1, count: 10 },
    { year: 2, count: 20 },
    { year: 3, count: 15 },
    { year: 4, count: 25 },
    { year: 5, count: 22 },
    { year: 6, count: 30 },
    { year: 7, count: 28 },
  ];

  new Chart(
    document.getElementById('density-chart'),
    {
      type: 'line',
      data: {
        labels: data.map(row => row.year),
        datasets: [
          {
            label: 'density',
            data: data.map(row => row.count),
            fill: true,
            backgroundColor: "#e44f2210",
            borderColor: "#e44f22",
            tension: 0.1,
          }
        ]
      }
    }
  );
};