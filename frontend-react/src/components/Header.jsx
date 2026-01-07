import './Header.css';

const POSITION_FILTERS = ['ALL', 'GK', 'DEF', 'MID', 'ATT'];

const SORT_OPTIONS = [
    { value: 'marketValue-desc', label: 'Value (High)' },
    { value: 'rating-desc', label: 'Rating (High)' },
    { value: 'goals-desc', label: 'Goals' },
    { value: 'age-asc', label: 'Age (Young)' },
];

export default function Header({
    currentFilter,
    onFilterChange,
    currentSort,
    onSortChange,
    searchValue,
    onSearchChange,
    onSearchSubmit,
    totalPlayers
}) {
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            onSearchSubmit();
        }
    };

    return (
        <header className="header">
            <h1 className="logo">
                <img src="/football-logo.png" alt="Football" className="logo-icon" />
                Player Analytics
            </h1>
            <div className="header-controls">
                <div className="filter-tabs">
                    {POSITION_FILTERS.map(pos => (
                        <button
                            key={pos}
                            className={`tab ${currentFilter === pos ? 'active' : ''}`}
                            onClick={() => onFilterChange(pos)}
                        >
                            {pos}
                        </button>
                    ))}
                </div>

                <select
                    className="sort-select"
                    value={currentSort}
                    onChange={(e) => onSortChange(e.target.value)}
                >
                    {SORT_OPTIONS.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                </select>

                <div className="search-box">
                    <input
                        type="text"
                        placeholder="Search player..."
                        value={searchValue}
                        onChange={(e) => onSearchChange(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                </div>

                <div className="player-count">
                    <span>{totalPlayers.toLocaleString()}</span> players
                </div>
            </div>
        </header>
    );
}
