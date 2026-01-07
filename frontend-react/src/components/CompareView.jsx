import { useState, useEffect, useRef } from 'react';
import { useApi } from '../hooks/useApi';
import RadarChart from './RadarChart';
import ValueChange from './ValueChange';
import './CompareView.css';

const STAT_CATEGORIES = ['attacking', 'passing', 'dribbling', 'defending', 'physical'];

function formatValue(value) {
    if (value == null) return '-';
    if (value >= 1e6) return `€${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `€${(value / 1e3).toFixed(0)}K`;
    return `€${value}`;
}

function PlayerSearchBox({ label, selectedPlayer, onSelect, searchPlayers }) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const debounceRef = useRef(null);
    const boxRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (boxRef.current && !boxRef.current.contains(e.target)) {
                setShowDropdown(false);
            }
        };
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, []);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setQuery(value);

        clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(async () => {
            if (value.length >= 2) {
                const players = await searchPlayers(value);
                setResults(players);
                setShowDropdown(true);
            } else {
                setResults([]);
                setShowDropdown(false);
            }
        }, 300);
    };

    const handleSelect = (player) => {
        onSelect(player);
        setQuery(player.name);
        setShowDropdown(false);
    };

    return (
        <div className="compare-select-box" ref={boxRef}>
            <label>{label}</label>
            <input
                type="text"
                placeholder="Search player..."
                value={query}
                onChange={handleInputChange}
                onFocus={() => results.length > 0 && setShowDropdown(true)}
            />
            {showDropdown && (
                <div className="compare-dropdown">
                    {results.length > 0 ? (
                        results.map(player => (
                            <div
                                key={player.playerId}
                                className="compare-dropdown-item"
                                onClick={() => handleSelect(player)}
                            >
                                <div className="player-name">{player.name}</div>
                                <div className="player-team">{player.teamName} · {player.positionGroup}</div>
                            </div>
                        ))
                    ) : (
                        <div className="compare-dropdown-item" style={{ color: 'var(--text-muted)' }}>
                            No players found
                        </div>
                    )}
                </div>
            )}
            <div className="selected-player">
                {selectedPlayer?.name || '-'}
            </div>
        </div>
    );
}

function CompareStatsRow({ statKey, value1, value2 }) {
    const max = Math.max(value1, value2, 1);
    const pct1 = (value1 / max) * 100;
    const pct2 = (value2 / max) * 100;
    const format = (v) => typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(1) : v;

    return (
        <div className="compare-stats-row">
            <span className={`stat-value left ${value1 > value2 ? 'better' : ''}`}>
                {format(value1)}
            </span>
            <div className="stat-middle">
                <div className="stat-label">{statKey}</div>
                <div className="stat-bar-container">
                    <div className="stat-bar left" style={{ width: `${pct1}%` }}></div>
                </div>
                <div className="stat-bar-container" style={{ marginTop: '2px' }}>
                    <div className="stat-bar right" style={{ width: `${pct2}%` }}></div>
                </div>
            </div>
            <span className={`stat-value right ${value2 > value1 ? 'better' : ''}`}>
                {format(value2)}
            </span>
        </div>
    );
}

export default function CompareView() {
    const { searchPlayers, fetchPlayer } = useApi();
    const [player1, setPlayer1] = useState(null);
    const [player2, setPlayer2] = useState(null);
    const [activeTab, setActiveTab] = useState('attacking');

    const handleSelectPlayer = async (playerData, setPlayer) => {
        const fullPlayer = await fetchPlayer(playerData.playerId);
        if (fullPlayer) {
            setPlayer(fullPlayer);
        }
    };

    const showComparison = player1 && player2;
    const stats1 = player1?.detailedStats?.[activeTab] || {};
    const stats2 = player2?.detailedStats?.[activeTab] || {};

    return (
        <div className="compare-view">
            {/* Player Selectors */}
            <div className="compare-selectors">
                <PlayerSearchBox
                    label="Player 1"
                    selectedPlayer={player1}
                    onSelect={(p) => handleSelectPlayer(p, setPlayer1)}
                    searchPlayers={searchPlayers}
                />
                <div className="compare-vs">VS</div>
                <PlayerSearchBox
                    label="Player 2"
                    selectedPlayer={player2}
                    onSelect={(p) => handleSelectPlayer(p, setPlayer2)}
                    searchPlayers={searchPlayers}
                />
            </div>

            {/* Comparison Content */}
            {showComparison && (
                <div className="compare-content">
                    {/* Headers with Price Change */}
                    <div className="compare-header">
                        <div className="compare-player-info">
                            <div className="name">{player1.name}</div>
                            <div className="team">{player1.teamName} · {player1.position}</div>
                            <ValueChange
                                currentValue={player1.marketValueCurrent}
                                previousValue={player1.marketValuePrevious}
                                size="compact"
                            />
                        </div>
                        <div className="compare-player-info">
                            <div className="name">{player2.name}</div>
                            <div className="team">{player2.teamName} · {player2.position}</div>
                            <ValueChange
                                currentValue={player2.marketValueCurrent}
                                previousValue={player2.marketValuePrevious}
                                size="compact"
                            />
                        </div>
                    </div>

                    {/* Radar Comparison */}
                    <div className="compare-grid">
                        <div className="section">
                            <h3>Skill Profile Comparison</h3>
                            <div className="radar-box compare-radar">
                                <RadarChart
                                    data={player1.radar}
                                    compareData={player2.radar}
                                    playerName={player1.name}
                                    comparePlayerName={player2.name}
                                />
                            </div>
                        </div>

                        {/* Stats Comparison */}
                        <div className="section">
                            <h3>Stats Comparison</h3>
                            <div className="compare-stats-tabs">
                                {STAT_CATEGORIES.map(cat => (
                                    <button
                                        key={cat}
                                        className={`compare-stats-tab ${activeTab === cat ? 'active' : ''}`}
                                        onClick={() => setActiveTab(cat)}
                                    >
                                        {cat.charAt(0).toUpperCase() + cat.slice(1)}
                                    </button>
                                ))}
                            </div>
                            <div className="compare-stats-content">
                                {Object.keys(stats1).map(key => (
                                    <CompareStatsRow
                                        key={key}
                                        statKey={key}
                                        value1={stats1[key] ?? 0}
                                        value2={stats2[key] ?? 0}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Season Overview */}
                    <div className="section">
                        <h3>Season Overview</h3>
                        <div className="compare-season-grid">
                            {[
                                { key: 'Apps', v1: player1.appearances || 0, v2: player2.appearances || 0 },
                                { key: 'Goals', v1: Math.floor(player1.goals || 0), v2: Math.floor(player2.goals || 0) },
                                { key: 'Assists', v1: Math.floor(player1.assists || 0), v2: Math.floor(player2.assists || 0) },
                                { key: 'Mins', v1: Math.round(player1.minutesPlayed || 0), v2: Math.round(player2.minutesPlayed || 0) }
                            ].map(stat => (
                                <div key={stat.key} className="compare-season-item">
                                    <span className={`val left ${stat.v1 > stat.v2 ? 'better' : ''}`}>
                                        {stat.v1.toLocaleString()}
                                    </span>
                                    <span className="label">{stat.key}</span>
                                    <span className={`val right ${stat.v2 > stat.v1 ? 'better' : ''}`}>
                                        {stat.v2.toLocaleString()}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
