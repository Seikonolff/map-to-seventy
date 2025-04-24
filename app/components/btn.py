"""
File: btn.py
Author: Mathis Labory
Date: 2025-02-12
Description: This file contains the Button class used in the To70 carbon footprint tool.
             The Button class is a wrapper around the Streamlit button with additional functionality.
"""

import streamlit as st

class Button:
    def __init__(self, label, type="primary", disable=False, icon=None, key=None, callback=None):
        self.label = label
        self.disable = disable
        self.type = type
        self.icon = icon
        self.key = key
        self.callback = callback
    
    def setDisabled(self, disabled):
        self.disabled = disabled
    
    def on_click(self, callback):
        self.callback = callback
        st.rerun()

    def display(self):
        st.button(self.label, type=self.type, icon=self.icon, disabled=self.disable, on_click=self.callback, key=self.key)