import streamlit as st
from utils.chat_history import clear_history

def render_history_download():
    if st.session_state.get("messages"):
        chat_text="\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("⬇️ Download Chat History", chat_text, file_name="chat_history.txt", mime="text/plain")

        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            clear_history()
            st.rerun()