import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from Functions import dataProcessor as DtPR

def train_multiple_dfs(df_list):
    trained_models = []

    for i, df in enumerate(df_list):
        # Assuming your DataFrame has columns 'HHMM' and 'Use'
        X = df[['HHMM']]  # Features
        y = df['Use']      # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a linear regression model
        model = LinearRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error for DataFrame {i}: {mse}')

        # Plot the actual vs predicted values
        plt.scatter(X_test, y_test, color='black', label='Actual')
        plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Predicted')
        plt.xlabel('HHMM')
        plt.ylabel('Use')
        plt.title(f'Actual vs Predicted Bicycle Usage - DataFrame {i}')
        plt.legend()
        plt.show()

        trained_models.append(model)

    return trained_models
dateRange = DtPR.chooseDate()
wkdayList, wkendList = DtPR.weekdays_weekends(dateRange)
dateList, dayList = zip(*wkdayList)
original_df_list = DtPR.readCSV(dateList)
filtered_df_list = DtPR.filtering(original_df_list)
df_list = DtPR.sumByUse(filtered_df_list)

trained_models = train_multiple_dfs(df_list)

# Example: Make predictions using the first trained model
first_model = trained_models[0]
new_data = pd.DataFrame({'HHMM': [5, 10, 15, 20]})
predictions = first_model.predict(new_data[['HHMM']])
print("Predictions:", predictions)