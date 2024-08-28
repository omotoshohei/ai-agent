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
## Task: Provide detailed and personalized career advice based on the user's current situation and aspirations.
## User Information:
- Current Career Status: {input_status}
- Career Goals: {input_goal}
- Skills and Experience: {input_skill}
- Interests: {input_interest}
- Preferred Work Environment: {input_environment}
- Location: {input_location}
- Challenges: {input_challenges}

## Objective: Offer actionable and supportive career advice that helps the user achieve both their short-term and long-term goals. Include strategies for overcoming challenges, leveraging skills, and aligning with their interests and preferred work environment. Provide specific tips and recommendations tailored to the user's unique context.

## Additional: Ensure the advice is clear, practical, and tailored to assist the user in making informed decisions about their career path.
"""

def init_page():
    st.set_page_config(
        page_title="Career Advice AI Agent",
        page_icon="🧘"
    )
    st.header("Career Advice AI Agent🧘")


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
        input_status = st.selectbox("Current Career Status",("Student", "Entry-Level Employee", "Senior-Level Employee", "Career Changer", "Unemployed/Job Seeker", "Entrepreneur"),key="input_status")
        input_goal = st.text_input("Career Goals (e.g., Become recognized as an expert in digital marketing field)", key="input_goal")
        input_skill = st.text_input("Skills and Experience (e.g., SEO and digital marketing)", key="input_skill")
        input_interest = st.text_input("Interests (e.g., Data Science and Python)", key="input_interest")
        input_environment = st.selectbox("Preferred work environment",("Corporate Office", "Startup", "Remote Work", "Freelance/Contract", "Government/Public Sector"),key="input_environment")
        input_location = st.text_input("Location (e.g., Tokyo)", key="input_location")
        input_challenges = st.text_input("Challenges (e.g., High competition for jobs in the field, making it difficult to stand out to employers.)", key="input_challenges")
        if st.button("Submit"):
            result = chain.stream({"input_status": input_status, "input_goal": input_goal, "input_skill": input_skill, "input_interest": input_interest, "input_environment": input_environment, "input_location": input_location, "input_challenges": input_challenges})
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


