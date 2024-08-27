import streamlit as st
import openai

# Constants
AI_MODEL = "gpt-4o"
TOKEN_COUNT = 4096
MAX_USES = 3

# Set the page configuration
st.set_page_config(page_title="Translation", page_icon=":bar_chart:")

# Load the API key from Streamlit's secrets
openai.api_key = st.secrets['OPENAI_API_KEY']

# Page title
st.title('Translation')

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

# Initialize usage counter and language in session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'Japanese to English'

def translate_text(input_text, source_language, target_language):
    """Function to handle text translation between two languages."""
    if st.session_state['usage_count'] < MAX_USES:
        st.session_state['usage_count'] += 1  # Increment the counter
        prompt = f"Translate from {source_language} to {target_language}. Here is the text: {input_text}"
        with st.spinner(f'Translating from {source_language} to {target_language}... Please wait.'):
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
if st.session_state['language'] == 'Japanese to English':
    switch_button_text = 'English to Japanese（英語から日本語）'
else:
    switch_button_text = 'Japanese to English（英語から日本語）'

# Language switcher button
if st.button(switch_button_text):
    if st.session_state['language'] == 'Japanese to English':
        st.session_state['language'] = 'English to Japanese'
    else:
        st.session_state['language'] = 'Japanese to English'
    st.experimental_rerun()

# Display form based on selected language
if st.session_state['language'] == 'Japanese to English':
    st.subheader('Japanese to English')
    ja_input = st.text_area("Enter your Japanese text here:", key="ja_input")
    if st.button("Translate", key="ja_translate"):
        result = translate_text(ja_input, "Japanese", "English")
        if result:
            st.write(result)
else:
    st.subheader('English to Japanese')
    en_input = st.text_area("Enter your English text here:", key="en_input")
    if st.button("Translate", key="en_translate"):
        result = translate_text(en_input, "English", "Japanese")
        if result:
            st.write(result)
