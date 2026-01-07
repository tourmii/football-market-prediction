import { useState, useEffect, useCallback } from 'react';

const API_BASE = 'http://localhost:8000/api';

export function useApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchPlayers = useCallback(async ({
        page = 1,
        limit = 50,
        search = '',
        positionGroup = 'ALL',
        sortBy = 'marketValue',
        sortOrder = 'desc'
    } = {}) => {
        setLoading(true);
        setError(null);

        try {
            const params = new URLSearchParams({ page, limit, sortBy, sortOrder });
            if (positionGroup !== 'ALL') params.append('positionGroup', positionGroup);
            if (search) params.append('search', search);

            const res = await fetch(`${API_BASE}/players?${params}`);
            if (!res.ok) throw new Error('Failed to fetch players');
            const data = await res.json();
            return data;
        } catch (err) {
            setError(err.message);
            return null;
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchPlayer = useCallback(async (playerId) => {
        setLoading(true);
        setError(null);

        try {
            const res = await fetch(`${API_BASE}/players/${playerId}`);
            if (!res.ok) throw new Error('Failed to fetch player');
            const data = await res.json();
            return data;
        } catch (err) {
            setError(err.message);
            return null;
        } finally {
            setLoading(false);
        }
    }, []);

    const searchPlayers = useCallback(async (query, limit = 10) => {
        if (!query || query.length < 2) return [];

        try {
            const res = await fetch(`${API_BASE}/players?search=${encodeURIComponent(query)}&limit=${limit}`);
            if (!res.ok) throw new Error('Search failed');
            const data = await res.json();
            return data.players || [];
        } catch (err) {
            console.error(err);
            return [];
        }
    }, []);

    return { loading, error, fetchPlayers, fetchPlayer, searchPlayers };
}
