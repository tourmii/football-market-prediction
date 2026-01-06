import os
import pandas as pd

data_dir = os.getcwd()
bio_data_path = f'{data_dir}/transfermarkt/data_transfermarktver4.csv'
bio_data = pd.read_csv(bio_data_path)

stats_data_path = f'{data_dir}/sofascore/all_player_stats_merged.csv'
stats_data = pd.read_csv(stats_data_path)
stats_data.head()

# Correcting and Standardizing Data Types

bio_data['contractUntil'] = pd.to_datetime(bio_data['contractUntil'], errors='coerce', utc=True)
bio_data['contractUntil'] = bio_data['contractUntil'].dt.tz_localize(None)

# Date time conversion
bio_data['date_of_birth'] = pd.to_datetime(bio_data['date_of_birth'], errors='coerce')
stats_data['date_of_birth'] = pd.to_datetime(stats_data['date_of_birth'], errors='coerce')

# Check object data types in stats_data
for col, dtype in stats_data.dtypes.items():
    if dtype == 'object':
        print(f"{col}: {dtype} (example value: {stats_data[col].dropna().iloc[0]})")

# Handle Duplicates and Missing Values
# Check duplicates
print('Duplicates in stats_data:', stats_data.duplicated().sum())
print('Duplicates in bio_data:', bio_data.duplicated().sum())

# Check missing values
for col, missing_count in bio_data.isna().sum().sort_values(ascending=False).items():
    if missing_count > 0:
        print(f"{col}: {missing_count} missing values")

# Drop nationality column
bio_data.drop(columns=['nationality'], inplace=True)
# Fill missing side positions values with 'None'
bio_data[['secondSidePosition', 'secondSidePositionId', 'firstSidePosition', 'firstSidePositionId']] = bio_data[['secondSidePosition', 'secondSidePositionId', 'firstSidePosition', 'firstSidePositionId']].fillna('None')

# Remove all players with no date_of_birth and position (since they are few)
bio_data.drop(index=bio_data[bio_data['date_of_birth'].isna()].index, inplace=True)
bio_data.drop(index=bio_data[bio_data['position'].isna()].index, inplace=True)
# Remove all players with no market_value (important column)
bio_data.drop(index=bio_data[bio_data['MarketValueCurrent'].isna()].index, inplace=True)
bio_data.drop(index=bio_data[bio_data['MarketValuePrevious'].isna()].index, inplace=True)

# Assume that players without contractUntil are free agents, fillna with a today date
bio_data['contractUntil'] = bio_data['contractUntil'].fillna(pd.to_datetime('today'))

# Fill missing preferredFoot with most common value
most_common_foot = bio_data['preferredFoot'].mode()[0]
most_common_foot_id = bio_data['preferredFootId'].mode()[0]
bio_data.loc[bio_data['preferredFoot'].isna(), 'preferredFoot'] = most_common_foot
bio_data.loc[bio_data['preferredFootId']==0, 'preferredFootId'] = most_common_foot_id

# Fill height with median values corresponding to their positions
position_groups = bio_data.groupby('position')
for position, group in position_groups:
    median_height = group['height'].median()
    bio_data.loc[(bio_data['position'] == position) & (bio_data['height'].isna()), 'height'] = median_height

# Check missing values again
missing_col = []
for col, missing_count in bio_data.isna().sum().sort_values(ascending=False).items():
    if missing_count > 0:
        print(f"{col}: {missing_count} missing values")
        missing_col.append(col)
if not missing_col:
    print("No missing values remain in bio_data.")

drop_cols = []
for col, missing_count in stats_data.isna().sum().sort_values(ascending=False).items():
    if missing_count > 0:
        print(f"{col}: {missing_count} missing values")
        if missing_count == 5535:
            drop_cols.append(col)

# Drop columns with too many missing values
stats_data.drop(columns=drop_cols, inplace=True)

# Remove rows with missing important values
stats_data.drop(index=stats_data[stats_data['cleanSheet'].isna()].index, inplace=True)

# Remove rows with missing date_of_birth (since they are few)
stats_data.drop(index=stats_data[stats_data['date_of_birth'].isna()].index, inplace=True)

# Players with no expected goals/assists get 0 since they might be defenders or goalkeepers
stats_data[['expectedGoals', 'expectedAssists']] = stats_data[['expectedGoals', 'expectedAssists']].fillna(0)

# Players without goalsPrevented might not be goalkeepers, fillna with 0
stats_data[['goalsPrevented']] = stats_data[['goalsPrevented']].fillna(0)

# Drop outfielderBlocks since this statistic may only be recorded for some leagues
stats_data.drop(columns=['outfielderBlocks'], inplace=True)

# Check missing values again
missing_col = []
for col, missing_count in stats_data.isna().sum().sort_values(ascending=False).items():
    if missing_count > 0:
        print(f"{col}: {missing_count} missing values")
        missing_col.append(col)
if len(missing_col) == 0:
    print('No missing values in stats_data')

# Merge Datasets
# Find similar columns in two datasets
common_cols = set(bio_data.columns).intersection(set(stats_data.columns))
print('Common columns in both datasets:', common_cols)

# Merge on name, teamName, and date_of_birth
merged_data = pd.merge(bio_data, stats_data, left_on=['name', 'teamName', 'date_of_birth'], right_on=['player_name', 'teamName', 'date_of_birth'], how='inner')

# Save cleaned data
merged_data.to_csv('cleaned_player_data.csv', index=False)