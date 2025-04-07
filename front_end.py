import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"  # URL ของ API server

def update_form():
    data_1 = st.session_state["data_1"]
    data_2 = st.session_state["data_2"]
    data_3 = st.session_state["data_3"]
    data_4 = st.session_state["data_4"]
    data_5 = st.session_state["data_5"]
    if data_1 and data_2 and data_3 and data_4 and data_5:
        response = requests.post(f"{API_URL}/add_data", json={
            "data_1": data_1, "data_2": data_2, "data_3": data_3, "data_4": data_4, "data_5": data_5
        })
        if response.status_code == 200:
            st.session_state["form_submitted"] = True
            st.session_state["data_1"] = ""
            st.session_state["data_2"] = ""
            st.session_state["data_3"] = ""
            st.session_state["data_4"] = ""
            st.session_state["data_5"] = ""
            st.session_state["cache_buster"] += 1
    else:
        st.session_state["form_submitted"] = False

def clear_form():
    st.session_state["data_1"] = ""
    st.session_state["data_2"] = ""
    st.session_state["data_3"] = ""
    st.session_state["data_4"] = ""
    st.session_state["data_5"] = ""
    st.session_state["form_submitted"] = False

def main():
    st.set_page_config(page_title="Program MC1", layout="wide")
    st.markdown("""
    <style>
    .stTextInput > div > input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #4CAF50;
        width: 100%;
        margin: 0;
        margin-top: 0px;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #e04343;
    }
    .title { text-align: center; font-size: 36px; color: #4CAF50; margin-bottom: 20px; }
    .subheader { font-size: 24px; color: #333; display: flex; align-items: center; gap: 10px; margin-bottom: 0; }
    .input-container { display: flex; align-items: center; gap: 10px; margin-bottom: -50px; margin-top: -5px; padding: 0; }
    .input-label { font-size: 16px; color: #333; margin: 0; }
    .icon { font-size: 20px; }
    .dataframe td, .dataframe th { text-align: center !important; }
    .stSelectbox > div > select { border-radius: 10px; padding: 8px; border: 2px solid #4CAF50; width: 150px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Program MC1</div>', unsafe_allow_html=True)

    if "cache_buster" not in st.session_state:
        st.session_state["cache_buster"] = 0
    if "form_submitted" not in st.session_state:
        st.session_state["form_submitted"] = False

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="subheader"><span class="icon">📝</span>Input Data</div>', unsafe_allow_html=True)
        with st.form(key="data_form"):
            st.markdown('<div class="input-container"><span class="icon">1️⃣</span><span class="input-label">data_1</span></div>', unsafe_allow_html=True)
            st.text_input("Data 1", placeholder="Enter data_1", key="data_1", label_visibility="hidden")
            st.markdown('<div class="input-container"><span class="icon">2️⃣</span><span class="input-label">data_2</span></div>', unsafe_allow_html=True)
            st.text_input("Data 2", placeholder="Enter data_2", key="data_2", label_visibility="hidden")
            st.markdown('<div class="input-container"><span class="icon">3️⃣</span><span class="input-label">data_3</span></div>', unsafe_allow_html=True)
            st.text_input("Data 3", placeholder="Enter data_3", key="data_3", label_visibility="hidden")
            st.markdown('<div class="input-container"><span class="icon">4️⃣</span><span class="input-label">data_4</span></div>', unsafe_allow_html=True)
            st.text_input("Data 4", placeholder="Enter data_4", key="data_4", label_visibility="hidden")
            st.markdown('<div class="input-container"><span class="icon">5️⃣</span><span class="input-label">data_5</span></div>', unsafe_allow_html=True)
            st.text_input("Data 5", placeholder="Enter data_5", key="data_5", label_visibility="hidden")

            button_col1, button_col2 = st.columns(2)
            with button_col1:
                submit_button = st.form_submit_button(label="Submit  📤", on_click=update_form)
            with button_col2:
                clear_button = st.form_submit_button(label="Clear Data  🗑️", on_click=clear_form)

        if submit_button:
            if st.session_state["form_submitted"]:
                st.success("Data processed successfully! ✅")
            else:
                st.error("Please fill in all fields. ⚠️")
        if clear_button:
            st.info("Input fields cleared! 🧹")

    with col2:
        st.markdown('<div class="subheader"><span class="icon">📊</span>Latest Data</div>', unsafe_allow_html=True)
        shift_option = st.selectbox("Select Shift", ["All", "A", "B", "C", "D"], index=0, key="shift_select")
        response = requests.get(f"{API_URL}/get_data?shift_option={shift_option}")
        if response.status_code == 200 and response.json()["data"]:
            df = pd.DataFrame(response.json()["data"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No data available yet. 📉")

if __name__ == "__main__":
    main()