from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd

def eval(delta_pred_org, df, model_name):
    pred = delta_pred_org.flatten()
    
    prev_log = np.log1p(df['MarketValuePrevious'])
    current_pred_log = prev_log + pred
    
    df['Predicted'] = np.expm1(current_pred_log)
    
    #Metrics on Log Scale
    actual_log = np.log1p(df['MarketValueCurrent'])
    rmse_log = np.sqrt(mean_squared_error(actual_log, current_pred_log))
    mae_log = mean_absolute_error(actual_log, current_pred_log)
    r2_log = r2_score(actual_log, current_pred_log)
    
    y_org = df['MarketValueCurrent'].copy()
    y_pred_org = df['Predicted'].copy()

    y_org.replace(0, 1, inplace=True)
    
    # Metrics on original scale
    rmse = np.sqrt(mean_squared_error(y_org, y_pred_org))
    mae = mean_absolute_error(y_org, y_pred_org)
    r2 = r2_score(y_org, y_pred_org)
    
    print(f"\n{'='*50}")
    print(f"{model_name} Evaluation Results")
    print(f"{'='*50}")
    print(f"  Log RMSE: {rmse_log:.4f}")
    print(f"  Log MAE:  {mae_log:.4f}")
    print(f"  Log R²:   {r2_log:.4f}")
    print(f"{'-'*50}")
    print(f"  RMSE: €{rmse:,.0f}")
    print(f"  MAE: €{mae:,.0f}")
    print(f"  R²: {r2:.4f}")
    
    return {
        'model': model_name,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'rmse_log': rmse_log,
        'mae_log': mae_log,
        'r2_log': r2_log
    }

model_path = 'models/checkpoints/'
import joblib
xgb_model = joblib.load(model_path+'xgb_model.pkl')
lgbm_model = joblib.load(model_path+'lgbm_model.pkl')
catboost_model = joblib.load(model_path+'catboost_model.pkl')
data_path = 'data/split/'
X_test =  pd.read_csv(data_path+'X_test.csv')  # Load or define your test features
y_test =  pd.read_csv(data_path+'y_test.csv')  # Load or define your test target
values_df_test =  pd.read_csv(data_path+'values_df_test.csv')  # Load or define your test target
# Make predictions
delta_pred_xgb = xgb_model.predict(X_test)
delta_pred_lgbm = lgbm_model.predict(X_test)
delta_pred_catboost = catboost_model.predict(X_test)
# Evaluate models
results_xgb = eval(delta_pred_xgb, values_df_test.copy(), 'XGBoost Regressor')
results_lgbm = eval(delta_pred_lgbm, values_df_test.copy(), 'LightGBM Regressor')
results_catboost = eval(delta_pred_catboost, values_df_test.copy(), 'CatBoost Regressor')