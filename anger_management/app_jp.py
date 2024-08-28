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
あなたはアンガーマネジメントを専門とするAIアシスタントです。以下の情報に基づいて、ユーザーが怒りを管理するための思慮深く、実用的で効果的なアドバイスを提供することがあなたの仕事です：
- 怒っている相手：{who}
- 怒りの具体的な原因：{content}

1. ユーザーの感情を認めて感情を認証します。
2. 怒りを管理し、軽減するための実践的なステップやテクニックを提供します。
3. 根本的な問題に建設的な方法で対処するように促します。
4. 将来同様の状況で役立つ追加のリソースやヒントを提供します。
"""

def init_page():
    st.set_page_config(page_title="アンガーマネジメント🧘AIエージェントナビ", page_icon="🧘")
    st.header("アンガーマネジメント🧘AIエージェントナビ")

def select_model(temperature=0):
    models = ("GPT-4o", "GPT-4o-mini", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
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
    prompt = ChatPromptTemplate.from_messages([("user", PROMPT)])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

def main():
    init_page()
    chain = init_chain()
    if chain:
        who = st.text_input("怒っている相手は誰ですか？", key="who")
        content = st.text_area("怒りの具体的な原因は何ですか？", key="content")
        if st.button("送信"):
            result = chain.stream({"who": who, "content": content})
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