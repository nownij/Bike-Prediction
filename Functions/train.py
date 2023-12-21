# train.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import streamlit as st

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}
def concat_dfs(df_list):
    df = pd.concat(df_list, ignore_index=True)
    res_df = df.groupby('HHMM').agg({'Use': 'mean', 'temp': 'mean'}).round(2).reset_index()

    return res_df
def train_and_predict(df):
    X = df[['HHMM', 'temp']]
    y = df['Use']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3)
    grid_search.fit(X_train, y_train)

    best_rf_model = grid_search.best_estimator_

    feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': best_rf_model.feature_importances_})
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    # print(feature_importances)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    predictions = rf_model.predict(X)

    #print(f'Mean Square Error >> {mse.round(6)}')
    #print(f'R-squared Score   >> {r2.round(6)}')

    df['prd_Use'] = predictions.round(2)
    pred_df = df[['HHMM', 'Use', 'prd_Use', 'temp']]

    st.write(feature_importances)
    st.write(f"Mean Squeare Error : {mse.round(6)}")
    st.write(f"R-Squared Score    : {r2.round(6)}")

    return pred_df
