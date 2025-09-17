# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 00:29:21 2025

@author: achyu
"""
import pandas as pd
import datetime
import xgboost as xgb
import streamlit as st


REQUIRED_FEATURES = [
    'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type',
    'Transmission', 'Owner', 'Age'
]

FUEL_MAP = {'petrol': 0, 'diesel': 1, 'cng': 2}
SELLER_MAP = {'dealer': 0, 'individual': 1}
TRANS_MAP = {'manual': 0, 'automatic': 1}


def main():
    st.set_page_config(page_title="Car Price Forecasting", layout="centered")

    html_temp = """
    <div style="
        background-image: url('https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg');
        background-size: cover;
        background-position: center;
        height: 250px;
        border-radius:10px;
    ">
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Title below the cover photo
    st.markdown(
        "<h2 style='color:white; text-align:center; margin-top:20px;'>Car Price Forecasting 🚘</h2>", 
        unsafe_allow_html=True
    )

    st.write("Are you planning to sell your car? Let's predict its selling price. 🚗")

    # Load model
    model = xgb.XGBRegressor()
    model.load_model('xgd_model.json')

    mode = st.radio("Choose how you want to work:", ("Enter Manually", "Upload Dataset"))


    if mode == "Enter Manually":
        st.subheader(" Price Forecasting for a Single Car ( Existing Dataset )")

        p1 = st.number_input("Current ex-showroom price (in Lakhs)", 0.1, 100.0, value=5.0, step=0.1)
        p2 = st.number_input("Distance completed (Kms)", 0, 10_000_000, value=50000, step=100)

        s1 = st.selectbox("Fuel type", ('Petrol', 'Diesel', 'CNG'))
        p3 = 0 if s1 == "Petrol" else 1 if s1 == "Diesel" else 2
        s2 = st.selectbox("Seller type", ('Dealer', 'Individual'))
        p4 = 0 if s2 == "Dealer" else 1
        s3 = st.selectbox("Transmission", ('Manual', 'Automatic'))
        p5 = 0 if s3 == "Manual" else 1
        p6 = st.slider("No. of previous owners", 0, 10, value=0)

        years = st.number_input("Year purchased", 1990, datetime.datetime.now().year, value=2018)
        p7 = datetime.datetime.now().year - years

        data_new = pd.DataFrame({
            'Present_Price': [p1],
            'Kms_Driven': [p2],
            'Fuel_Type': [p3],
            'Seller_Type': [p4],
            'Transmission': [p5],
            'Owner': [p6],
            'Age': [p7]
        })

        if st.button("Predict Price"):
            try:
                pred = model.predict(data_new)
                st.balloons()
                st.success(f"Estimated selling price: {pred[0]:.2f} Lakhs")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

    else:
        st.subheader("🔹 Work with an Uploaded Dataset")

        uploaded_file = st.file_uploader("Upload CSV/Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.write(" Preview of uploaded file:")
                st.dataframe(df.head())

                # After uploading, you STILL enter fields manually
                st.subheader("Enter Car Details for Prediction")
                p1 = st.number_input("Current ex-showroom price (in Lakhs)", 0.1, 100.0, value=5.0, step=0.1)
                p2 = st.number_input("Distance completed (Kms)", 0, 10_000_000, value=50000, step=100)

                s1 = st.selectbox("Fuel type", ('Petrol', 'Diesel', 'CNG'))
                p3 = 0 if s1 == "Petrol" else 1 if s1 == "Diesel" else 2
                s2 = st.selectbox("Seller type", ('Dealer', 'Individual'))
                p4 = 0 if s2 == "Dealer" else 1
                s3 = st.selectbox("Transmission", ('Manual', 'Automatic'))
                p5 = 0 if s3 == "Manual" else 1
                p6 = st.slider("No. of previous owners", 0, 10, value=0)

                years = st.number_input("Year purchased", 1990, datetime.datetime.now().year, value=2018)
                p7 = datetime.datetime.now().year - years

                data_new = pd.DataFrame({
                    'Present_Price': [p1],
                    'Kms_Driven': [p2],
                    'Fuel_Type': [p3],
                    'Seller_Type': [p4],
                    'Transmission': [p5],
                    'Owner': [p6],
                    'Age': [p7]
                })

                if st.button("Predict Price from Uploaded Dataset"):
                    try:
                        pred = model.predict(data_new)
                        st.balloons()
                        st.success(f"Estimated selling price: {pred[0]:.2f} Lakhs")
                    except Exception as e:
                        st.error(f"Prediction failed: {e}")

           except Exception as e:
                st.error(f"Something went wrong while reading dataset: {e}")
  

if __name__ == '__main__':
    main()


