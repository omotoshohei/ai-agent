import streamlit as st
import openai

# Constants
AI_MODEL = "gpt-4o"
TOKEN_COUNT = 4096
MAX_USES = 3

# Set the page configuration
st.set_page_config(page_title="Rap Generator", page_icon=":bar_chart:")

# Load the API key and prompt from secrets
openai.api_key = st.secrets['OPENAI_API_KEY']
prompt_template = st.secrets['PROMPT_RAP_GENERATOR']

# Style adjustments (optional, remove if not needed)
st.markdown(
"""
<style>
/* Custom style adjustments */
.st-emotion-cache-iiif1v { display: none !important; }
.st-emotion-cache-gh2jqd {padding: 6rem 1rem 0rem;}
@media (max-width: 50.5rem) {
.st-emotion-cache-gh2jqd {
max-width: calc(0rem + 100vw);
}
}
</style>
""",
    unsafe_allow_html=True,
)

# Page title
st.title('Rap Generator')

# Initialize or retrieve the usage count from session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

def generate_rap(language, topic, occupation, message):
    """Generate a rap based on the user's inputs."""
    if st.session_state['usage_count'] < MAX_USES:
        st.session_state['usage_count'] += 1  # Increment the usage counter
        rap_prompt = f"""
        - Task: {prompt_template}.
        - Output language: {language}.
        - Topic: {topic}.
        - Occupation: {occupation}.
        - What you want to say: {message}.
        - Don't exceed more than 8 lines.
        """
        with st.spinner('Generating your rap... Please wait.'):
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": rap_prompt}],
                max_tokens=TOKEN_COUNT
            )
        return response["choices"][0]["message"]["content"]
    else:
        st.error("You have reached your maximum usage limit.")
        return None

# Determine button text based on current language
if st.session_state['language'] == 'English':
    switch_button_text = 'Japanese（日本語）'
else:
    switch_button_text = 'English'

# Language switcher button
if st.button(switch_button_text):
    if st.session_state['language'] == 'English':
        st.session_state['language'] = 'Japanese'
    else:
        st.session_state['language'] = 'English'
    st.experimental_rerun()

# Display form based on selected language
if st.session_state['language'] == 'English':
    st.subheader('English')
    en_topic = st.text_input("Topic (e.g., Sunday)", key="en_topic")
    en_occupation = st.text_input("Your Occupation (e.g., Data Scientist)", key="en_occupation")
    en_message = st.text_input("What do you want to say? (e.g., prepare for tomorrow)", key="en_message")
    if st.button("Generate a rap", key="en_generate_rap"):
        result = generate_rap("English", en_topic, en_occupation, en_message)
        if result:
            st.write(result)
else:
    st.subheader('日本語')
    ja_topic = st.text_input("トピック（例：日曜日）", key="ja_topic")
    ja_occupation = st.text_input("あなたの仕事（例：データサイエンティスト）", key="ja_occupation")
    ja_message = st.text_input("言いたいこと（例：明日に向けて気持ちを準備したい）", key="ja_message")
    if st.button("ラップを生成する", key="ja_generate_rap"):
        result = generate_rap("Japanese", ja_topic, ja_occupation, ja_message)
        if result:
            st.write(result)

