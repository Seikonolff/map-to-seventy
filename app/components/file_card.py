"""
File: file_card.py
Author: Mathis Labory
Date: 2025-02-12
Description: This component represents a file card that displays the file name and size,
             and provides a button to clear the uploaded file.
"""

import streamlit as st
    
class FileCard:
    def __init__(self, file):
        self.file = file
    
    def display(self):
        with st.container(border=1):
            file_name_col, space, file_size_col, clear_btn = st.columns([5, 1, 4, 2], vertical_alignment="center")

        with file_name_col:
            st.write(f"**{self.file.name}**")

        with file_size_col:
            st.write(f"Size: {self.file.size / 1024:.2f} KB")
        
        with clear_btn:
            if st.button("Clear", type="secondary", icon="❌", key="clear_file"):
                st.session_state.uploaded_file = None
                st.rerun()