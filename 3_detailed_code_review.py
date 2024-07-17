import streamlit as st
from utils import stream_text_word_by_word

def display_chat(messages):
    for msg in messages:
        st.chat_message(msg["role"], avatar="🥷" if msg["role"] == "assistant" else "👨🏻‍💻").markdown(msg["content"])


def review():
    yield st.session_state.detailed_review

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
                #st.write_stream(stream_text_word_by_word(st.session_state.detailed_review))
                st.write_stream(review())
                st.session_state.messages.append({"role": "assistant", "content": st.session_state.detailed_review, "type": "review"})

            st.success("Code reviewed successfully.")


detailed_code_review_tab()
