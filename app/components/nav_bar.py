"""
File: navigation_bar.py
Author: Mathis Labory
Date: 2025-02-12
Description: This module defines the NavigationBar class, which is used to create a navigation bar with optional left and right buttons.
             The navigation bar is displayed using Streamlit columns.
"""

import streamlit as st

class NavigationBar:
    def __init__(self, left_btn=None, right_btn=None):
        self.left_width = None
        self.space = None
        self.right_width = None

        self.left_btn = left_btn
        self.right_btn = right_btn

        '''
        self.left_width = 0.28 * len(self.left_btn.label) if self.left_btn else 1.5
        self.right_width = 0.28 * len(self.right_btn.label) if self.right_btn else 1.2
        self.space_width = max(1, 12 - self.left_width - self.right_width)
        
        self.left_width, self.space, self.right_width = st.columns(
            [self.left_width,self.space_width, self.right_width], 
            gap="small",
            vertical_alignment="center",
        )
        '''
        self.left_width, self.space, self.right_width = st.columns([1.5, 5.8, 1.2])
    
    def display(self):
        with self.left_width:
            if self.left_btn:
                self.left_btn.display()
            else:
                st.empty()
        
        with self.space:
            st.empty()
        
        with self.right_width:
            if self.right_btn:
                self.right_btn.display()
            else:
                st.empty()

    