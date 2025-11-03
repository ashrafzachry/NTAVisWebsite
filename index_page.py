# index_page.py
import streamlit as st
import streamlit.components.v1 as components

with open("index.html", "r") as f:
    html_content = f.read()

components.html(html_content, height=800, scrolling=True)
