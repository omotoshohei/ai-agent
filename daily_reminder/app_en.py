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
1. Task: Generate a unique motivational or reflective quote that relates directly to the user's reported feeling and plan for the day. 
1-1.Ensure the quote is relevant and offers either support or inspiration based on the specific emotional context provided. 
1-2.Avoid repeating any quotes, and do not use quotes by Steve Jobs. 
1-3.Seek out lesser-known quotes and consider a diverse range of cultural and historical sources to enrich the variety and inclusiveness of the selections. 
Provide a brief explanation of why the chosen quote fits the situation described by the user.

2.Feeling: {feeling}.
3.Reason for the feeling: {reason}.
4.Plan for the day: {plan}.
5. Explain within 100 words in English.
"""

def init_page():
    st.set_page_config(
        page_title="Daily Reminder",
        page_icon="🧘"
    )
    st.header("Daily Reminder🧘")


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
        feeling = st.selectbox(
            "How are you feeling today?",
            ("I want to be more motivated", "I'm feeling sad", "I'm angry", "I just want to relax today", "I feel excited", "I'm feeling anxious"),
            key="feeling"
        )
        reason = st.text_input("What's the reason for this feeling?", key="reason")
        plan = st.text_input("What's your plan for today?", key="plan")
        if st.button("Submit"):
            result = chain.stream({"feeling": feeling, "reason": reason, "plan": plan})
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