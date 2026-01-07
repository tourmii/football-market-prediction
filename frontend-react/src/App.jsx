import { useState, useEffect, useCallback } from 'react';
import { useApi } from './hooks/useApi';
import Header from './components/Header';
import PlayerTable from './components/PlayerTable';
import PlayerDetail from './components/PlayerDetail';
import CompareView from './components/CompareView';
import './App.css';

export default function App() {
  const { loading, fetchPlayers, fetchPlayer } = useApi();

  // State
  const [players, setPlayers] = useState([]);
  const [totalPlayers, setTotalPlayers] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [currentFilter, setCurrentFilter] = useState('ALL');
  const [currentSort, setCurrentSort] = useState('marketValue-desc');
  const [searchValue, setSearchValue] = useState('');

  const [selectedPlayerId, setSelectedPlayerId] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  const [activeView, setActiveView] = useState('player'); // 'player' | 'compare'

  // Load players
  const loadPlayers = useCallback(async () => {
    const [sortBy, sortOrder] = currentSort.split('-');
    const data = await fetchPlayers({
      page: currentPage,
      limit: 50,
      search: searchValue,
      positionGroup: currentFilter,
      sortBy,
      sortOrder
    });

    if (data) {
      setPlayers(data.players);
      setTotalPlayers(data.total);
      setTotalPages(data.totalPages);
    }
  }, [currentPage, currentFilter, currentSort, searchValue, fetchPlayers]);

  useEffect(() => {
    loadPlayers();
  }, [loadPlayers]);

  // Handle player selection
  const handleSelectPlayer = async (playerId) => {
    setSelectedPlayerId(playerId);
    const player = await fetchPlayer(playerId);
    if (player) {
      setSelectedPlayer(player);
    }
  };

  // Handle filter change
  const handleFilterChange = (filter) => {
    setCurrentFilter(filter);
    setCurrentPage(1);
  };

  // Handle sort change
  const handleSortChange = (sort) => {
    setCurrentSort(sort);
    setCurrentPage(1);
  };

  // Handle search submit
  const handleSearchSubmit = () => {
    setCurrentPage(1);
    loadPlayers();
  };

  // Handle page change
  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="app">
      <Header
        currentFilter={currentFilter}
        onFilterChange={handleFilterChange}
        currentSort={currentSort}
        onSortChange={handleSortChange}
        searchValue={searchValue}
        onSearchChange={setSearchValue}
        onSearchSubmit={handleSearchSubmit}
        totalPlayers={totalPlayers}
      />

      <main className="container">
        <PlayerTable
          players={players}
          loading={loading}
          currentPage={currentPage}
          totalPages={totalPages}
          selectedPlayerId={selectedPlayerId}
          onSelectPlayer={handleSelectPlayer}
          onPageChange={handlePageChange}
        />

        <section className="detail">
          {/* View Tabs */}
          <div className="view-tabs">
            <button
              className={`view-tab ${activeView === 'player' ? 'active' : ''}`}
              onClick={() => setActiveView('player')}
            >
              Player
            </button>
            <button
              className={`view-tab ${activeView === 'compare' ? 'active' : ''}`}
              onClick={() => setActiveView('compare')}
            >
              Compare
            </button>
          </div>

          {/* View Panels */}
          {activeView === 'player' ? (
            <PlayerDetail player={selectedPlayer} />
          ) : (
            <CompareView />
          )}
        </section>
      </main>
    </div>
  );
}
