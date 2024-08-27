import streamlit as st
import openai

# Constants
AI_MODEL = "gpt-4o"
TOKEN_COUNT = 2000
MAX_USES = 3

# Set the page title and favicon
st.set_page_config(page_title="Daily Reminder", page_icon=":bar_chart:")

# Load API key and prompt template from secrets
try:
    openai.api_key = st.secrets['OPENAI_API_KEY']
    prompt_template = st.secrets['PROMPT_DAILY_REMINDER']
except KeyError:
    st.error("API key or prompt template is missing in the secrets.")
    st.stop()

# Page title
st.title('Daily Reminder')

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
    st.session_state['language'] = 'English'

def generate_reminder(language, feeling, reason, plan):
    """Generates a daily reminder based on the user's mood and plans."""
    if st.session_state['usage_count'] < MAX_USES:
        st.session_state['usage_count'] += 1  # Increment the usage counter
        reminder_prompt = f"""
        - Task: {prompt_template}
        - Output language: {language}.
        - Feeling: {feeling}.
        - Reason for the feeling: {reason}.
        - Plan for the day: {plan}.
         - Explain within 100 words in English, or 150 characters in Japanese.
         - Display with only single language. Don't mix Japanese and English.
        """
        with st.spinner('Generating your daily reminder...'):
            response = openai.ChatCompletion.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": reminder_prompt}],
                max_tokens=TOKEN_COUNT
            )
        return response["choices"][0]["message"]["content"]
    else:
        st.error("You have reached your maximum usage limit.")
        return None

# Determine button text based on current language
switch_button_text = 'Japanese（日本語）' if st.session_state['language'] == 'English' else 'English'

# Language switcher button
if st.button(switch_button_text):
    st.session_state['language'] = 'Japanese' if st.session_state['language'] == 'English' else 'English'
    st.experimental_rerun()

# Display form based on selected language
if st.session_state['language'] == 'English':
    st.subheader('English')
    en_feeling = st.selectbox(
        "How are you feeling today?",
        ("I want to be more motivated", "I'm feeling sad", "I'm angry", "I just want to relax today", "I feel excited", "I'm feeling anxious"),
        key="en_feeling"
    )
    en_reason = st.text_input("What's the reason for this feeling?", key="en_reason")
    en_plan = st.text_input("What's your plan for today?", key="en_plan")
    if st.button("Generate a daily reminder", key="en_generate"):
        result = generate_reminder("English", en_feeling, en_reason, en_plan)
        if result:
            st.write(result)
else:
    st.subheader('日本語')
    ja_feeling = st.selectbox(
        "今日の気分を教えてください?",
        ("モチベーションを上げたい", "悲しい", "怒っている", "今はリラックスしたい", "ワクワクしている", "不安を感じている"),
        key="ja_feeling"
    )
    ja_reason = st.text_input("その理由は何ですか？", key="ja_reason")
    ja_plan = st.text_input("今日の予定は何ですか？", key="ja_plan")
    if st.button("今日の名言を生成する", key="ja_generate"):
        result = generate_reminder("Japanese", ja_feeling, ja_reason, ja_plan)
        if result:
            st.write(result)

