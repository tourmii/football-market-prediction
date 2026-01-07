import './PlayerTable.css';

const POSITION_COLORS = {
    GK: '#d29922',
    DEF: '#1f6feb',
    MID: '#238636',
    ATT: '#da3633',
};

function formatValue(value) {
    if (value == null) return '-';
    if (value >= 1e6) return `€${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `€${(value / 1e3).toFixed(0)}K`;
    return `€${value}`;
}

export default function PlayerTable({
    players,
    loading,
    currentPage,
    totalPages,
    selectedPlayerId,
    onSelectPlayer,
    onPageChange
}) {
    const startIndex = (currentPage - 1) * 50;

    return (
        <section className="players">
            <table className="player-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Player</th>
                        <th>Pos</th>
                        <th>Age</th>
                        <th>Rating</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {players.map((player, index) => (
                        <tr
                            key={player.playerId}
                            className={player.playerId === selectedPlayerId ? 'selected' : ''}
                            onClick={() => onSelectPlayer(player.playerId)}
                        >
                            <td>{startIndex + index + 1}</td>
                            <td>
                                <div className="player-cell">
                                    <span className="name">{player.name}</span>
                                    <span className="team">{player.teamName}</span>
                                </div>
                            </td>
                            <td>
                                <span
                                    className="pos-tag"
                                    style={{
                                        background: POSITION_COLORS[player.positionGroup] || '#6e7681',
                                        color: player.positionGroup === 'GK' ? '#000' : '#fff'
                                    }}
                                >
                                    {player.positionGroup}
                                </span>
                            </td>
                            <td>{player.age ? Math.floor(player.age) : '-'}</td>
                            <td>{player.rating ? player.rating.toFixed(2) : '-'}</td>
                            <td className="value-col">{formatValue(player.marketValue)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                </div>
            )}

            <div className="pagination">
                <button
                    onClick={() => onPageChange(currentPage - 1)}
                    disabled={currentPage <= 1}
                >
                    ←
                </button>
                <span className="page-info">{currentPage}/{totalPages}</span>
                <button
                    onClick={() => onPageChange(currentPage + 1)}
                    disabled={currentPage >= totalPages}
                >
                    →
                </button>
            </div>
        </section>
    );
}
