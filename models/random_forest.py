import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def add_lags(lags, X, y):
    new_X = X.copy()
    if lags < 1:
        return new_X
    for lag in range(1, lags + 1):
        new_lag = "civic_sales_L" + str(lag)
        new_X[new_lag] = y.shift(lag)
    return new_X

if __name__ == "__main__":
    df = pd.read_csv("data/combined_table.csv").set_index("date")
    y = df["civic_sales"]
    X = df.drop(columns = ["civic_sales"], axis="columns")
    
    # Random split
    best_train_mse = None
    best_test_mse = None
    best_num_lags = None
    best_model = None
    
    for lags in range(0, 5):
        X_lagged = add_lags(lags, X, y)
        new_df = pd.concat([X_lagged, y], axis=1).dropna()

        new_X = new_df.drop(columns="civic_sales")
        new_y = new_df["civic_sales"]
        
        X_train, X_test, y_train, y_test = train_test_split(new_X, new_y, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        model.fit(X_train, y_train)
        y_hat_train = model.predict(X_train)
        y_hat_test = model.predict(X_test)

        train_mse = mean_squared_error(y_train, y_hat_train)
        test_mse = mean_squared_error(y_test, y_hat_test)
        
        if best_test_mse == None or best_test_mse > test_mse:
            best_model = model
            best_train_mse = train_mse
            best_test_mse = test_mse
            best_num_lags = lags
        
    model = best_model
    train_mse = best_train_mse
    test_mse = best_test_mse
    
    train_rmse = np.sqrt(train_mse)
    test_rmse = np.sqrt(test_mse)
    
    print("Random split")
    print(f"{model.feature_names_in_=}")
    print(f"{model.feature_importances_=}")
    print(f"{train_mse=}")
    print(f"{test_mse=}")
    print(f"{train_rmse=}")
    print(f"{test_rmse=}")
    print(f"{best_num_lags=}")
    
    # Future predictions
    best_train_mse = None
    best_test_mse = None
    best_num_lags = None
    best_model = None
    
    for lags in range(0, 5):
        X_lagged = add_lags(lags, X, y)
        new_df = pd.concat([X_lagged, y], axis=1).dropna()

        new_X = new_df.drop(columns="civic_sales")
        new_y = new_df["civic_sales"]
        
        X_train = new_X[:-12]
        y_train = new_y[:-12]
        X_test = new_X[-12:]
        y_test = new_y[-12:]
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        model.fit(X_train, y_train)
        y_hat_train = model.predict(X_train)
        y_hat_test = model.predict(X_test)

        train_mse = mean_squared_error(y_train, y_hat_train)
        test_mse = mean_squared_error(y_test, y_hat_test)
        
        if best_test_mse == None or best_test_mse > test_mse:
            best_model = model
            best_train_mse = train_mse
            best_test_mse = test_mse
            best_num_lags = lags
        
    model = best_model
    train_mse = best_train_mse
    test_mse = best_test_mse
    
    train_rmse = np.sqrt(train_mse)
    test_rmse = np.sqrt(test_mse)
    
    print()
    print("Future prediction")
    print(f"{model.feature_names_in_=}")
    print(f"{model.feature_importances_=}")
    print(f"{train_mse=}")
    print(f"{test_mse=}")
    print(f"{train_rmse=}")
    print(f"{test_rmse=}")
    print(f"{best_num_lags=}")
    