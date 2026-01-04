const API_BASE = 'http://localhost:8000/api';

let currentPage = 1, totalPages = 1, currentFilter = 'ALL', currentSort = 'marketValue-desc', selectedPlayerId = null, radarChart = null, currentPlayer = null;
let comparePlayer1 = null, comparePlayer2 = null, compareRadarChart = null, currentCompareCategory = 'attacking';

const $ = id => document.getElementById(id);

document.addEventListener('DOMContentLoaded', () => {
    loadPlayers();
    setupEvents();
});

function setupEvents() {
    $('searchInput').addEventListener('keypress', e => { if (e.key === 'Enter') { currentPage = 1; loadPlayers(); } });
    $('positionFilters').addEventListener('click', e => {
        if (e.target.classList.contains('tab')) {
            $('positionFilters').querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.position;
            currentPage = 1;
            loadPlayers();
        }
    });
    $('sortSelect').addEventListener('change', () => { currentSort = $('sortSelect').value; currentPage = 1; loadPlayers(); });
    $('prevPage').addEventListener('click', () => { if (currentPage > 1) { currentPage--; loadPlayers(); } });
    $('nextPage').addEventListener('click', () => { if (currentPage < totalPages) { currentPage++; loadPlayers(); } });

    document.querySelector('.stats-tabs').addEventListener('click', e => {
        if (e.target.classList.contains('stats-tab') && currentPlayer) {
            document.querySelectorAll('.stats-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            renderDetailedStats(currentPlayer.detailedStats[e.target.dataset.cat]);
        }
    });

    // View tabs (Player / Compare)
    document.querySelector('.view-tabs').addEventListener('click', e => {
        if (e.target.classList.contains('view-tab')) {
            document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            const view = e.target.dataset.view;
            $('playerView').classList.toggle('hidden', view !== 'player');
            $('compareView').classList.toggle('hidden', view !== 'compare');
        }
    });

    // Compare player search
    setupCompareSearch('compareSearch1', 'compareDropdown1', 1);
    setupCompareSearch('compareSearch2', 'compareDropdown2', 2);

    // Compare stats tabs
    document.querySelector('.compare-stats-tabs').addEventListener('click', e => {
        if (e.target.classList.contains('compare-stats-tab') && comparePlayer1 && comparePlayer2) {
            document.querySelectorAll('.compare-stats-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentCompareCategory = e.target.dataset.cat;
            renderCompareStats(comparePlayer1.detailedStats[currentCompareCategory], comparePlayer2.detailedStats[currentCompareCategory]);
        }
    });

    // Close dropdowns on outside click
    document.addEventListener('click', e => {
        if (!e.target.closest('.compare-select-box')) {
            $('compareDropdown1').classList.add('hidden');
            $('compareDropdown2').classList.add('hidden');
        }
    });
}

function setupCompareSearch(inputId, dropdownId, playerNum) {
    const input = $(inputId);
    const dropdown = $(dropdownId);
    let debounce = null;

    input.addEventListener('input', () => {
        clearTimeout(debounce);
        debounce = setTimeout(async () => {
            const query = input.value.trim();
            if (query.length < 2) {
                dropdown.classList.add('hidden');
                return;
            }
            try {
                const res = await fetch(`${API_BASE}/players?search=${encodeURIComponent(query)}&limit=10`);
                const data = await res.json();
                if (data.players.length > 0) {
                    dropdown.innerHTML = data.players.map(p => `
                        <div class="compare-dropdown-item" data-id="${p.playerId}">
                            <div class="player-name">${esc(p.name)}</div>
                            <div class="player-team">${esc(p.teamName)} · ${p.positionGroup}</div>
                        </div>
                    `).join('');
                    dropdown.classList.remove('hidden');
                } else {
                    dropdown.innerHTML = '<div class="compare-dropdown-item" style="color:var(--text-muted)">No players found</div>';
                    dropdown.classList.remove('hidden');
                }
            } catch (e) {
                console.error(e);
            }
        }, 300);
    });

    input.addEventListener('focus', () => {
        if (dropdown.innerHTML && input.value.trim().length >= 2) {
            dropdown.classList.remove('hidden');
        }
    });

    dropdown.addEventListener('click', async e => {
        const item = e.target.closest('.compare-dropdown-item');
        if (item && item.dataset.id) {
            try {
                const res = await fetch(`${API_BASE}/players/${item.dataset.id}`);
                const player = await res.json();
                if (playerNum === 1) {
                    comparePlayer1 = player;
                    $('selectedPlayer1').textContent = player.name;
                } else {
                    comparePlayer2 = player;
                    $('selectedPlayer2').textContent = player.name;
                }
                input.value = player.name;
                dropdown.classList.add('hidden');
                updateComparison();
            } catch (e) { console.error(e); }
        }
    });
}

function updateComparison() {
    if (!comparePlayer1 || !comparePlayer2) {
        $('compareContent').classList.add('hidden');
        return;
    }
    $('compareContent').classList.remove('hidden');

    // Render player info headers
    $('compareInfo1').innerHTML = `
        <div class="name">${esc(comparePlayer1.name)}</div>
        <div class="team">${esc(comparePlayer1.teamName)} · ${comparePlayer1.position}</div>
        <div class="value">${fmtVal(comparePlayer1.marketValueCurrent)}</div>
    `;
    $('compareInfo2').innerHTML = `
        <div class="name">${esc(comparePlayer2.name)}</div>
        <div class="team">${esc(comparePlayer2.teamName)} · ${comparePlayer2.position}</div>
        <div class="value">${fmtVal(comparePlayer2.marketValueCurrent)}</div>
    `;

    // Render comparison radar
    updateCompareRadar(comparePlayer1.radar, comparePlayer2.radar);

    // Render stats tabs - reset to attacking
    document.querySelectorAll('.compare-stats-tab').forEach((t, i) => t.classList.toggle('active', i === 0));
    currentCompareCategory = 'attacking';
    renderCompareStats(comparePlayer1.detailedStats.attacking, comparePlayer2.detailedStats.attacking);

    // Render season overview comparison
    renderCompareSeasonOverview();
}

function updateCompareRadar(r1, r2) {
    const ctx = $('compareRadarChart').getContext('2d');
    if (compareRadarChart) compareRadarChart.destroy();

    compareRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Attacking', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Rating'],
            datasets: [
                {
                    label: comparePlayer1.name,
                    data: [r1.attacking, r1.passing, r1.dribbling, r1.defending, r1.physical, r1.rating],
                    fill: true,
                    backgroundColor: 'rgba(88, 166, 255, 0.15)',
                    borderColor: '#58a6ff',
                    pointBackgroundColor: '#58a6ff',
                    pointRadius: 3,
                    borderWidth: 1.5
                },
                {
                    label: comparePlayer2.name,
                    data: [r2.attacking, r2.passing, r2.dribbling, r2.defending, r2.physical, r2.rating],
                    fill: true,
                    backgroundColor: 'rgba(163, 113, 247, 0.15)',
                    borderColor: '#a371f7',
                    pointBackgroundColor: '#a371f7',
                    pointRadius: 3,
                    borderWidth: 1.5
                }
            ]
        },
        options: {
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
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#8b949e',
                        font: { size: 10 },
                        boxWidth: 12,
                        padding: 10
                    }
                }
            }
        }
    });
}

