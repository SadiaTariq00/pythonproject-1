import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweepers", layout='wide')

# Toggle for dark and light mode
mode = st.sidebar.radio("Select Mode:", ["Light", "Dark"], index=0)

# Apply custom CSS based on the selected mode
if mode == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: white;
        }
        .stApp, .stMarkdown, .stDataFrame, .stTextInput, .stButton, .stSelectbox, .stRadio {
            background-color: black !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stApp, .stMarkdown, .stDataFrame, .stTextInput, .stButton, .stSelectbox, .stRadio {
            background-color: white !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Description
st.title('Data Sweepers')
st.write('A tool to easily and efficiently search and retrieve data from various data sources.')

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(file)
        elif file_extension == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            continue

        # File details
        st.write(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader('Data Cleaning Options:')
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")
            
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

            st.subheader("Select columns to keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data visualization
            st.subheader('Data Visualization')
            if st.checkbox(f'Show visualization for {file.name}'):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion options
            st.subheader('Conversion Options:')
            conversion_types = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                
                if conversion_types == 'CSV':
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_extension, ".csv")
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_extension, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                buffer.seek(0)
                st.download_button(
                    label=f"Download {file_name} as {conversion_types}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("Congratulations! All files processed successfully.")
