import streamlit as st


def display_chat(messages):
    for msg in messages:
        st.chat_message(msg["role"], avatar="🥷" if msg["role"] == "assistant" else "👨🏻‍💻").markdown(msg["content"])


def detailed_code_review_tab():
    st.logo(image="img.png", icon_image="img.png")
    st.title("Detailed Code Review :memo:")
    st.write("Get a detailed review of your refactored code.")

    # Display history
    st.markdown("**Review History**")
    review_messages = [msg for msg in st.session_state.messages if msg.get("type") == "review"]
    display_chat(review_messages)

    if not st.session_state.refactored_code:
        st.warning("Please refactor the code first in the 'Code Refactoring' tab.")
    else:
        if st.button("Review :mag_right:"):
            with st.chat_message("assistant", avatar="🥷"):
                st.markdown(st.session_state.detailed_review)

            st.success("Code reviewed successfully.")


detailed_code_review_tab()
