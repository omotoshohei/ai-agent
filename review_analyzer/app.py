import streamlit as st
import openai

# Streamlit page configuration
st.set_page_config(page_title="Review Analyzer", page_icon=":bar_chart:")

# Load secrets
openai.api_key = st.secrets['OPENAI_API_KEY']
prompt = st.secrets['PROMPT_REVIEW_ANALYZER']

# Title of the page
st.title('Product Review Analyzer')

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

# Initialize or retrieve the usage count and language from session state
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

max_uses = 3

# Define a function to handle API requests and increase modularity
def analyze_review(input_brand, input_product, input_region, language):
    st.session_state['usage_count'] += 1
    with st.spinner('Loading... Please wait.'):
        user_prompt = f"- Task: {prompt} - Output language: {language}. - Brand: {input_brand}. - Product: {input_product}. - Region: {input_region}. - Explain within 180 words in English, or 600 charactors in Japanese.- Display with only single language. Don't mix Japanese and English."
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
            en_input_brand = st.text_input("Enter the brand name (e.g., Nike)", key="en_input_brand")
            en_input_product = st.text_input("Enter the product name (e.g., Air Force One shoes)", key="en_input_product")
            en_input_region = st.text_input("Enter your region (e.g., USA)", key="en_input_region", value="USA")
            submit_en = st.form_submit_button("Analyze the review")
            if submit_en:
                result = analyze_review(en_input_brand, en_input_product, en_input_region, "English")
                st.write(result)
    else:
        # Japanese Input Section
        with st.form(key='ja_form'):
            st.subheader('日本語')
            ja_input_brand = st.text_input("ブランド名を入力ください（例：Nike）", key="ja_input_brand")
            ja_input_product = st.text_input("商品名を入力ください (例：エアフォースワンの靴)", key="ja_input_product")
            ja_input_region = st.text_input("集めるレビューの国を指定ください (例：日本)", key="ja_input_region", value="日本")
            submit_ja = st.form_submit_button("レビューを分析する")
            if submit_ja:
                result = analyze_review(ja_input_brand, ja_input_product, ja_input_region, "Japanese")
                st.write(result)
else:
    st.error("You have reached your maximum usage limit.")

