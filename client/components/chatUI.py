import streamlit as st
from utils.api import ask_question
from utils.chat_history import load_history, save_history


def render_chat():
    st.subheader("💬 Chat with your assistant")

    if "messages" not in st.session_state:  # It stores data between user interactions
        st.session_state.messages = load_history()  # Load persisted history from disk

    # render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])   # Creates chat bubble "user" → right side / "assistant" → left side

    # input and response
    user_input=st.chat_input("Type your question....")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})
        save_history(st.session_state.messages)

        response=ask_question(user_input)
        if response.status_code==200:
            data=response.json()
            answer=data["response"]
            sources=data.get("sources",[])
            st.chat_message("assistant").markdown(answer)
            # if sources:
            #     st.markdown("📄 **Sources: **")
            #     for src in sources:
            #         st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role":"assistant","content":answer})
            save_history(st.session_state.messages)
        else:
            st.error(f"Error: {response.text}")