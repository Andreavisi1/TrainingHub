// File: skills-chart.js
function createSkillsRadarChart() {
    const ctx = document.getElementById('skillsRadarChart').getContext('2d');
    
    // Dati delle skill
    const skillsData = {
        leadership: 75,
        technical: 85,
        communication: 80,
        problemSolving: 90,
        teamwork: 85,
        creativity: 70
    };
    
    // Crea il grafico radar
    const skillsChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Leadership', 'Technical', 'Communication', 'Problem Solving', 'Teamwork', 'Creativity'],
            datasets: [{
                data: Object.values(skillsData), // Rimosso il label
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderColor: 'rgba(79, 70, 229, 1)',
                pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(79, 70, 229, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // ❌ Disabilita completamente la legenda
                }
            }
        }
    });

    return skillsChart;
}
