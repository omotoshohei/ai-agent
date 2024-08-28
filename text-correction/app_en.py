import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

###### dotenv を利用する場合 ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################


PROMPT = """
Correct the following sentence. 
The output language should be English. 
Here is the text: {text}
"""

def init_page():
    st.set_page_config(
        page_title="Text Correction AI Agent",
        page_icon="✍️"
    )
    st.header("Text Correction AI Agent ✍️")


def select_model(temperature=0):
    models = ("GPT-4o","GPT-4o-mini", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model_choice = st.radio("Choose a model:", models)
    if model_choice == "GPT-4o":
        return ChatOpenAI(temperature=temperature, model_name="gpt-4o")
    elif model_choice == "GPT-4o-mini":
        return ChatOpenAI(temperature=temperature, model_name="gpt-4o-mini")
    elif model_choice == "Claude 3.5 Sonnet":
        return ChatAnthropic(temperature=temperature, model_name="claude-3-5-sonnet-20240620")
    elif model_choice == "Gemini 1.5 Pro":
        return ChatGoogleGenerativeAI(temperature=temperature, model="gemini-1.5-pro-latest")

def init_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        ("user", PROMPT),
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

def main():
    init_page()
    chain = init_chain()
    if chain:
        text = st.text_area("Enter your English text here:", key="text")
        if st.button("Generate Text"):
            result = chain.stream({"text": text})
            st.write(result)   
      

if __name__ == '__main__':
    main()

# Style adjustments (optional, remove if not needed)
st.markdown(
"""
<style>
/* Custom style adjustments */
.st-emotion-cache-iiif1v { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)