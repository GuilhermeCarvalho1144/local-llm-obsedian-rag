import streamlit as st
import requests
import logging

logging.basicConfig(level=logging.INFO, filemode="w")
logger = logging.getLogger(__name__)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

API_URL = st.sidebar.text_input("API URL", value="http://localhost:8000")

st.title("Echo bot")

# create msg history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        response = requests.get(
            f"{API_URL}/echo", params={"message": prompt}, timeout=10
        )
        response.raise_for_status()
        data = response.json()["reply"]
    except Exception as e:
        data = f"Backend error: {e}"
        logger.error("Error while calling backend: %s", e)
    with st.chat_message("assistant"):
        st.markdown(data)
    st.session_state.messages.append({"role": "assistant", "content": data})
