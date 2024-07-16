import streamlit as st

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "code" not in st.session_state:
    st.session_state.code = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""
if "refactored_code" not in st.session_state:
    st.session_state.refactored_code = ""
if "detailed_review" not in st.session_state:
    st.session_state.detailed_review = ""

st.logo(image="img.png", icon_image="img.png")
st.set_page_config(page_title="ReviewNinja", page_icon=":ninja:", layout="wide")
with st.sidebar:
    st.title("ReviewNinja :ninja:")
    st.caption("Streamlining Your Code Review Process")


def main():
    home_page = st.Page("0_home.py", title="Home", icon="🏠")
    code_analysis_page = st.Page("1_code_analysis.py", title="Code Analysis", icon="🔎")
    code_refactoring_page = st.Page("2_code_refactoring.py", title="Code Refactoring", icon="🛠️")
    detailed_code_review_page = st.Page("3_detailed_code_review.py", title="Detailed Code Review", icon="📝")

    page = st.navigation(pages=[home_page, code_analysis_page, code_refactoring_page, detailed_code_review_page])

    page.run()


if __name__ == "__main__":
    main()
