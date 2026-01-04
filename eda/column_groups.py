COLUMN_GROUPS = {
    "identifiers_metadata": [
        'playerId', 'id',
        'name', 'player_name',
        'teamId', 'teamName',
        'nationalityId',
        'type'
    ],
    
    "contract_market": [
        'contractUntil',
        'MarketValueCurrent',
        'MarketValuePrevious',
        'MarketValueCurrency'
    ],
    
    "demographics_physical": [
        'date_of_birth',
        'age',
        'height',
        'preferredFoot', 'preferredFootId'
    ],
    
    "position_role": [
        'position', 'positionId',
        'firstSidePosition', 'firstSidePositionId',
        'secondSidePosition', 'secondSidePositionId'
    ],
    
    "playing_time": [
        'minutesPlayed',
        'appearances',
        'matchesStarted'
    ],
    
    "rating_performance": [
        'rating',
        'totalRating',
        'countRating',
        'scoringFrequency',
        'totwAppearances'
    ],
    
    "attacking_output": [
        'goals',
        'expectedGoals',
        'totalShots',
        'shotsOnTarget',
        'shotsOffTarget',
        'goalConversionPercentage',
        'goalsFromInsideTheBox',
        'goalsFromOutsideTheBox',
        'shotsFromInsideTheBox',
        'shotsFromOutsideTheBox',
        'headedGoals',
        'leftFootGoals',
        'rightFootGoals',
        'hitWoodwork',
        'bigChancesMissed'  
    ],
    
    "chance_creation": [
        'assists',
        'expectedAssists',
        'goalsAssistsSum',
        'keyPasses',
        'bigChancesCreated',
        'passToAssist',
        'totalAttemptAssist'
    ],
    
    "passing_buildup": [
        'accuratePasses',
        'inaccuratePasses',
        'totalPasses',
        'accuratePassesPercentage',
        'accurateOwnHalfPasses',
        'accurateOppositionHalfPasses',
        'accurateFinalThirdPasses',
        'totalOwnHalfPasses',
        'totalOppositionHalfPasses',
        'accurateLongBalls',
        'accurateLongBallsPercentage',
        'totalLongBalls',
        'totalChippedPasses',
        'accurateChippedPasses',
        'accurateCrosses',        
        'accurateCrossesPercentage',
        'totalCross'              
    ],
    
    "dribbling_carrying": [
        'successfulDribbles',
        'successfulDribblesPercentage',
        'dispossessed',
        'possessionLost',
        'possessionWonAttThird',
        'touches'
    ],
    
    "defensive_actions": [
        'tackles',
        'tacklesWon',
        'tacklesWonPercentage',
        'interceptions',
        'clearances',
        'blockedShots',
        'ballRecovery'
    ],
    
    "duels_physical": [
        'groundDuelsWon',
        'groundDuelsWonPercentage',
        'aerialDuelsWon',
        'aerialDuelsWonPercentage',
        'totalDuelsWon',
        'totalDuelsWonPercentage',
        'duelLost',
        'aerialLost',
        'totalContest'
    ],
    
    "discipline_fouls": [
        'yellowCards',
        'redCards',
        'directRedCards',
        'yellowRedCards',
        'fouls',
        'wasFouled',
        'offsides',
        'ownGoals'
    ],
    
    "errors_mistakes": [
        'errorLeadToGoal',
        'errorLeadToShot',
        'dribbledPast'
    ],
    
    "set_pieces_penalties": [
        'penaltiesTaken',
        'penaltyGoals',
        'penaltyWon',
        'penaltyConceded',
        'penaltyConversion',
        'setPieceConversion',
        'attemptPenaltyMiss',
        'attemptPenaltyPost',
        'attemptPenaltyTarget',
        'freeKickGoal',
        'shotFromSetPiece'
    ],
    
    "goalkeeping": [
        'saves',
        'savesCaught',
        'savesParried',
        'goalsPrevented',
        'cleanSheet',
        'penaltyFaced',
        'penaltySave',
        'savedShotsFromInsideTheBox',
        'savedShotsFromOutsideTheBox',
        'goalsConceded',
        'goalsConcededInsideTheBox',
        'goalsConcededOutsideTheBox',
        'punches',
        'runsOut',
        'successfulRunsOut',
        'highClaims',
        'crossesNotClaimed',
        'goalKicks'
    ]
}

GROUP_DESCRIPTIONS = {
    "identifiers_metadata": "Used for joins, keys, filtering. Never feed directly into models.",
    "contract_market": "Economic / transfer-related signals.",
    "demographics_physical": "Mostly static, slow-changing features.",
    "position_role": "Defines tactical role and positional context.",
    "playing_time": "Exposure variables. Crucial for normalization.",
    "rating_performance": "High-level evaluation metrics.",
    "attacking_output": "Direct goal threat.",
    "chance_creation": "How the player creates value for others.",
    "passing_buildup": "Ball circulation and progression.",
    "dribbling_carrying": "1v1 and ball progression under pressure.",
    "defensive_actions": "Out-of-possession contribution.",
    "duels_physical": "Physical dominance metrics.",
    "discipline_fouls": "Risk and discipline profile.",
    "errors_mistakes": "High-impact negative events.",
    "set_pieces_penalties": "Special situations (outfield).",
    "goalkeeping": "GK-only metrics. Should be isolated or filtered by position."
}

EXCLUDE_FROM_MODELS = COLUMN_GROUPS["identifiers_metadata"] + COLUMN_GROUPS["contract_market"]

OUTFIELD_FEATURES = (
    COLUMN_GROUPS["attacking_output"] +
    COLUMN_GROUPS["chance_creation"] +
    COLUMN_GROUPS["passing_buildup"] +
    COLUMN_GROUPS["dribbling_carrying"] +
    COLUMN_GROUPS["defensive_actions"] +
    COLUMN_GROUPS["duels_physical"] +
    COLUMN_GROUPS["discipline_fouls"] +
    COLUMN_GROUPS["errors_mistakes"] +
    COLUMN_GROUPS["set_pieces_penalties"]
)

GK_FEATURES = COLUMN_GROUPS["goalkeeping"]

NORMALIZATION_COLS = COLUMN_GROUPS["playing_time"]


def get_columns_by_group(group_name: str) -> list:
    return COLUMN_GROUPS.get(group_name, [])


def get_all_columns() -> list:
    return [col for cols in COLUMN_GROUPS.values() for col in cols]


def get_group_for_column(column: str) -> str | None:
    for group_name, columns in COLUMN_GROUPS.items():
        if column in columns:
            return group_name
    return None


def validate_columns(df_columns: list) -> dict:
    all_defined = set(get_all_columns())
    df_cols = set(df_columns)
    
    return {
        'matched': list(all_defined & df_cols),
        'unmatched': list(df_cols - all_defined),  
        'missing': list(all_defined - df_cols)     
    }
