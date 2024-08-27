import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# dotenvを利用する場合
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenvが見つかりません。環境変数を手動で設定してください。", ImportWarning)

PROMPT = """
## タスク: ユーザーの現状と願望に基づいた詳細で個別化されたキャリアアドバイスを提供する。
## ユーザー情報:
- 現在のキャリアステータス: {input_status}
- キャリア目標: {input_goal}
- スキルと経験: {input_skill}
- 興味: {input_interest}
- 好ましい職場環境: {input_environment}
- 場所: {input_location}
- 課題: {input_challenges}

## 目的: 短期的および長期的な目標を達成するのに役立つ行動可能でサポート的なキャリアアドバイスを提供する。課題の克服、スキルの活用、興味や好ましい職場環境との調和に焦点を当てた戦略を含める。ユーザーの独自の状況に合わせた具体的なヒントと推奨事項を提供する。
## 追加: アドバイスが明確で実用的であり、ユーザーがキャリアパスについて情報に基づいた決定をするのに役立つようにする。
"""

def init_page():
    st.set_page_config(page_title="キャリアアドバイスツール", page_icon="🧘")
    st.header("キャリアアドバイスツール🧘")


def select_model(temperature=0):
    models = ("GPT-4o","GPT-4o-mini", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model_choice = st.radio("モデルを選択:", models)
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
        input_status = st.selectbox("現在のキャリアステータス",("学生", "初級職員", "上級職員", "キャリアチェンジャー", "無職・求職中", "起業家"),key="input_status")
        input_goal = st.text_input("キャリア目標（例：デジタルマーケティングの専門家として認知されること）", key="input_goal")
        input_skill = st.text_input("スキルと経験（例：SEOとデジタルマーケティング）", key="input_skill")
        input_interest = st.text_input("興味（例：データサイエンスとPython）", key="input_interest")
        input_environment = st.selectbox("好ましい職場環境",("企業オフィス", "スタートアップ", "リモートワーク", "フリーランス・契約", "政府・公共セクター"),key="input_environment")
        input_location = st.text_input("場所（例：東京）", key="input_location")
        input_challenges = st.text_input("課題（例：分野内の仕事における競争が激しく、雇用者に目立つことが困難）", key="input_challenges")
        if st.button("提出"):
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


