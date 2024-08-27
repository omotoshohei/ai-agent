import streamlit as st
import openai

# Constants
AI_MODEL = "gpt-4o"
TOKEN_COUNT = 4096
MAX_USES = 3

# Set page configuration
st.set_page_config(page_title="Code Debugging Tool", page_icon=":bar_chart:")

###### dotenv を利用しない場合は消してください ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################


# Load API key and prompt from secrets
# openai.api_key = st.secrets['OPENAI_API_KEY']
# prompt_template = st.secrets['PROMPT_DEBUG']

# Page title
st.title('Code Debugging Tool')

# Styling (optional)
st.markdown(
"""
<style>
/* Custom style adjustments */
.st-emotion-cache-iiif1v { display: none !important; }
.st-emotion-cache-13ln4jf {padding: 6rem 1rem 0rem;}
@media (max-width: 50.5rem) {
.st-emotion-cache-13ln4jf {
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
    st.session_state['language'] = 'English'

def generate_from_ai(language, input_task, input_code, input_error):
    """Generates requirements based on the given instructions and background context."""
    if st.session_state['usage_count'] < MAX_USES:
        st.session_state['usage_count'] += 1  # Increment the usage counter
        task_prompt = f"""
        - Output language: {language}
        - Task: {input_task}
        - Current Code: {input_code}
        - Error Message: {input_error}
        """
        with st.spinner('Defining requirements...'):
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": task_prompt}],
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
    en_input_task = st.text_input(
        "Enter the Task / What do you want to do with your code? (e.g., Review my code below and correct the mistakes)",
        value="Review my code below and correct the mistakes",
        key="en_input_task"
    )
    en_input_code = st.text_area(
        "Paste your code here",
        key="en_input_code"
    )
    en_input_error = st.text_area(
        "Paste the error message here",
        key="en_input_error"
    )
    if st.button("Debug", key="en_fixed_code"):
        result = generate_from_ai("English", en_input_task, en_input_code, en_input_error)
        if result:
            st.write(result)
else:
    st.subheader('日本語')
    ja_input_task = st.text_input(
        "タスクの内容、またはしたいことを入力ください。 (例：下記のコードをレビューして修正ください。)",
        value="下記のコードをレビューして修正ください",
        key="ja_input_task"
    )
    ja_input_code = st.text_area(
        "現在のコードを入力ください",
        key="ja_input_code"
    )
    ja_input_error = st.text_area(
        "エラーメッセージを入力ください",
        key="ja_input_error"
    )
    if st.button("デバッグする", key="ja_fixed_code"):
        result = generate_from_ai("Japanese", ja_input_task, ja_input_code, ja_input_error)
        if result:
            st.write(result)
