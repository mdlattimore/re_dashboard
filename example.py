import streamlit as st
import requests


def retrieve_book(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()
    return data

with st.form("isbn_form"):
    isbn_input = st.text_input("ISBN:")
    submitted = st.form_submit_button("Search")

if submitted and isbn_input:
    data = retrieve_book(isbn_input)
    st.write(data)
