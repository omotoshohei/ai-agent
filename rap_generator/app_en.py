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
Generate a rap that strictly adheres to the following structure to ensure completeness and coherence:
- Length: Exactly 8 lines, each line containing 8 beats.
- Rhyme Scheme: Use an ABAB rhyme scheme throughout to maintain a rhythmic and lyrical flow.
- Content: Reflect the given topic, occupation, and personal message in the lyrics. The rap should start with an introduction to the theme, follow with the body that develops the idea, and conclude with a strong ending.
- Style: Incorporate internal rhymes and multisyllabic rhymes to enhance the lyrical complexity.
- Tone: Align the tone with the sentiment of the personal message, ranging from motivational to contemplative, depending on the input.
Ensure each line transitions smoothly to the next, maintaining thematic and rhythmic continuity. The rap must complete all 8 lines to provide a full narrative arc.
- Topic:{topic},
- Occupation:{occupation},
- Personal Message:{message}
"""

def init_page():
    st.set_page_config(
        page_title="Rap Generator AI Agent",
        page_icon="🎶"
    )
    st.header("Rap Generator AI Agent 🎶")


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
        topic = st.text_input("Topic (e.g., Sunday)", key="topic")
        occupation = st.text_input("Your Occupation (e.g., Data Scientist)", key="occupation")
        message = st.text_input("What do you want to say? (e.g., prepare for tomorrow)", key="message")
        if st.button("返信を生成する"):
            result = chain.stream({"topic": topic, "occupation": occupation, "message": message})
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