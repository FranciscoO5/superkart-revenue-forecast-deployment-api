# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkartAPI = Flask("SuperKart Revenue Forecast")

# Load the trained machine learning model
model = joblib.load("rfTunedModel.joblib")

# Define a route for the home page (GET request)
@superkartAPI.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Revenue Forecast API!"

# Define an endpoint for single prediction (POST request)
@superkartAPI.post('/v1/predict')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Type_Category': product_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction
    return jsonify({'Sales': round(prediction, 2)})

# Define an endpoint for batch prediction (POST request)
@superkartAPI.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing product details for multiple entries
    and returns the predicted sales as a list in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all products in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

    # Round the predictions to 2 decimal places
    predicted_sales = [round(sale, 2) for sale in predicted_sales]

    # Return the predictions list as a JSON response
    return jsonify({'Sales': predicted_sales})


# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkartAPI.run(debug=True)
