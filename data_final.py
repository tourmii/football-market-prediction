import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# FINAL DATA PREPARATION BEFORE MODEL TRAINING
# ------------------------------------------------------------------------------

data_path = '/Users/khangdoan/Documents/GitHub/football-market-prediction/data/cleaned_player_data.csv'
df = pd.read_csv(data_path)
data = df.copy()

# DROP UNNECESSARY COLUMNS
cols_to_drop = [
    'playerId', 'playerID', 'player_name', 'name', 'date_of_birth',
    'MarketValueCurrency', 'id', 'type',
    'preferredFoot', 'teamName',
    'position', 'firstSidePosition', 'secondSidePosition', 'contractUntil'
]

data = data.drop(columns=cols_to_drop, errors='ignore')

label_encoders = {}

categorical_cols = data.select_dtypes(include=['object']).columns.tolist()

for col in categorical_cols:
    # Fill missing values with 'Unknown'
    data[col] = data[col].fillna('Unknown')
    
    # Label encode
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

# Create new features

# 1. Goals per 90 minutes
data['goals_per_90'] = np.where(data['minutesPlayed'] > 0, 
                                 (data['goals'] / data['minutesPlayed']) * 90, 0)

# 2. Assists per 90 minutes
data['assists_per_90'] = np.where(data['minutesPlayed'] > 0, 
                                   (data['assists'] / data['minutesPlayed']) * 90, 0)

# 3. Goal involvement (goals + assists)
data['goal_involvement'] = data['goals'] + data['assists']

# 4. Goal involvement per 90
data['goal_involvement_per_90'] = np.where(data['minutesPlayed'] > 0,
                                            (data['goal_involvement'] / data['minutesPlayed']) * 90, 0)

# 5. Shots on target percentage
data['shots_on_target_pct'] = np.where(data['totalShots'] > 0,
                                        (data['shotsOnTarget'] / data['totalShots']) * 100, 0)

# 6. Big chances conversion rate
data['big_chance_conversion'] = np.where((data['bigChancesMissed'] + data['goals']) > 0,
                                          data['goals'] / (data['bigChancesMissed'] + data['goals']) * 100, 0)

# 7. Duels won per 90
data['duels_won_per_90'] = np.where(data['minutesPlayed'] > 0,
                                     (data['totalDuelsWon'] / data['minutesPlayed']) * 90, 0)

# 8. Touches per 90
data['touches_per_90'] = np.where(data['minutesPlayed'] > 0,
                                   (data['touches'] / data['minutesPlayed']) * 90, 0)

# 9. Key passes per 90
data['key_passes_per_90'] = np.where(data['minutesPlayed'] > 0,
                                      (data['keyPasses'] / data['minutesPlayed']) * 90, 0)

# 10. Successful dribbles per 90
data['dribbles_per_90'] = np.where(data['minutesPlayed'] > 0,
                                    (data['successfulDribbles'] / data['minutesPlayed']) * 90, 0)

# 11. Interceptions per 90
data['interceptions_per_90'] = np.where(data['minutesPlayed'] > 0,
                                         (data['interceptions'] / data['minutesPlayed']) * 90, 0)

# 12. Tackles per 90
data['tackles_per_90'] = np.where(data['minutesPlayed'] > 0,
                                   (data['tackles'] / data['minutesPlayed']) * 90, 0)

# 13. Clearances per 90
data['clearances_per_90'] = np.where(data['minutesPlayed'] > 0,
                                      (data['clearances'] / data['minutesPlayed']) * 90, 0)

# 14. Age squared (to capture non-linear age effects)
data['age_squared'] = data['age'] ** 2

# 15. Peak age indicator (typically 25-29 for football players)
data['is_peak_age'] = ((data['age'] >= 25) & (data['age'] <= 29)).astype(int)

# 16. Young talent indicator (under 23)
data['is_young_talent'] = (data['age'] < 23).astype(int)

# 17. Rating difference from average
data['rating_diff'] = data['rating'] - data['rating'].mean()

# 18. Minutes per appearance
data['minutes_per_appearance'] = np.where(data['appearances'] > 0,
                                        data['minutesPlayed'] / data['appearances'], 0)

# 19. Passes per 90
data['passes_per_90'] = np.where(data['minutesPlayed'] > 0,
                                  (data['totalPasses'] / data['minutesPlayed']) * 90, 0)

data = data.replace([np.inf, -np.inf], np.nan)
data = data.fillna(0)

# TARGET VARIABLE
data['delta'] = data['MarketValueCurrent'] - data['MarketValuePrevious']

TARGET = 'delta'

values_df = data[['MarketValuePrevious', 'MarketValueCurrent']].copy()
data.drop(columns=['MarketValuePrevious', 'MarketValueCurrent'], inplace=True)

feature_cols = [col for col in data.columns if col not in [TARGET]]
X = data[feature_cols]
y = data[TARGET]

#DATA SPLITTING
X_train_full, X_test, y_train_full, y_test, values_df_train, values_df_test = train_test_split(
    X, y, values_df, test_size=0.20, random_state=42
)

X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=42 
)

#SAVE FINAL DATASETS
final_data_path = 'data/split/'
X_train.to_csv(final_data_path+'X_train.csv', index=False)
y_train.to_csv(final_data_path+'y_train.csv', index=False)
X_valid.to_csv(final_data_path+'X_valid.csv', index=False)
y_valid.to_csv(final_data_path+'y_valid.csv', index=False)
X_test.to_csv(final_data_path+'X_test.csv', index=False)
y_test.to_csv(final_data_path+'y_test.csv', index=False)
values_df_train.to_csv(final_data_path+'values_df_train.csv', index=False)
values_df_test.to_csv(final_data_path+'values_df_test.csv', index=False)