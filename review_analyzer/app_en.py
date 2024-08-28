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
## Task: Analyze customer reviews for our product, the 'Review Analyzer'. Focus on extracting key points that a potential buyer would find helpful. Include sentiment analysis to determine overall customer satisfaction.
## Websites for Review: Please collect reviews from popular platforms like Facebook, Instagram, and other relevant forums based on the product's market presence.
## Objective: The goal is to provide potential customers with a clear and concise summary of what current users think about the product. Highlight the most praised features, common issues, and general sentiment.
## Additional: Summarize the analysis in about 200 words, indicating the sources of the reviews and the number of posts analyzed. Ensure the summary is straightforward and easy to understand, tailored to assist in making purchasing decisions.
- Brand: {brand},
- Product:{product},
- Region: {region}
"""

def init_page():
    st.set_page_config(
        page_title="Product Review Checker AI Agent",
        page_icon="🔍"
    )
    st.header("Product Review Checker AI Agent🔍")


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
        brand = st.text_input("Enter the brand name (e.g., Nike)", key="brand")
        product = st.text_input("Enter the product name (e.g., Air Force One shoes)", key="product")
        region = st.text_input("Enter your region (e.g., USA)", key="region", value="USA")
        if st.button("Submit"):
            result = chain.stream({"brand": brand, "product": product, "region": region})
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