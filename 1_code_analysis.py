import streamlit as st
from utils import analyze


def display_chat(messages):
    for msg in messages:
        #st.chat_message(msg["role"], avatar="🥷" if msg["role"] == "assistant" else "👨🏻‍💻").markdown(msg["content"])
        if msg["role"] == "assistant":
            st.chat_message("🥷", avatar="🥷").markdown(msg["content"])
        else:
            st.chat_message("👨🏻‍💻", avatar="👨🏻‍💻").code(msg["content"])



st.logo(image="img.png", icon_image="img.png")
st.title("Code Analysis :mag:")
st.write("Enter your code and analyze it.")

# Display history
st.markdown("### Analysis History:")
analysis_messages = [msg for msg in st.session_state.messages if msg.get("type") in ["prompt", "analysis"]]
display_chat(analysis_messages)


if codeInput := st.chat_input("Enter your code here:", key="codeInput"):
    st.session_state.code = codeInput
    st.chat_message("user", avatar="👨🏻‍💻").code(codeInput)
    st.session_state.messages.append({"role": "user", "content": codeInput, "type": "prompt"})
    with st.chat_message("assistant", avatar="🥷"):
        st.write_stream(analyze(codeInput))

    st.success("Code analyzed successfully.")
