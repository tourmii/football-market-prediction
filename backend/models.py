from pydantic import BaseModel
from typing import Optional


class PlayerSummary(BaseModel):
    playerId: int
    name: str
    teamName: str
    position: str
    positionGroup: str
    age: Optional[float] = None
    marketValue: Optional[float] = None
    marketValueCurrency: str = "EUR"
    rating: Optional[float] = None
    appearances: Optional[int] = None


class RadarData(BaseModel):
    attacking: float
    passing: float
    dribbling: float
    defending: float
    physical: float
    rating: float


class AttackingStats(BaseModel):
    Goals: int = 0
    xG: float = 0
    Shots: int = 0
    OnTarget: int = 0


class PassingStats(BaseModel):
    Assists: int = 0
    KeyPasses: int = 0
    PassPercent: float = 0
    ChancesCreated: int = 0


class DribblingStats(BaseModel):
    Dribbles: int = 0
    DribblePercent: float = 0
    Touches: int = 0


class DefendingStats(BaseModel):
    Tackles: int = 0
    Interceptions: int = 0
    Clearances: int = 0
    Blocks: int = 0


class PhysicalStats(BaseModel):
    GroundDuels: int = 0
    AerialDuels: int = 0
    DuelsWonPercent: float = 0


class DetailedStats(BaseModel):
    attacking: dict = {}
    passing: dict = {}
    dribbling: dict = {}
    defending: dict = {}
    physical: dict = {}


class PlayerDetail(BaseModel):
    playerId: int
    name: str
    teamName: str
    position: str
    positionGroup: str
    firstSidePosition: Optional[str] = None
    secondSidePosition: Optional[str] = None
    
    # Demographics
    age: Optional[float] = None
    height: Optional[float] = None
    preferredFoot: Optional[str] = None
    dateOfBirth: Optional[str] = None
    nationalityId: Optional[int] = None
    
    # Contract & Market
    contractUntil: Optional[str] = None
    marketValueCurrent: Optional[float] = None
    marketValuePrevious: Optional[float] = None
    marketValueCurrency: str = "EUR"
    marketValueTrend: str = "stable"  # up, down, stable
    
    # Playing Time
    appearances: Optional[int] = None
    minutesPlayed: Optional[float] = None
    matchesStarted: Optional[int] = None
    
    # Rating
    rating: Optional[float] = None
    
    # Attacking
    goals: Optional[float] = None
    expectedGoals: Optional[float] = None
    assists: Optional[float] = None
    
    # Additional key stats
    totalPasses: Optional[float] = None
    accuratePassesPercentage: Optional[float] = None
    successfulDribbles: Optional[float] = None
    tackles: Optional[float] = None
    interceptions: Optional[float] = None
    keyPasses: Optional[float] = None
    bigChancesCreated: Optional[float] = None
    clearances: Optional[float] = None
    aerialDuelsWon: Optional[float] = None
    groundDuelsWon: Optional[float] = None
    totalShots: Optional[float] = None
    shotsOnTarget: Optional[float] = None
    
    # Radar data
    radar: RadarData
    
    # Detailed stats by category
    detailedStats: DetailedStats


class PaginatedPlayers(BaseModel):
    players: list[PlayerSummary]
    total: int
    page: int
    limit: int
    totalPages: int

