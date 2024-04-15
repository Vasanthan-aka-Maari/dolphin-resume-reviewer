import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64
import fitz

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Initialize a list to hold the text of each page
        text_parts = []

        # Iterate over the pages of the PDF to extract the text
        for page in document:
            text_parts.append(page.get_text())

        # Concatenate the list into a single string with a space in between each part
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="Dolphin Reviewer", page_icon="dolphin", layout="wide")

st.header("Dolphin Reviewer 🐬")
st.text("Generally dolphins are smart but I'm smarter 😏. I know 18+3 is 59. ~ D (🐬)")
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume as PDF 👇", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

st.subheader("Oki, choose what you want me to do?")

submit1 = st.button("Rewrite my bio from resume with proper keywords")

submit2 = st.button("How Can I Improve my Skills")

submit3 = st.button("What are the Keywords That are Missing")

submit4 = st.button("Percentage match")

input_prompt1 = """
You are an skilled ATS (Applicant Tracking System) scanner named Dolphin with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the job description and pick the keywords that are important for the resume but missing and 
rewrite the bio from the resume with the keywords so that it can pass the ATS. The bio should be within 60 words.
"""

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager named Dolphin, your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. Keep your answer brief, crisp and in a fun tone.
# """

input_prompt2 = """
You are an Technical Human Resource Manager named Dolphin, 
 and your role is to understand the resume and the job description given and provide a list of skills the candidate is missing inorder to be the best fit for the job description given. Give me a brief about the skills and how or where to attain those skills.
Do not include anything about you or give an intro to your answer.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner named Dolphin with a deep understanding of the ATS functionality, 
your task is to evaluate the resume against the provided job description. Assess the compatibility of the resume with the role. Give out a list of skills that the candidate need to have inorder to be the best for the job description.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner named Dolphin with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts. Keep your answer brief, crisp and in a professional tone.
""" 

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Here you go:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Here you go:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Here you go:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("Here you go:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

footer = """
---
Dolphin says "good night and byeeee ❤️" \n
Built with 🤏🧠 by Rohith, Gokul, Sabeeh, Vasanthan
"""

st.markdown(footer, unsafe_allow_html=True)
