import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

###### dotenv を利用する場合 ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################


PROMPT = """
1. 課題: ユーザーが報告した感情とその日の計画に直接関連するユニークなモチベーショナルまたはリフレクティブな引用を生成します。
1-1. 引用が具体的な感情的文脈に基づいてサポートまたはインスピレーションを提供することを確認してください。
1-2. スティーブ・ジョブズの引用を使用しないでください。
1-3. 知られざる引用を求め、多様な文化的及び歴史的源泉を考慮することで、選択の多様性と包括性を豊かにしてください。
ユーザーが説明した状況に選んだ引用がどうフィットするかの簡潔な説明を提供してください。

2. 感情: {feeling}.
3. 感情の理由: {reason}.
4. その日の計画: {plan}.
5. 日本語で100語以内で説明してください。
"""


def init_page():
    st.set_page_config(
        page_title="今日の一言AIエージェント",
        page_icon="🧘"
    )
    st.header("今日の一言AIエージェント🧘")


def select_model(temperature=0):
    models = ("GPT-4o","GPT-4o-mini", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model_choice = st.radio("Choose a model:", models)
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
        feeling = st.selectbox(
            "今日の気分はどうですか？",
            ("もっとやる気が出したい", "悲しい気持ちです", "怒っています", "今日はリラックスしたい", "ワクワクしています", "不安です"),
            key="feeling"
        )
        reason = st.text_input("その感情の理由は何ですか？", key="reason")
        plan = st.text_input("今日の予定は何ですか？", key="plan")
        if st.button("Submit"):
            result = chain.stream({"feeling": feeling, "reason": reason, "plan": plan})
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


