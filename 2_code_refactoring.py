import streamlit as st


def display_chat(messages):
    for msg in messages:
        st.chat_message(msg["role"], avatar="🥷" if msg["role"] == "assistant" else "👨🏻‍💻").markdown(msg["content"])


def code_refactoring_tab():
    st.logo(image="img.png", icon_image="img.png")
    st.title("Code Refactoring :hammer_and_wrench:")
    st.write("Refactor your analyzed code.")

    # Display history
    st.markdown("**Refactoring History**")
    refactoring_messages = [msg for msg in st.session_state.messages if msg.get("type") == "refactored"]
    display_chat(refactoring_messages)

    if not st.session_state.analysis_result:
        st.warning("Please analyze the code first in the 'Code Analysis' tab.")
    else:
        if st.button("Refactor :repeat:"):
            with st.chat_message("assistant", avatar="🥷"):
                st.markdown(st.session_state.refactored_code)

            st.success("Code refactored successfully.")


code_refactoring_tab()
