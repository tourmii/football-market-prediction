from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import lightgbm as lgb
import pandas as pd

data_path = 'data/split/'
X_train =  pd.read_csv(data_path+'X_train.csv')  # Load or define your training features
y_train =  pd.read_csv(data_path+'y_train.csv')  # Load or define your training target
X_valid =  pd.read_csv(data_path+'X_valid.csv')  # Load or define your validation features
y_valid =  pd.read_csv(data_path+'y_valid.csv')  # Load or define your validation target


#------------------------------------------------------------------------------
#Setting up models with best hyperparameters found during tuning
#------------------------------------------------------------------------------
best_xgb_param = {'subsample': 1.0, 
                  'reg_lambda': 1.0, 
                  'reg_alpha': 0.1, 
                  'n_estimators': 10000, 
                  'min_child_weight': 3, 
                  'max_depth': 3, 
                  'learning_rate': 0.01, 
                  'colsample_bytree': 0.8}
xgb_base = XGBRegressor(**best_xgb_param, random_state=42, n_jobs=-1, verbosity=0, early_stopping_rounds=50)
xgb_base.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_valid, y_valid)], verbose=False)

callbacks = [
    lgb.early_stopping(stopping_rounds=50, verbose=False),
    lgb.log_evaluation(period=0)
]
best_lgbm_param = {'subsample': 1.0, 
     'reg_lambda': 0, 
     'reg_alpha': 0.1, 
     'num_leaves': 31, 
     'n_estimators': 500, 
     'min_child_samples': 20, 
     'max_depth': 3, 
     'learning_rate': 0.01, 
     'colsample_bytree': 0.8}
lgbm_base = LGBMRegressor(**best_lgbm_param, random_state=42, n_jobs=-1, verbosity=-1)
lgbm_base.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_valid, y_valid)],
    eval_metric="rmse",
    callbacks=callbacks)

best_catboost_param = {'random_strength': 0, 
 'learning_rate': 0.05, 
 'l2_leaf_reg': 7, 
 'iterations': 200, 
 'depth': 4, 
 'border_count': 128, 
 'bagging_temperature': 1}

catboost_base = CatBoostRegressor(task_type="GPU",devices='0',**best_catboost_param, random_state=42,verbose=0,thread_count=-1,od_type='Iter',od_wait=50)
catboost_base.fit(X_train, y_train, eval_set=(X_valid, y_valid), use_best_model=True)

#Save trained models
import joblib
model_path = 'models/'
joblib.dump(xgb_base, model_path+'xgb_base_model.pkl')
joblib.dump(lgbm_base, model_path+'lgbm_base_model.pkl')
joblib.dump(catboost_base, model_path+'catboost_base_model.pkl')