import streamlit as st
import pandas as pd
import time
import enum
from io import BytesIO

from components.nav_bar import NavigationBar
from components.btn import Button

from core.plotter import check_dataframe, get_coordinates, plotMap

tool_state = enum.Enum("tool_state", "IDLE PLOT FINISHED")

if "tool_state" not in st.session_state:
    st.session_state.tool_state = tool_state.IDLE

if "map" not in st.session_state:
    st.session_state.map = None

if "file" not in st.session_state:
    st.session_state.file = None

if "data_frame" not in st.session_state:
    st.session_state.data_frame = None

if "input_select" not in st.session_state:
    st.session_state.input_select = "Excel"

if "tile_select" not in st.session_state:
    st.session_state.tile_select = "OpenStreetMap"

if "reset" not in st.session_state:
    st.session_state.reset_tool = False

match st.session_state.tool_state.value:
    case tool_state.IDLE.value:
        st.write(
            """
            # Map Plotter
            This is the tool page. You can use this page to data on a map.
            """
        )

        st.segmented_control(
            "Select input desired",
            options=["Excel", "Dataframe"],
            selection_mode="single",
            default="Excel",
            key="input_select",
        )

        match st.session_state.input_select:
            case "Excel":
                st.write(
                    """
                    Upload a Excel file with the following columns:
                    - Departure city
                    - Arrival city
                    - Line color (hexcode)
                    """
                )

                st.session_state.file = st.file_uploader(
                    "Upload a Excel file",
                    type=["xlsx"],
                    label_visibility="collapsed"
                )

                isdisabled = st.session_state.file is None

                pass
            
            case "Dataframe":
                st.write(
                    """
                    Upload a dataframe with the following columns:
                    - Departure city
                    - Arrival city
                    - Line color (hexcode)
                    """
                )

                df = pd.DataFrame({
                    "Departure city": pd.Series([], dtype="str"),
                    "Arrival city": pd.Series([], dtype="str"),
                    "Line color": pd.Series([], dtype="str"),
                })

                st.session_state.data_frame = st.data_editor(
                    df,
                    num_rows="dynamic",
                    use_container_width=True
                )

                isdisabled = False

                pass
        
        st.segmented_control(
            "Select tile desired",
            options=["OpenStreetMap", "Cartodb Positron", "Cartodb dark_matter"],
            selection_mode="single",
            default="OpenStreetMap",
            key="tile_select",
        )

        NavigationBar(
            right_btn=Button(
                label="Plot",
                icon="📊",
                disable=isdisabled,
                callback=lambda: st.session_state.update({"tool_state": tool_state.PLOT})
            ),
        ).display()

        pass
    
    case tool_state.PLOT.value:

        steps = [
            "Extract data",
            "Parse data",
            "Plot map",
            "map successfully plotted"
        ]

        progress_text = "Loading..."
        progress_bar = st.progress(0, text=progress_text)
        
        # Step 1: Extract data
        progress_text = f"Extracting data..."
        progress_bar.progress(0.1, text=progress_text)

        if st.session_state.input_select == "Excel":
            df = pd.read_excel(st.session_state.file)
        else:
            df = st.session_state.data_frame
        
        if df.empty:
            st.error("Empty dataframe")
            time.sleep(2)
            st.session_state.tool_state = tool_state.IDLE
            st.rerun()
        
        if check_dataframe(df, ["Departure city", "Arrival city", "Line color"]):
            st.session_state.data_frame = df
        else:
            st.error("Invalid dataframe. Please make sure it contains the required columns.")
            time.sleep(2)
            st.session_state.tool_state = tool_state.IDLE
            st.rerun()

        # Step 2: Parse data
        progress_text = f"Parsing data..."
        progress_bar.progress(0.25, text=progress_text)
        
        df["Departure lat"] = None
        df["Departure lon"] = None
        df["Arrival lat"] = None
        df["Arrival lon"] = None

        for index, row in df.iterrows():
            dep_city = row["Departure city"]
            arr_city = row["Arrival city"]

            dep_coords = get_coordinates(dep_city)
            arr_coords = get_coordinates(arr_city)

            if dep_coords and arr_coords:
                df.at[index, "Departure lat"] = dep_coords[0]
                df.at[index, "Departure lon"] = dep_coords[1]
                df.at[index, "Arrival lat"] = arr_coords[0]
                df.at[index, "Arrival lon"] = arr_coords[1]

        df = df.dropna()

        # Step 3: Plot map
        progress_text = f"Plotting map..."
        progress_bar.progress(0.5, text=progress_text)

        st.session_state.map = plotMap(
            df,
            tile=st.session_state.tile_select
        )

        # Step 4: Map successfully plotted
        progress_text = f"Map successfully plotted"
        progress_bar.progress(1.0, text=progress_text)

        st.session_state.tool_state = tool_state.FINISHED
        st.session_state.data_frame = df
        st.session_state.map = st.session_state.map
        st.session_state.file = None

        st.rerun()

        pass

    case tool_state.FINISHED.value:
        st.balloons()
        st.write(
            """
            # Map Plotter
            This is the tool page. You can use this page to data on a map.
            """
        )

        if st.session_state.get("map"):
            # Flag Button click
            st.session_state.reset_tool = False

            # Sauvegarde la carte dans un buffer HTML
            map_obj = st.session_state.map
            map_buffer = BytesIO()
            map_obj.save(map_buffer, close_file=False)

            # Proposer le téléchargement
            st.download_button(
                label="Download Map",
                icon=":material/download:",
                data=map_buffer,
                file_name="map.html",
                mime="text/html",
                key="download_map"
            )


            if st.button("Go Back", key="reset_tool_btn", icon="↩️"):
                st.session_state.reset_tool = True
                st.session_state.map = None
                st.session_state.file = None
                st.session_state.data_frame = None
                st.session_state.input_select = "Excel"
                st.session_state.tile_select = "OpenStreetMap"
                
                st.session_state.tool_state = tool_state.IDLE
                st.rerun()