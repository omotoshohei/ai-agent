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
以下の構造に厳密に従ってラップを生成してください。完全性と一貫性を確保します：
- 長さ: 正確に8行で、各行に8拍子。
- 韻の構造: ABABの韻の構造を通じてリズミカルで詩的な流れを維持してください。
- 内容: 与えられたトピック、職業、個人的なメッセージを歌詞に反映させてください。テーマの紹介で始め、アイデアを発展させる本文で続き、強いエンディングで結ぶ。
- スタイル: 内韻と多音節の韻を組み込んで歌詞の複雑さを高めてください。
- トーン: 個人的なメッセージの感情に合わせてトーンを調整してください。入力に応じてモチベーショナルから省察的までの範囲です。
各行が次の行にスムーズに移行し、テーマとリズムの連続性を維持してください。8行全部で完全なナラティブアークを提供する必要があります。
- トピック:{topic},
- 職業:{occupation},
- 個人的なメッセージ:{message}
"""

def init_page():
    st.set_page_config(
        page_title="ラップ自動生成AIエージェント",
        page_icon="🎶"
    )
    st.header("ラップ自動生成AIエージェント 🎶")


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
        topic = st.text_input("トピック（例：日曜日）", key="topic")
        occupation = st.text_input("あなたの職業（例：データサイエンティスト）", key="occupation")
        message = st.text_input("伝えたいこと（例：明日に備える）", key="message")
        if st.button("返信を生成する"):
            result = chain.stream({"topic": topic, "occupation": occupation, "message": message})
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