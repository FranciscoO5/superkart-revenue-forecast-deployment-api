import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860" 

# Set the title of the Streamlit app
st.title("SuperKart Revenue Forecast Frontend")
st.write('This application predicts the sales revenue for SuperKart products.')

# Section for online prediction
st.subheader("Enter Product Details for Single Prediction:")

# Collect user input for product and store features
product_weight = st.number_input('Product Weight', value=12.66, min_value=4.0, max_value=22.0, help="Weight of the product")
product_sugar_content = st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'], help="Sugar content level")
product_allocated_area = st.number_input('Product Allocated Area', value=0.06, min_value=0.004, max_value=0.298, help="Ratio of display area allocated to the product")
product_mrp = st.number_input('Product MRP', value=150.0, min_value=31.0, max_value=266.0, help="Maximum Retail Price of the product")
store_size = st.selectbox('Store Size', ['Medium', 'High', 'Small'], help="Size of the store")
store_location_city_type = st.selectbox('Store Location City Type', ['Tier 2', 'Tier 1', 'Tier 3'], help="Type of city where the store is located")
store_type = st.selectbox('Store Type', ['Supermarket Type2', 'Departmental Store', 'Supermarket Type1', 'Food Mart'], help="Type of the store")
product_id_char = st.selectbox('Product ID Character', ['FD', 'NC', 'DR'], help="First two characters of the Product ID (e.g., FD, NC, DR)")
store_age_years = st.number_input('Store Age (Years)', value=17, min_value=1, max_value=50, help="Age of the store in years")
product_type_category = st.selectbox('Product Type Category', ['Non Perishables', 'Perishables'], help="Category indicating if the product is perishable or not")


# Make prediction when the "Predict" button is clicked
if st.button("Predict Sales", type="primary"):
    # Prepare the data as a dictionary to send to the Flask API
    payload = {
        'Product_Weight': product_weight,
        'Product_Sugar_Content': product_sugar_content,
        'Product_Allocated_Area': product_allocated_area,
        'Product_MRP': product_mrp,
        'Store_Size': store_size,
        'Store_Location_City_Type': store_location_city_type,
        'Store_Type': store_type,
        'Product_Id_char': product_id_char,
        'Store_Age_Years': store_age_years,
        'Product_Type_Category': product_type_category
    }

    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
        if response.status_code == 200:
            prediction = response.json().get('Sales')
            st.success(f'Predicted Sales: ${prediction:.2f}')
        else:
            st.error(f'Error from backend: {response.status_code} - {response.text}')
    except requests.exceptions.ConnectionError:
        st.error('Could not connect to the backend API. Please ensure the backend is running and the URL is correct.')
    except Exception as e:
        st.error(f'An unexpected error occurred: {e}')

# Section for batch prediction
st.subheader("Batch Prediction")

st.markdown("Upload a CSV file with columns matching the features above (`Product_Weight`, `Product_Sugar_Content`, `Product_Allocated_Area`, `Product_MRP`, `Store_Size`, `Store_Location_City_Type`, `Store_Type`, `Product_Id_char`, `Store_Age_Years`, `Product_Type_Category`) for batch predictions.")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", key="batch_predict_button", type="primary"):
        files = {'file': uploaded_file.getvalue()}
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
            if response.status_code == 200:
                predictions = response.json().get('Sales')
                predictions_df = pd.DataFrame({'Predicted Sales': predictions})
                st.success("Batch predictions completed!")
                st.dataframe(predictions_df) # Display the predictions as a DataFrame
            else:
                st.error(f'Error from backend: {response.status_code} - {response.text}')
        except requests.exceptions.ConnectionError:
            st.error('Could not connect to the backend API. Please ensure the backend is running and the URL is correct.')
        except Exception as e:
            st.error(f'An unexpected error occurred: {e}')
