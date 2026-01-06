from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
import joblib

data_path = 'data/split/'
X_train =  pd.read_csv(data_path+'X_train.csv')
y_train =  pd.read_csv(data_path+'y_train.csv')  
X_valid =  pd.read_csv(data_path+'X_valid.csv')  
y_valid =  pd.read_csv(data_path+'y_valid.csv')  

print("Training XGBoost with Hyperparameter Tuning...")

xgb_param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'min_child_weight': [1, 3, 5],
    'reg_alpha': [0, 0.1, 0.5],
    'reg_lambda': [0, 0.1, 1.0]
}

xgb_base = XGBRegressor(random_state=42, n_jobs=-1, verbosity=0)

xgb_random_search = RandomizedSearchCV(
    xgb_base,
    param_distributions=xgb_param_grid,
    n_iter=50,
    cv=5,
    scoring='neg_root_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

xgb_random_search.fit(X_train, y_train)

print(f"\nBest XGBoost Parameters: {xgb_random_search.best_params_}")
print(f"Best CV Score (RMSE): {-xgb_random_search.best_score_:.4f}")

print("Training LightGBM with Hyperparameter Tuning...")

lgbm_param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'num_leaves': [15, 31, 63, 127],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'min_child_samples': [5, 10, 20],
    'reg_alpha': [0, 0.1, 0.5],
    'reg_lambda': [0, 0.1, 1.0]
}

lgbm_base = LGBMRegressor(random_state=42, n_jobs=-1, verbosity=-1)

lgbm_random_search = RandomizedSearchCV(
    lgbm_base,
    param_distributions=lgbm_param_grid,
    n_iter=50, 
    cv=5,
    scoring='neg_root_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

lgbm_random_search.fit(X_train, y_train)

print(f"\nBest LightGBM Parameters: {lgbm_random_search.best_params_}")
print(f"Best CV Score (RMSE): {-lgbm_random_search.best_score_:.4f}")


print("Training CatBoost with Hyperparameter Tuning...")

catboost_param_grid = {
    'iterations': [100, 200, 300, 500],
    'depth': [4, 6, 8, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'l2_leaf_reg': [1, 3, 5, 7],
    'bagging_temperature': [0, 0.5, 1],
    'random_strength': [0, 0.5, 1],
    'border_count': [32, 64, 128]
}

catboost_base = CatBoostRegressor(
    random_state=42,
    verbose=0,
    thread_count=-1,
)

catboost_random_search = RandomizedSearchCV(
    catboost_base,
    param_distributions=catboost_param_grid,
    n_iter=50,
    cv=5,
    scoring='neg_root_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

catboost_random_search.fit(X_train, y_train)

print(f"\nBest CatBoost Parameters: {catboost_random_search.best_params_}")
print(f"Best CV Score (RMSE): {-catboost_random_search.best_score_:.4f}")

xgb_best = xgb_random_search.best_estimator_
lgbm_best = lgbm_random_search.best_estimator_
catboost_best = catboost_random_search.best_estimator_

#Save trained models
model_path = 'models/checkpoints/'
joblib.dump(xgb_best, model_path+'xgb_model.pkl')
joblib.dump(lgbm_best, model_path+'lgbm_model.pkl')
joblib.dump(catboost_best, model_path+'catboost_model.pkl')