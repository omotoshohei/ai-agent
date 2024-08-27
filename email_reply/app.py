import streamlit as st
import openai

# Streamlit page configuration
st.set_page_config(page_title="Email Reply Generator", page_icon=":bar_chart:")

# Load secrets
openai.api_key = st.secrets['OPENAI_API_KEY']
prompt = st.secrets['PROMPT_EMAIL_REVIEW_GENERATOR']

# Title of the page
st.title('Email Reply Generator')

# Initialize or retrieve the usage count and language from session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

max_uses = 3

# Define a function to handle API requests and increase modularity
def generate_reply(input_sender, input_subject, input_message, input_reply, language):
    st.session_state['usage_count'] += 1
    with st.spinner('Loading... Please wait.'):
        user_prompt = f"- Task: {prompt} - Output language: {language}. - Sender: {input_sender}. - Email Subject: {input_subject}. - Email Message: {input_message}. - What you want to say: {input_reply}."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4096
        )
        return response["choices"][0]["message"]["content"]

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

# Check usage count to limit API calls
if st.session_state['usage_count'] < max_uses:
    # Display form based on selected language
    if st.session_state['language'] == 'English':
        # English Input Section
        with st.form(key='en_form'):
            st.subheader('English')
            en_input_sender = st.selectbox("Sender",("Co-worker", "Boss", "Client", "Friend"),key="en_input_sender")
            en_input_subject = st.text_input("Email Subject (e.g., About scheduling a meeting)", key="en_input_subject")
            en_input_message = st.text_area("Content of the recipient's email: (e.g., I would like to adjust the time for tomorrow's meeting, are you available in the afternoon?)", key="en_input_message")
            en_input_reply = st.text_input("What you want to say: (e.g., I am available after 2 PM.)", key="en_input_reply")
            submit_en = st.form_submit_button("Generate an Email Reply")
            if submit_en:
                result = generate_reply(en_input_sender, en_input_subject, en_input_message, en_input_reply, en_input_length, "English")
                st.write(result)
    else:
        # Japanese Input Section
        with st.form(key='ja_form'):
            st.subheader('日本語')
            ja_input_sender = st.selectbox("送信主",("同僚", "上司", "クライアント", "友達"),key="ja_input_sender")
            ja_input_subject = st.text_input("メールの件名 (例：ミーティングの日程調整について)", key="ja_input_subject")
            ja_input_message = st.text_area("相手のメールの内容： (例：明日、ミーティングの時間を調整したいのですが、午後の時間帯は空いていますか？)", key="ja_input_message")
            ja_input_reply = st.text_input("伝えたいこと： (例：午後2時以降は空いています。)", key="ja_input_reply")
            submit_ja = st.form_submit_button("Eメールの返信を生成する")
            if submit_ja:
                result = generate_reply(ja_input_sender, ja_input_subject, ja_input_message, ja_input_reply, ja_input_length, "Japanese")
                st.write(result)
else:
    st.error("You have reached your maximum usage limit.")

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