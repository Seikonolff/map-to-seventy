import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

navigator = st.navigation([
    st.Page("tool_page.py", title="Tool", icon="🧭"),
])

def main():
    navigator.run()

if __name__ == "__main__":
    main()