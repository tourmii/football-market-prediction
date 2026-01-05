from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd

def eval_new(delta_pred_org, df, model_name):

    scaler = StandardScaler()
    pred = delta_pred_org.flatten()
    
    """Evaluate model performance with multiple metrics."""
    # Metrics on log-scale
    df['PredictedDelta'] = pred
    df['Predicted'] = df['MarketValuePrevious'] + df['PredictedDelta']
    scaler.fit(df['MarketValueCurrent'].values.reshape(-1, 1))
    
    y_std = scaler.transform(df['MarketValuePrevious'].values.reshape(-1, 1))
    y_pred_std = scaler.transform(df['Predicted'].values.reshape(-1, 1))

    
    rmse_log = np.sqrt(mean_squared_error(y_std, y_pred_std))
    mae_log = mean_absolute_error(y_std, y_pred_std)
    r2_log = r2_score(y_std, y_pred_std)

    print(df[df['MarketValueCurrent'] == 0])
    y_org = df['MarketValueCurrent'].copy()
    y_pred_org = df['Predicted'].copy()

    y_org.replace(0, 1, inplace=True)
    # y_org.fillna(y_org.mean(), inplace=True)
    
    # Metrics on original scale
    rmse = np.sqrt(mean_squared_error(y_org, y_pred_org))
    mae = mean_absolute_error(y_org, y_pred_org)
    r2 = r2_score(y_org, y_pred_org)
    
    print(f"\n{'='*50}")
    print(f"{model_name} Evaluation Results")
    print(f"{'='*50}")
    print(f"\\Normalized Metrics:")
    print(f"  RMSE: {rmse_log:.4f}")
    print(f"  MAE: {mae_log:.4f}")
    print(f"  R²: {r2_log:.4f}")
    print(f"\nOriginal Scale Metrics:")
    print(f"  RMSE: €{rmse:,.0f}")
    print(f"  MAE: €{mae:,.0f}")
    print(f"  R²: {r2:.4f}")
    
    return {
        'model': model_name,
        'rmse_log': rmse_log,
        'mae_log': mae_log,
        'r2_log': r2_log,
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }

model_path = 'models/'
import joblib
xgb_model = joblib.load(model_path+'xgb_base_model.pkl')
lgbm_model = joblib.load(model_path+'lgbm_base_model.pkl')
catboost_model = joblib.load(model_path+'catboost_base_model.pkl')
data_path = 'data/'
X_test =  pd.read_csv(data_path+'X_test.csv')  # Load or define your test features
y_test =  pd.read_csv(data_path+'y_test.csv')  # Load or define your test target
values_df_test =  pd.read_csv(data_path+'values_df_test.csv')  # Load or define your test target
# Make predictions
delta_pred_xgb = xgb_model.predict(X_test)
delta_pred_lgbm = lgbm_model.predict(X_test)
delta_pred_catboost = catboost_model.predict(X_test)
# Evaluate models
results_xgb = eval_new(delta_pred_xgb, values_df_test.copy(), 'XGBoost Regressor')
results_lgbm = eval_new(delta_pred_lgbm, values_df_test.copy(), 'LightGBM Regressor')
results_catboost = eval_new(delta_pred_catboost, values_df_test.copy(), 'CatBoost Regressor')