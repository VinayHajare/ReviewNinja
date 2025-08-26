import streamlit as st

st.logo(image="img.png", icon_image="img.png")
st.title("Welcome to ReviewNinja 🥷🏻")
st.subheader("Streamlining Your Code Review Process")
st.markdown("""
    **ReviewNinja** is a tool designed to help developers improve their code through comprehensive analysis, refactoring, and detailed review.
    """)

# Overview Section
st.markdown("")
st.markdown("### Overview")
st.markdown("""
    ReviewNinja simplifies the code review process by providing automated analysis, refactoring suggestions, and detailed reviews. Whether you're a solo developer or part of a team, ReviewNinja can help you write cleaner, more efficient code.
    """)

# Features Section
st.markdown("")
st.markdown("### Features")
col1, col2, col3 = st.columns(3)
with col1:
        st.markdown("#### :mag: Code Analysis")
        st.markdown("""
        Analyze your code to identify potential issues and areas for improvement.
        - Detect bugs and vulnerabilities
        - Highlight code smells
        - Provide improvement suggestions
        """)
with col2:
        st.markdown("#### :hammer_and_wrench: Code Refactoring")
        st.markdown("""
        Automatically refactor your code for better readability and performance.
        - Optimize code structure
        - Improve maintainability
        - Enhance performance
        """)
with col3:
        st.markdown("#### :memo: Detailed Code Review")
        st.markdown("""
        Get a thorough review of your code, including suggestions for further improvements.
        - Comprehensive feedback
        - Best practices recommendations
        - Code quality assessment
        """)

# Getting Started Section
st.markdown("")
st.markdown("### Getting Started")
st.markdown("""
    1. **Navigate to the Code Analysis page**: Enter your code and get an initial analysis.
    2. **Proceed to Code Refactoring**: Use the analysis results to refactor your code automatically.
    3. **Finish with Detailed Code Review**: Get an in-depth review and further suggestions to improve your code.
    """)

# Footer
st.markdown("---")
st.markdown("""
    **ReviewNinja** is developed to assist developers and streamline the process of code reviews. For any questions or support, please contact us [here](http://www.vinayhajare.engineer).

    """)
