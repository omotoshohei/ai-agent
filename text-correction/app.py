import streamlit as st
import openai

# Constants and configurations
AI_MODEL = "gpt-4o"
TOKEN_COUNT = 4096
MAX_USES = 3

# Set the page title and favicon
st.set_page_config(page_title="Text Correction", page_icon=":bar_chart:")

# Load the API key
openai.api_key = st.secrets['OPENAI_API_KEY']

# Page title
st.title('Sentence Correction')

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

# Initialize usage count and language in session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

def correct_text(language, input_text):
    """Generate corrected text using OpenAI API based on the input text and language."""
    if st.session_state['usage_count'] < MAX_USES:
        st.session_state['usage_count'] += 1
        prompt = f"Correct the following {language} sentence. The output language should be {language}. Here is the text: {input_text}"
        with st.spinner('Loading... Please wait.'):
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
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
    en_input = st.text_area("Enter your English text here:", key="en_input")
    if st.button("Correct", key="en_correction"):
        result = correct_text("English", en_input)
        if result:
            st.write(result)
else:
    st.subheader('日本語')
    ja_input = st.text_area("日本語を入力ください", key="ja_input")
    if st.button("校正する", key="ja_correction"):
        result = correct_text("Japanese", ja_input)
        if result:
            st.write(result)

