import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def plot_forecasted_trends(hashtag_data):
    # Convert input data to DataFrame
    df = pd.DataFrame(hashtag_data)
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce')  # Convert to datetime
    df = df.dropna()  # Drop rows with NaN values

    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(df)

    # Create future dataframe for prediction
    future = model.make_future_dataframe(periods=7)  # Forecast for the next 7 days

    # Predict the future
    forecast = model.predict(future)

    # Plot the forecast
    fig = model.plot(forecast)
    plt.title("Hashtag Trend Forecast")
    return fig
