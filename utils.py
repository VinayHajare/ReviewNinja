import re
import os
import streamlit as st
from llama_cpp import Llama
from llama_cpp_agent import LlamaCppAgent
from llama_cpp_agent.providers import LlamaCppPythonProvider
from llama_cpp_agent import MessagesFormatterType
from huggingface_hub import hf_hub_download

llm = None
llm_model = ""

def is_file_in_models_directory(file_name: str, models_directory: str = "models") -> bool:
    """
    Checks if the given file is present in the models directory.

    Args:
        file_name (str): The name of the file to check.
        models_directory (str): The path to the models directory. Default is "models".

    Returns:
        bool: True if the file is present, False otherwise.
    """
    # Construct the full path to the file
    file_path = os.path.join(models_directory, file_name)
    
    # Check if the file exists at the specified path
    return os.path.isfile(file_path)


if is_file_in_models_directory("Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf", "models"):
    hf_hub_download(
        repo_id="VinayHajare/Meta-Llama-3-8B-Instruct-GGUF-v2",
        filename="Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf",
        local_dir="./models"
    )

def get_context_by_model(model_name: str):
    model_context = {
        "Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf": 8000,
        "codeqwen-1_5-7b-chat-q6_k.gguf": 65536,
        "Codestral-22B-v0.1-Q6_K.gguf": 32768,
        "AutoCoder-Q6_K.gguf": 16384
    }
    return model_context.get(model_name)


def get_message_formatter_type(model_name: str):
    if any(keyword in model_name for keyword in ["Meta"]):
        return MessagesFormatterType.LLAMA_3
    elif any(keyword in model_name for keyword in ["codeqwen"]):
        return MessagesFormatterType.CHATML
    elif any(keyword in model_name for keyword in ["Codestral"]):
        return MessagesFormatterType.MISTRAL
    elif any(keyword in model_name for keyword in ["AutoCoder"]):
        return MessagesFormatterType.AUTOCODER
    else:
        return MessagesFormatterType.MISTRAL


@st.cache_data
def load_model(model: str = "Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf"):
    global llm
    global llm_model
    context = get_context_by_model(model)

    if llm is None or llm_model != model:
        # llm = Llama.from_pretrained(
        #     repo_id="VinayHajare/Meta-Llama-3-8B-Instruct-GGUF-v2",
        #     filename="Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf",
        #     # additional_files=["Meta-Llama-3-70B-Instruct-v2.Q6_K-00002-of-00002.gguf"],
        #     local_dir="./models",
        #     flash_attn=True,
        #     n_gpu_layers=81,
        #     n_batch=1024,
        #     n_ctx=context,
        # )
        llm = Llama(
            model_path=f"models/{model}",
            flash_attn=True,
            n_gpu_layers=81,
            n_batch=1024,
            n_ctx=context,
        )


def remove_tags(text):
    # Define a regular expression pattern to match tags like <scratchpad>, <principle_analysis_1>, etc.
    pattern = r'<[^>]+>'
    # Substitute all occurrences of the pattern with an empty string
    cleaned_text = re.sub(pattern, '', text)
    # Return the cleaned text
    return cleaned_text.strip()

