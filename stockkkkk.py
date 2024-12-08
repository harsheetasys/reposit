import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import plotly.graph_objects as go
import streamlit as st
from datetime import date

# Streamlit UI Setup
st.set_page_config(page_title="Stock Price Prediction App", layout="centered", initial_sidebar_state="auto")

# Sidebar Configuration
st.sidebar.header("Stock Price Prediction")
st.sidebar.markdown("Select the company and date range to predict future stock prices.")

# Dropdown for stock selection in the sidebar
stock_options = {
    'Apple (AAPL)': 'AAPL',
    'Google (GOOG)': 'GOOG',
    'Microsoft (MSFT)': 'MSFT',
    'Amazon (AMZN)': 'AMZN',
    'Tesla (TSLA)': 'TSLA',
    'Facebook (META)': 'META'
}

stock_choice = st.sidebar.selectbox("Select a Company:", list(stock_options.keys()))
stock_ticker = stock_options[stock_choice]

# User input for date range in the sidebar
start_date = st.sidebar.date_input("From Date", value=date(2015, 1, 1), max_value=date.today())
end_date = st.sidebar.date_input("To Date", min_value=start_date, max_value=date.today())

# Option for predicting future prices
forecast_days = st.sidebar.slider("Number of days to forecast into the future", min_value=1, max_value=30, value=7)

# Main Page Title
st.title(f"Stock Price Prediction for {stock_choice}")

# Cache the data fetching to avoid re-downloading
@st.cache_data
def load_stock_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# Button to trigger stock data download and prediction
if st.sidebar.button('Predict Stock Price'):

    # Download stock data using yfinance
    with st.spinner('Fetching stock data...'):
        data = load_stock_data(stock_ticker, start_date, end_date)

    # Handling missing values by filling forward
    data.fillna(method='ffill', inplace=True)

    # Display the current stock price
    current_price = data['Close'].iloc[-1]
    previous_price = data['Close'].iloc[-2]
    if current_price > previous_price:
        st.metric(label="Current Stock Price", value=f"${current_price:.2f}", delta=f"{(current_price - previous_price):.2f}", delta_color="normal")
    else:
        st.metric(label="Current Stock Price", value=f"${current_price:.2f}", delta=f"{(current_price - previous_price):.2f}", delta_color="inverse")

    # Visualize the historical stock price
    st.subheader("Historical Stock Prices")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price', line=dict(color='royalblue')))
    st.plotly_chart(fig, use_container_width=True)

    # Preprocessing the data
    df = data['Close'].values.reshape(-1, 1)

    # Feature scaling
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    # Define train and test size
    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[0:train_size, :]
    test_data = scaled_data[train_size - 60:, :]

    # Function to create dataset
    def create_dataset(dataset, time_step=60):
        X, y = [], []
        for i in range(len(dataset) - time_step - 1):
            X.append(dataset[i:(i + time_step), 0])
            y.append(dataset[i + time_step, 0])
        return np.array(X), np.array(y)

    X_train, y_train = create_dataset(train_data)
    X_test, y_test = create_dataset(test_data)

    # Reshape data for LSTM
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    with st.spinner('Training the LSTM model...'):
        model.fit(X_train, y_train, batch_size=32, epochs=20)
    st.success("Model trained successfully!")

    # Predict on test data
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)

    # Adjust the length of the test data to match the predictions
    test = df[train_size:train_size + len(predictions), :]  # Adjust the length of test data
    test = pd.DataFrame(test, columns=['Actual Price'])
    test['Predictions'] = predictions

    # Forecast future prices
    last_60_days = scaled_data[-60:]
    X_forecast = []
    for i in range(forecast_days):
        pred_input = last_60_days.reshape(1, last_60_days.shape[0], 1)
        forecast_pred = model.predict(pred_input)
        last_60_days = np.append(last_60_days[1:], forecast_pred, axis=0)
        X_forecast.append(scaler.inverse_transform(forecast_pred)[0, 0])

    # Display forecast results
    future_dates = pd.date_range(end_date, periods=forecast_days + 1)[1:]
    future_dates = future_dates.date
    forecast_df = pd.DataFrame(X_forecast, index=future_dates, columns=['Forecast Price'])
    st.subheader("Predicted Future Stock Prices")
    st.dataframe(forecast_df)

    # Plot the predicted vs actual prices and future predictions
    st.subheader("Predicted vs Actual Stock Prices")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=test.index, y=test['Actual Price'], mode='lines', name='Actual Price', line=dict(color='yellow')))
    fig2.add_trace(go.Scatter(x=test.index, y=test['Predictions'], mode='lines', name='Predicted Price', line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=future_dates, y=forecast_df['Forecast Price'], mode='lines', name='Future Predictions', line=dict(color='green')))
    st.plotly_chart(fig2, use_container_width=True)
