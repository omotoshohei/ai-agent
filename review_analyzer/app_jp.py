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
## 課題: 当社の製品「レビューアナライザー」の顧客レビューを分析します。購入を検討している可能性のある顧客に役立つ重要なポイントを抽出することに焦点を当ててください。全体的な顧客満足度を判断するために感情分析を含めます。
## レビューサイト: Facebook、Instagram、その他の製品の市場存在に基づいた関連フォーラムからレビューを収集してください。
## 目的: 現在のユーザーが製品についてどう思っているかについて、潜在的な顧客に明確で簡潔な要約を提供することです。最も称賛されている機能、一般的な問題、および一般的な感情を強調してください。
## 追加: レビューの出典と分析した投稿数を示しながら、約200語で分析を要約します。要約は直截的で理解しやすく、購入決定を支援するために調整されていることを確認してください。
- ブランド: {brand},
- 製品:{product},
- 地域: {region}
"""

def init_page():
    st.set_page_config(
        page_title="商品レビュー確認AIエージェント",
        page_icon="🔍"
    )
    st.header("商品レビュー確認AIエージェント🔍")


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
        brand = st.text_input("ブランド名を入力してください（例：ナイキ）", key="brand")
        product = st.text_input("製品名を入力してください（例：エアフォースワンシューズ）", key="product")
        region = st.text_input("地域を入力してください（例：アメリカ）", key="region", value="USA")
        if st.button("Submit"):
            result = chain.stream({"brand": brand, "product": product, "region": region})
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