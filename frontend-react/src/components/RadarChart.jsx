import { useEffect, useRef } from 'react';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

const LABELS = ['Attacking', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Rating'];

export default function RadarChart({
    data,
    compareData = null,
    playerName = 'Player',
    comparePlayerName = 'Player 2'
}) {
    const datasets = [
        {
            label: playerName,
            data: [
                data?.attacking || 0,
                data?.passing || 0,
                data?.dribbling || 0,
                data?.defending || 0,
                data?.physical || 0,
                data?.rating || 0
            ],
            fill: true,
            backgroundColor: 'rgba(88, 166, 255, 0.15)',
            borderColor: '#58a6ff',
            pointBackgroundColor: '#58a6ff',
            pointRadius: 3,
            borderWidth: 1.5
        }
    ];

    if (compareData) {
        datasets.push({
            label: comparePlayerName,
            data: [
                compareData?.attacking || 0,
                compareData?.passing || 0,
                compareData?.dribbling || 0,
                compareData?.defending || 0,
                compareData?.physical || 0,
                compareData?.rating || 0
            ],
            fill: true,
            backgroundColor: 'rgba(163, 113, 247, 0.15)',
            borderColor: '#a371f7',
            pointBackgroundColor: '#a371f7',
            pointRadius: 3,
            borderWidth: 1.5
        });
    }

    const chartData = {
        labels: LABELS,
        datasets
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            r: {
                beginAtZero: true,
                max: 100,
                ticks: { display: false, stepSize: 25 },
                grid: { color: '#30363d' },
                angleLines: { color: '#30363d' },
                pointLabels: { color: '#8b949e', font: { size: 9 } }
            }
        },
        plugins: {
            legend: {
                display: !!compareData,
                position: 'bottom',
                labels: {
                    color: '#8b949e',
                    font: { size: 10 },
                    boxWidth: 12,
                    padding: 10
                }
            }
        }
    };

    return (
        <div className="radar-box">
            <Radar data={chartData} options={options} />
        </div>
    );
}
