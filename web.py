# -*- coding: utf-8 -*-

import datetime
import streamlit as st  #Web App
import requests
import os
import shutil
import app
import aspose.words as aw
from PIL import Image, ImageOps
from pdf2image import convert_from_path

#Make streamlit to wide screen
st.set_page_config(layout="wide")

# Hide made with streamlit and Hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Uploading file in the form of pdf, doc and docx format 
image = Image.open(r'BPAI_logo.png')
st.image(image)
st.header("ARABIC PARSER")
input_file=st.file_uploader(label='UPLOAD FILE HERE:',type=['pdf','doc','docx','jpg','jpeg','png'])

# Checking uploaded file is pdf or doc or docx
if input_file is not None:
    os.mkdir('fileDir')
    # os.mkdir('uploaded_files')
    if input_file.type == "application/pdf":
        with open(os.path.join("uploaded_files", input_file.name),"wb") as f:
                f.write((input_file).getbuffer())
        pdf_file = os.path.join("./uploaded_files/", input_file.name)
        data = app.extraction(pdf_file)
        # Create two columns, one for the PDF and the other for the extracted data
        col1, col2 = st.columns(2)
        
        # Convert the first page of the PDF file to an image and display it in the first column
        with col1:
            st.subheader("Uploaded File")
            st.write(" ")
            pages = convert_from_path(pdf_file, 500, first_page=1)
            for page in pages:
                image = ImageOps.autocontrast(page.convert('RGB'))
                st.image(image, use_column_width=True)
        
        # Display the extracted data in the second column
        with col2:
            st.subheader("Extracted Details")
            st.write(" ")
            st.write(data)
            # for k,v in data.items():
            #     st.write(k,":", v)

        st.success("Data Extracted Successfully")
        # shutil.rmtree("./uploaded_files/")
            
    else:
        doc = aw.Document(input_file)
        doc.save("./uploaded_files/temp.pdf")
        app.extraction('./uploaded_files/temp.pdf')
else:
    st.write("Upload a pdf")