def analyze(
        message: str,
        model: str = "Meta-Llama-3-8B-Instruct-v2.Q6_K.gguf",
        system_message: str = "You are a helpful assistant.",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 40,
        repetition_penalty: float = 1.1,
):
    load_model(model)
    provider = LlamaCppPythonProvider(llm)

    settings = provider.get_provider_default_settings()
    settings.temperature = temperature
    settings.top_k = top_k
    settings.top_p = top_p
    settings.max_tokens = max_tokens
    settings.repeat_penalty = repetition_penalty
    settings.stream = True

    agent = LlamaCppAgent(
        provider,
        system_prompt="You are a code analysis tool",
        predefined_messages_formatter_type=get_message_formatter_type(model),
        debug_output=True
    )

    # Collect the entire output from the stream
    code_analysis = ""
    code_analysis_stream = agent.get_chat_response(
        f"""Your task is to analyze a provided code snippet based on 10 good coding principles and create a report on the code quality.
        The 10 principles are:
        1. Follow Code Specifications
        2. Documentation and Comments
        3. Robustness
        4. Follow the SOLID principle
        5. Make Testing Easy
        6. Abstraction
        7. Utilize Design Patterns, but don't over-design
        8. Reduce Global Dependencies
        9. Continuous Refactoring
        10. Security is a Top Priority

        Here is the code to analyze:

        <code>
        {message}
        </code>

        First, carefully review the code and take notes on how well it adheres to each of the 10 principles. Write your notes inside <scratchpad> tags.
        Next, for each of the 10 principles, provide an analysis of how well the code follows that principle. Include specific examples from the code to support your analysis. Write each analysis inside <principle_analysis> tags with the principle number, like this:
        <principle_analysis_1>
        Analysis for principle 1 goes here.
        </principle_analysis_1>

        After analyzing all 10 principles, summarize the overall code quality, highlighting the main strengths and areas where the code could be improved. Provide this summary inside <code_quality_summary> tags.
        Finally, give the code a score from 1 (very poor quality) to 10 (excellent quality) based on its overall adherence to the 10 principles. Provide the score inside <code_quality_score> tags.
        Remember, the goal is to provide a thorough and constructive analysis to help improve the code quality. Be specific and support your analysis with examples from the code.
        """,
        llm_sampling_settings=settings,
        returns_streaming_generator=True,
        print_output=False
    )

    for output in code_analysis_stream:
        code_analysis += output

    # Clean the collected output
    cleaned_code_analysis = remove_tags(code_analysis)

    # Stream the cleaned output
    yield cleaned_code_analysis

    st.session_state.messages.append({"role": "assistant", "content": cleaned_code_analysis, "type": "analysis"})
    st.session_state.analysis_result = cleaned_code_analysis

    agent.system_prompt = "You are a refactoring expert"
    refactoring_suggestions_stream = agent.get_chat_response(
        f"""Here is some code that needs refactoring:
        <code>
        {message}
        </code>

        And here is an analysis of the code:

        <code_analysis>
        {cleaned_code_analysis}
        </code_analysis>

        Please carefully review the provided code and analysis. In a <scratchpad> section, think through how the code could potentially be refactored to improve its structure, readability, and maintainability. Consider things like:

        - Opportunities to apply relevant design patterns
        - Ways to remove any duplication
        - How to better organize and modularize the code
        - Improvements to naming conventions
        - Enhancements to code style and formatting

        After brainstorming ideas in the scratchpad, provide your suggestions for refactoring the code in a <suggestions> section. Explain your reasoning for each suggestion. Where relevant, include code snippets to illustrate your proposed changes.
        """,
        llm_sampling_settings=settings,
        # chat_history=messages,
        returns_streaming_generator=True,
        print_output=False
    )

    refactoring_suggestions = ""
    for output in refactoring_suggestions_stream:
        refactoring_suggestions += output

    cleaned_refactoring_suggestions = remove_tags(refactoring_suggestions)


    st.session_state.messages.append({"role": "assistant", "content": cleaned_refactoring_suggestions, "type": "refactored"})
    st.session_state.refactored_code = cleaned_refactoring_suggestions

    agent.system_prompt = "You are the code review moderator"

    final_review_stream = agent.get_chat_response(
        f"""You will be summarizing the key findings and recommendations from a code review process. Your goal is to provide an overall assessment of the code quality and suggest next steps for the developer based on the code analysis results and refactoring suggestions provided.
            First, include the code analysis results in a <code_analysis> section, like this:
            <code_analysis>
            {cleaned_code_analysis}
            </code_analysis>
            Next, include the refactoring suggestions in a <refactoring_suggestions> section:
            <refactoring_suggestions>
            {cleaned_refactoring_suggestions} 
            </refactoring_suggestions>
            Then, think through your overall assessment of the code quality and what the next steps for the developer should be based on the code analysis and refactoring suggestions. Write out your thought process in a <scratchpad> section. Consider:
            - What are the key takeaways from the code analysis? 
            - How critical are the issues identified?
            - Do the refactoring suggestions address the main problems?
            - What is your overall assessment of the current state of the code?
            - What should the developer prioritize to improve the code quality?
            Finally, write a summary of the key findings, your overall assessment of the code quality, and your recommendations for next steps inside an <answer> section. Make sure to touch on the main insights from the code analysis and refactoring suggestions in your response.
            """,
        llm_sampling_settings=settings,
        # chat_history=messages,
        returns_streaming_generator=True,
        print_output=False
    )

    final_review = ""
    for output in final_review_stream:
        final_review += output

    cleaned_final_review = remove_tags(final_review)


    st.session_state.detailed_review = cleaned_final_review
    st.session_state.messages.append({"role": "assistant", "content": cleaned_final_review, "type": "review"})

    print("Response Ended")
