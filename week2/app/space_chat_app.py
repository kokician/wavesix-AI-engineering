import streamlit as st
import requests

st.set_page_config(page_title="Space Explorer Chat", page_icon="🚀", layout="centered")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#1e90ff;'>🚀 Space Explorer Chat 🚀</h1>
        <p>Ask me anything about space, planets, stars, black holes, or the universe!</p>
    </div>
""", unsafe_allow_html=True)

question = st.text_input("💬 Type your space question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Exploring the cosmos..."):
            try:
                res = requests.post("http://localhost:8000/chat", json={"question": question})
                res.raise_for_status()
                st.success(res.json()["answer"])
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                st.error("Please check your FastAPI server or API key.")
