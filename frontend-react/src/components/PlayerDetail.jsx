import { useState } from 'react';
import ValueChange from './ValueChange';
import RadarChart from './RadarChart';
import './PlayerDetail.css';

const STAT_CATEGORIES = ['attacking', 'passing', 'dribbling', 'defending', 'physical'];

function formatDate(dateStr) {
    if (!dateStr) return '-';
    try {
        return new Date(dateStr).toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    } catch {
        return dateStr.split(' ')[0];
    }
}

export default function PlayerDetail({ player }) {
    const [activeStatTab, setActiveStatTab] = useState('attacking');

    if (!player) {
        return (
            <div className="detail-empty">
                Select a player from the list
            </div>
        );
    }

    const detailedStats = player.detailedStats?.[activeStatTab] || {};

    return (
        <div className="detail-content">
            {/* Header with Name and Value */}
            <div className="detail-header">
                <div>
                    <h2 className="player-name">{player.name}</h2>
                    <p className="meta">
                        <span>{player.teamName}</span> · <span>{player.position}</span>
                    </p>
                </div>
                <ValueChange
                    currentValue={player.marketValueCurrent}
                    previousValue={player.marketValuePrevious}
                    size="large"
                />
            </div>

            {/* Info Row */}
            <div className="info-row">
                <div className="info-item">
                    <span>{player.age ? Math.floor(player.age) : '-'}</span>
                    <label>Age</label>
                </div>
                <div className="info-item">
                    <span>{player.height ? `${player.height.toFixed(2)}m` : '-'}</span>
                    <label>Height</label>
                </div>
                <div className="info-item">
                    <span>{player.preferredFoot || '-'}</span>
                    <label>Foot</label>
                </div>
                <div className="info-item">
                    <span>{player.rating ? player.rating.toFixed(2) : '-'}</span>
                    <label>Rating</label>
                </div>
            </div>

            {/* Two Column Grid */}
            <div className="detail-grid">
                {/* Left Column - Radar and Season */}
                <div className="detail-col">
                    <div className="section">
                        <h3>Skill Profile <span className="note">(Percentile vs All Players)</span></h3>
                        <RadarChart data={player.radar} playerName={player.name} />
                    </div>

                    <div className="section">
                        <h3>Season Overview</h3>
                        <div className="season-grid">
                            <div>
                                <span>{player.appearances || 0}</span>
                                <label>Apps</label>
                            </div>
                            <div>
                                <span>{player.goals ? Math.floor(player.goals) : 0}</span>
                                <label>Goals</label>
                            </div>
                            <div>
                                <span>{player.assists ? Math.floor(player.assists) : 0}</span>
                                <label>Assists</label>
                            </div>
                            <div>
                                <span>{player.minutesPlayed ? Math.round(player.minutesPlayed).toLocaleString() : '-'}</span>
                                <label>Mins</label>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column - Detailed Stats */}
                <div className="detail-col">
                    <div className="section">
                        <h3>Detailed Stats</h3>
                        <div className="stats-tabs">
                            {STAT_CATEGORIES.map(cat => (
                                <button
                                    key={cat}
                                    className={`stats-tab ${activeStatTab === cat ? 'active' : ''}`}
                                    onClick={() => setActiveStatTab(cat)}
                                >
                                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                                </button>
                            ))}
                        </div>
                        <div className="stats-content">
                            {Object.entries(detailedStats).map(([key, value]) => (
                                <div key={key} className="stats-row">
                                    <span>{key}</span>
                                    <span>
                                        {typeof value === 'number' && !Number.isInteger(value)
                                            ? value.toFixed(1)
                                            : value}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Contract Info */}
            <div className="contract-info">
                <span>Contract until <strong>{formatDate(player.contractUntil)}</strong></span>
            </div>
        </div>
    );
}
