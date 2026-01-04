from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from models import PlayerSummary, PlayerDetail, RadarData, PaginatedPlayers
from data_service import get_data_service

app = FastAPI(
    title="Football Player Dashboard API",
    description="API for the Football Market Prediction demo dashboard",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """API health check endpoint."""
    return {"status": "ok", "message": "Football Player Dashboard API is running"}


@app.get("/api/players", response_model=PaginatedPlayers)
def get_players(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by player name"),
    positionGroup: Optional[str] = Query(None, description="Filter by position group (GK, DEF, MID, ATT)"),
    team: Optional[str] = Query(None, description="Filter by team name"),
    sortBy: str = Query("marketValue", description="Sort field"),
    sortOrder: str = Query("desc", description="Sort order (asc/desc)")
):
    """Get paginated list of players with optional filters."""
    service = get_data_service()
    players, total = service.get_players(
        page=page,
        limit=limit,
        search=search,
        position_group=positionGroup,
        team=team,
        sort_by=sortBy,
        sort_order=sortOrder
    )
    
    total_pages = (total + limit - 1) // limit
    
    return {
        "players": players,
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": total_pages
    }


@app.get("/api/players/{player_id}", response_model=PlayerDetail)
def get_player(player_id: int):
    """Get detailed player information by ID."""
    service = get_data_service()
    player = service.get_player_by_id(player_id)
    
    if player is None:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    
    return player


@app.get("/api/players/{player_id}/radar", response_model=RadarData)
def get_player_radar(player_id: int):
    """Get radar chart data for a player."""
    service = get_data_service()
    radar = service.get_radar_data(player_id)
    
    if radar is None:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    
    return radar


@app.get("/api/positions")
def get_positions():
    """Get available position groups for filtering."""
    service = get_data_service()
    return service.get_positions()


@app.get("/api/teams")
def get_teams():
    """Get all available team names."""
    service = get_data_service()
    return service.get_teams()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