function renderCompareStats(stats1, stats2) {
    const keys = Object.keys(stats1);
    $('compareStatsContent').innerHTML = keys.map(k => {
        const v1 = stats1[k] ?? 0;
        const v2 = stats2[k] ?? 0;
        const max = Math.max(v1, v2, 1);
        const pct1 = (v1 / max) * 100;
        const pct2 = (v2 / max) * 100;
        const better1 = v1 > v2;
        const better2 = v2 > v1;
        const fmtV = v => typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(1) : v;

        return `
            <div class="compare-stats-row">
                <span class="stat-value left ${better1 ? 'better' : ''}">${fmtV(v1)}</span>
                <div>
                    <div class="stat-label">${k}</div>
                    <div class="stat-bar-container">
                        <div class="stat-bar left" style="width:${pct1}%"></div>
                    </div>
                    <div class="stat-bar-container" style="margin-top:2px">
                        <div class="stat-bar right" style="width:${pct2}%"></div>
                    </div>
                </div>
                <span class="stat-value right ${better2 ? 'better' : ''}">${fmtV(v2)}</span>
            </div>
        `;
    }).join('');
}

function renderCompareSeasonOverview() {
    const stats = [
        { key: 'Apps', v1: comparePlayer1.appearances || 0, v2: comparePlayer2.appearances || 0 },
        { key: 'Goals', v1: comparePlayer1.goals ? Math.floor(comparePlayer1.goals) : 0, v2: comparePlayer2.goals ? Math.floor(comparePlayer2.goals) : 0 },
        { key: 'Assists', v1: comparePlayer1.assists ? Math.floor(comparePlayer1.assists) : 0, v2: comparePlayer2.assists ? Math.floor(comparePlayer2.assists) : 0 },
        { key: 'Mins', v1: comparePlayer1.minutesPlayed ? Math.round(comparePlayer1.minutesPlayed) : 0, v2: comparePlayer2.minutesPlayed ? Math.round(comparePlayer2.minutesPlayed) : 0 }
    ];

    $('compareSeasonGrid').innerHTML = stats.map(s => {
        const better1 = s.v1 > s.v2;
        const better2 = s.v2 > s.v1;
        return `
            <div class="compare-season-item">
                <span class="val left ${better1 ? 'better' : ''}">${s.v1.toLocaleString()}</span>
                <span class="label">${s.key}</span>
                <span class="val right ${better2 ? 'better' : ''}">${s.v2.toLocaleString()}</span>
            </div>
        `;
    }).join('');
}

