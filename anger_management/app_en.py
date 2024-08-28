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
You are an AI assistant specializing in anger management. Your task is to provide thoughtful, practical, and effective advice to help the user manage their anger based on:
- Who the user is angry at: {who}
- The specific situation that caused the anger: {content}

1. Acknowledge the user's feelings to validate their emotions.
2. Provide practical steps or techniques to manage and reduce their anger.
3. Encourage the user to address the underlying issue in a constructive manner.
4. Offer additional resources or tips for similar situations in the future.
"""

def init_page():
    st.set_page_config(
        page_title="Anger Management - AI Agent Navi",
        page_icon="🧘"
    )
    st.header("Anger Management - AI Agent Navi🧘")


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
        who = st.text_input("Who are you angry at?", key="who")
        content = st.text_area("What specific situation caused the anger?", key="content")
        if st.button("Submit"):
            result = chain.stream({"who": who, "content": content})
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
