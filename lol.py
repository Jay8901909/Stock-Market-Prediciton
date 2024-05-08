# Import necessary libraries
import os
from datetime import date
import streamlit as st
import yfinance as yf
from prophet import Prophet
import plotly.graph_objs as go
import plotly.express as px

# Define a class for session state
class SessionState:
    def __init__(self):
        self.user_logged_out = False

# Create a SessionState instance
session_state = SessionState()

# Set page configuration
st.set_page_config(
    page_title="Stock Market Prediction",
    page_icon="statistics.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Display logout button in the top right corner
logout_button = f'''
    <div style="position: absolute; right: 20px;">
        <form action="http://192.168.15.126:5000/fk">
            <input type="submit" value="Logout" style="background-color:#339966; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
        </form>
    </div>
'''
st.markdown(logout_button, unsafe_allow_html=True)

# Display welcome message with first name
first_name = st.experimental_get_query_params().get('first_name', [''])[0]
welcome_message = f'<div style="position: absolute; font-family: \'Bradley Hand\', cursive; color: black; font-size: 20px;">Welcome {first_name}!</div>'
st.markdown(welcome_message, unsafe_allow_html=True)

# Title for the app
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; background-color: #339966; color: white; padding: 5px; border-radius: 10px;">
        <h1 style="font-family: 'Bradley Hand', cursive; text-decoration: none;">Stock Market Prediction</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Input for stock symbol
selected_stock = st.text_input('Enter stock symbol (e.g., TATAPOWER, RELIANCE,MRF)', 'MRF')
if selected_stock and not selected_stock.upper().endswith('.NS'):
    selected_stock += '.NS'

# Slider for years of prediction
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Define the start date for fetching historical data
START = "2015-01-01"

# Load data function with error handling and documentation
@st.cache_data
def load_data(ticker):
    """
    Fetch historical stock data using yfinance.

    Parameters:
        - ticker (str): Stock symbol.

    Returns:
        - pd.DataFrame: DataFrame containing historical stock data.
    """
    try:
        data = yf.download(ticker, START)
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)

if data is not None:
    data_load_state.text('Loading data... done!')

    # Display raw data
    st.subheader('Original data')
    st.dataframe(data.tail(), use_container_width=True)

    # Check for missing values
    if data.isnull().values.any():
        st.warning("The data contains missing values. Please handle them before proceeding.")
    else:
        # Plot raw data
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], line=dict(color='green'), name="stock_open"))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], line=dict(color='red'), name="stock_close"))
            fig.update_layout(title_text='Time Series data with Range-slider(dynamic time series data)', xaxis_rangeslider_visible=True)
            
           # Remove "Produced with Plotly" text and icon
            config = {'displayModeBar': False}
            st.plotly_chart(fig, use_container_width=True, config=config)
            # st.plotly_chart(fig, use_container_width=True)

        plot_raw_data()

        # Predict forecast with Prophet
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        # Drop rows with missing values
        df_train = df_train.dropna()

        # Check if there is enough data for training
        if len(df_train) < 2:
            st.warning("Insufficient data for training. Please select a different stock or time range.")
        else:
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)

            # Replace yhat with a more descriptive term
            forecast.rename(columns={'yhat': 'predictive_value', 'yhat_lower': 'minimum_prediction', 'yhat_upper': 'maximum_predictive_value'}, inplace=True)

            # Ensure predictive values and minimum values are non-negative and not less than 1
            forecast['predictive_value'] = forecast['predictive_value'].apply(lambda x: max(1, x))
            forecast['minimum_prediction'] = forecast['minimum_prediction'].apply(lambda x: max(1, x))

            # Show and plot forecast
            st.subheader('Predicted data')

            # Display forecast data
            st.dataframe(forecast[['ds', 'predictive_value', 'minimum_prediction', 'maximum_predictive_value']].tail(), use_container_width=True)

            st.write(f'Predicted data for {n_years} years')

            # Create a Plotly figure with uncertainty intervals
            fig1 = go.Figure()

            # Plotting the predictive values
            fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['predictive_value'], mode='lines', line=dict(color='blue'), name='Predicted'))

            # Plotting the minimum prediction with adjusted values
            fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['minimum_prediction'], mode='lines', line=dict(color='red'), name='Low_Prediction'))
            fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['maximum_predictive_value'], mode='lines', line=dict(color='green'), name='High_Prediction'))

            # Customize the layout
            fig1.update_layout(title_text=f'Predicted data for {n_years} years', xaxis_title='Date', yaxis_title='Stock Value')

           # Remove "Produced with Plotly" text and icon
            config = {'displayModeBar': False}
            st.plotly_chart(fig1, use_container_width=True, config=config)

            #st.plotly_chart(fig1, use_container_width=True)

# Hide Streamlit menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Prevent Streamlit from automatically opening a browser window
os.environ["STREAMLIT_SERVER_ADDRESS"] = ""