async function loadPlayers() {
    $('loadingIndicator').style.display = 'flex';
    const [sortBy, sortOrder] = currentSort.split('-');
    const params = new URLSearchParams({ page: currentPage, limit: 50, sortBy, sortOrder });
    if (currentFilter !== 'ALL') params.append('positionGroup', currentFilter);
    const search = $('searchInput').value.trim();
    if (search) params.append('search', search);

    try {
        const res = await fetch(`${API_BASE}/players?${params}`);
        const data = await res.json();
        renderTable(data.players);
        totalPages = data.totalPages;
        $('prevPage').disabled = currentPage <= 1;
        $('nextPage').disabled = currentPage >= totalPages;
        $('pageInfo').textContent = `${currentPage}/${totalPages}`;
        $('totalPlayers').textContent = data.total.toLocaleString();
    } catch (e) {
        $('playerTableBody').innerHTML = '<tr><td colspan="6" style="text-align:center;padding:30px;color:#6e7681">Failed to load</td></tr>';
    }
    $('loadingIndicator').style.display = 'none';
}

function renderTable(players) {
    const start = (currentPage - 1) * 50;
    $('playerTableBody').innerHTML = players.map((p, i) => `
        <tr class="${p.playerId === selectedPlayerId ? 'selected' : ''}" onclick="selectPlayer(${p.playerId})">
            <td>${start + i + 1}</td>
            <td><div class="player-cell"><span class="name">${esc(p.name)}</span><span class="team">${esc(p.teamName)}</span></div></td>
            <td><span class="pos-tag ${p.positionGroup}">${p.positionGroup}</span></td>
            <td>${p.age ? Math.floor(p.age) : '-'}</td>
            <td>${p.rating ? p.rating.toFixed(2) : '-'}</td>
            <td class="value-col">${fmtVal(p.marketValue)}</td>
        </tr>
    `).join('');
}

async function selectPlayer(id) {
    selectedPlayerId = id;
    document.querySelectorAll('.player-table tbody tr').forEach(r => r.classList.remove('selected'));
    event.currentTarget.classList.add('selected');

    try {
        const res = await fetch(`${API_BASE}/players/${id}`);
        currentPlayer = await res.json();
        renderDetail(currentPlayer);
    } catch (e) { console.error(e); }
}

function renderDetail(p) {
    $('detailPlaceholder').style.display = 'none';
    $('detailContent').style.display = 'block';

    $('playerName').textContent = p.name;
    $('playerTeam').textContent = p.teamName;
    $('playerPosition').textContent = p.position;
    $('marketValue').textContent = fmtVal(p.marketValueCurrent);

    const trend = $('valueTrend');
    trend.className = 'trend ' + p.marketValueTrend;
    trend.textContent = p.marketValueTrend === 'up' ? '↑' : p.marketValueTrend === 'down' ? '↓' : '';

    $('playerAge').textContent = p.age ? Math.floor(p.age) : '-';
    $('playerHeight').textContent = p.height ? p.height.toFixed(2) + 'm' : '-';
    $('playerFoot').textContent = p.preferredFoot || '-';
    $('playerRating').textContent = p.rating ? p.rating.toFixed(2) : '-';

    $('statApps').textContent = p.appearances || 0;
    $('statGoals').textContent = p.goals ? Math.floor(p.goals) : 0;
    $('statAssists').textContent = p.assists ? Math.floor(p.assists) : 0;
    $('statMinutes').textContent = p.minutesPlayed ? Math.round(p.minutesPlayed).toLocaleString() : '-';

    $('contractUntil').textContent = p.contractUntil ? fmtDate(p.contractUntil) : '-';
    $('previousValue').textContent = fmtVal(p.marketValuePrevious);

    updateRadar(p.radar);

    document.querySelectorAll('.stats-tab').forEach((t, i) => t.classList.toggle('active', i === 0));
    renderDetailedStats(p.detailedStats.attacking);
}

function renderDetailedStats(stats) {
    $('statsContent').innerHTML = Object.entries(stats).map(([k, v]) =>
        `<div class="stats-row"><span>${k}</span><span>${typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(1) : v}</span></div>`
    ).join('');
}

function updateRadar(r) {
    const ctx = $('radarChart').getContext('2d');
    if (radarChart) radarChart.destroy();

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Attacking', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Rating'],
            datasets: [{
                data: [r.attacking, r.passing, r.dribbling, r.defending, r.physical, r.rating],
                fill: true,
                backgroundColor: 'rgba(88, 166, 255, 0.15)',
                borderColor: '#58a6ff',
                pointBackgroundColor: '#58a6ff',
                pointRadius: 3,
                borderWidth: 1.5
            }]
        },
        options: {
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
            plugins: { legend: { display: false } }
        }
    });
}

function fmtVal(v) { return v == null ? '-' : v >= 1e6 ? '€' + (v / 1e6).toFixed(1) + 'M' : v >= 1e3 ? '€' + (v / 1e3).toFixed(0) + 'K' : '€' + v; }
function fmtDate(d) { try { return new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }); } catch { return d.split(' ')[0]; } }
function esc(t) { const d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

window.selectPlayer = selectPlayer;

