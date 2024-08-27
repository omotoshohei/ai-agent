import streamlit as st
import openai

# Streamlit page configuration
st.set_page_config(page_title="Career Advice AI Generator", page_icon=":bar_chart:")

# Load secrets
# openai.api_key = st.secrets['OPENAI_API_KEY']
# prompt = st.secrets['PROMPT_CAREER_ADIVCE']

###### dotenv を利用しない場合は消してください ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################

# Title of the page
st.title('Career Advice AI Generator')

# Style adjustments (optional, remove if not needed)
st.markdown(
"""
<style>
/* Custom style adjustments */
.st-emotion-cache-iiif1v { display: none !important; }
.st-emotion-cache-13ln4jf {padding: 6rem 1rem 0rem;}
@media (max-width: 50.5rem) {.st-emotion-cache-13ln4jf {max-width: calc(0rem + 100vw);}}
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
def generate_reply(input_status, input_goal, input_skill, input_interest,input_environment,input_location, input_challenges,language):
    st.session_state['usage_count'] += 1
    with st.spinner('Loading... Please wait.'):
        user_prompt = f"- Task: {prompt} - Output language: {language}. - Current Career Status: {input_status}. - Career Goals: {input_goal}. - Skill and Experience: {input_skill}. - Interests: {input_interest}. - Preferred work environment: {input_environment}. - Location:{input_location} - Challenges{input_challenges}."
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
            en_input_status = st.selectbox("Current Career Status",("Student", "Entry-Level Employee", "Senior-Level Employee", "Career Changer", "Unemployed/Job Seeker", "Entrepreneur"),key="en_input_status")
            en_input_goal = st.text_input("Career Goals (e.g., Become recognized as an expert in digital marketing field)", key="en_input_goal")
            en_input_skill = st.text_input("Skills and Experience (e.g., SEO and digital marketing)", key="en_input_skill")
            en_input_interest = st.text_input("Interests (e.g., Data Science and Python)", key="en_input_interest")
            en_input_environment = st.selectbox("Preferred work environment",("Corporate Office", "Startup", "Remote Work", "Freelance/Contract", "Government/Public Sector"),key="en_input_environment")
            en_input_location = st.text_input("Location (e.g., Tokyo)", key="en_input_location")
            en_input_challenges = st.text_input("Challenges (e.g., High competition for jobs in the field, making it difficult to stand out to employers.)", key="en_input_challenges")
            submit_en = st.form_submit_button("Generate a Career Advice")
            if submit_en:
                result = generate_reply(en_input_status, en_input_goal, en_input_skill, en_input_interest, en_input_environment,en_input_location,en_input_challenges, "English")
                st.write(result)
    else:
        # Japanese Input Section
        with st.form(key='ja_form'):
            st.subheader('日本語')
            ja_input_status = st.selectbox("現在のキャリア状況",("学生", "エントリーレベル社員", "シニアレベル社員", "キャリアチェンジャー", "無職/求職中", "起業家"),key="ja_input_status")
            ja_input_goal = st.text_input("キャリアの目標（例: デジタルマーケティング分野の専門家として認められる）", key="ja_input_goal")
            ja_input_skill = st.text_input("スキルと経験（例: SEOとデジタルマーケティング）", key="ja_input_skill")
            ja_input_interest = st.text_input("興味、学びたいこと（例: データサイエンスとPython）", key="ja_input_interest")
            ja_input_environment = st.selectbox("希望する勤務環境",("企業のオフィス", "スタートアップ", "リモートワーク", "フリーランス契約", "政府/公共部門"),key="ja_input_environment")
            ja_input_location = st.text_input("勤務地（例: 東京）", key="ja_input_location")
            ja_input_challenges = st.text_input("課題（例: 分野内の高い競争により、雇用主に目立つのが難しい）", key="ja_input_challenges")
            submit_ja = st.form_submit_button("キャリアアドバイスを生成する")
            if submit_ja:
                result = generate_reply(ja_input_status, ja_input_goal, ja_input_skill, ja_input_interest, ja_input_environment,ja_input_location,ja_input_challenges,"Japanese")
                st.write(result)
else:
    st.error("You have reached your maximum usage limit.")
