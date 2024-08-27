import streamlit as st
import openai

# Streamlit page configuration
st.set_page_config(page_title="Anger Management Tool", page_icon=":bar_chart:")

# Load secrets
# openai.api_key = st.secrets['OPENAI_API_KEY']

###### dotenv を利用しない場合は消してください ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################

prompt =  """
You are an AI assistant specializing in anger management. Your task is to provide thoughtful, practical, and effective advice to help the user manage their anger in a given situation. The advice should be tailored based on the following inputs:
- Who the user is angry at
- The user's level of anger (on a scale from 1 to 5)
- The specific situation that caused the anger

Your response should:
1. Briefly acknowledge the user's feelings to validate their emotions.
2. Provide practical steps or techniques to manage and reduce their anger.
3. Encourage the user to address the underlying issue in a constructive manner.
4. Offer additional resources or tips that could help the user in similar situations in the future.

Ensure your response flows naturally without explicitly stating the sections. Use empathetic and supportive language throughout.

Example response structure (do not include section headers in your response):
1. Acknowledge the user's feelings.
2. Provide practical steps or techniques.
3. Encourage constructive action.
4. Offer additional resources or tips.

Remember to be empathetic and supportive.
"""



# Title of the page
st.title('Anger Management Tool')

# Style adjustments (optional, remove if not needed)
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

# Initialize or retrieve the usage count and language from session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

max_uses = 3

# Define a function to handle API requests and increase modularity
def generate_from_ai(input_who, input_anger_level, input_situation, language):
    st.session_state['usage_count'] += 1
    with st.spinner('Loading... Please wait.'):
        user_prompt = f"- Task: {prompt} - Output language: {language}. - Who are you angry at?: {input_who}. - Your anger level(out of 5): {input_anger_level}. - Situation: {input_situation}. - Explain within 180 words in English, or 600 charactors in Japanese."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1500
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
            en_input_who = st.selectbox("Who are you angry at?", ("Your boss", "Your co-worker", "Your family or relatives", "Your friend"), key="en_input_who")
            en_input_anger_level = st.selectbox("Your anger level", ("1", "2", "3", "4", "5"), key="en_anger_level")
            en_input_situation = st.text_input("Explain the situation (e.g., My boss gives me too much work to handle.)", key="en_input_situation")
            submit_en = st.form_submit_button("Generate a Suggestion")

            if submit_en:
                result = generate_from_ai(en_input_who, en_input_anger_level, en_input_situation, "English")
                st.write(result)
    else:
        # Japanese Input Section
        with st.form(key='ja_form'):
            st.subheader('日本語')
            ja_input_who = st.selectbox("誰に怒っていますか?", ("上司", "同僚", "パートナー", "家族、または親戚", "友達"), key="ja_input_who")
            ja_input_anger_level = st.selectbox("怒りのレベル", ("1", "2", "3", "4", "5"), key="ja_anger_level")
            ja_input_situation = st.text_input("状況を説明ください (例：上司が多すぎる仕事を依頼してきた。)", key="ja_input_situation")
            submit_ja = st.form_submit_button("提案を生成")

            if submit_ja:
                result = generate_from_ai(ja_input_who, ja_input_anger_level, ja_input_situation, "Japanese")
                st.write(result)
else:
    st.error("You have reached your maximum usage limit.")
