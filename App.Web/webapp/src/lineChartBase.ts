import Chart from 'chart.js/auto'

export default function baseChart(target: string, title:string, range:number):Chart {
    let chart = new Chart(target, {
        type: 'line',
        data: {
          labels: [...Array(range).keys()].map(i => i),
          datasets: [
            {
              borderWidth: 1,
              label: title,
              data: [],
              stepped: false,
              borderColor: "#e44f22",
              backgroundColor: '#e44f2210',
              fill: true,
              pointRadius: 0,
            }
          ]
        },
        options: {
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false,
          },
          scales: {
            x: {
              grid: {
                color: '#2C323F'
              }
            },
            y: {
              grid: {
                color: '#2C323F',
              },
            }
          }
        }
      })

      return chart
}