# TO70 Map Maker Tool

## Description
**TO70 Map Maker Tool** is a tool designed to visualize data on a map.

## Installation
To install the tool, open a terminal and run the following command:
```bash
git clone https://github.com/Seikonolff/map-to_seventy.git
```

## Virtual Environment
It is recommended to use the tool in a virtual environment. To create and use one, follow these steps:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

After activating the environment, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Launching the Tool
To launch the tool, run the following commands:
```bash
cd app
streamlit run main.py
```