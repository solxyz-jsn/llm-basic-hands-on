import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock 
from langchain_community.retrievers.bedrock import AmazonKnowledgeBasesRetriever

# 検索手段を指定
retriever = AmazonKnowledgeBasesRetriever(
    # ナレッジベースIDを指定
    knowledge_base_id = "",
    retrieval_config = {"vectorSearchConfiguration": {"numberOfResults": 10}}
)

# プロンプトのテンプレートを定義
prompt = ChatPromptTemplate.from_template("以下のcontextに基づいて回答してください: {context} / 質問: {question}")

# LLMを指定
model = ChatBedrock(
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs = {
        "max_tokens": 1000,
        "top_p": 0.9,
        "temperature": 0.7,
    },
    streaming = True
)

# チェーンを定義（検索 → プロンプト作成 → LLM呼び出し → 結果を取得）
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# アプリケーションタイトル
st.title("AWS - RAGチャットボット")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴の再表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力によって処理を実行
if user_input := st.chat_input("メッセージを入力してください..."):
    # 入力されたユーザーメッセージの表示
    st.chat_message("user").markdown(user_input)
    
    # 質問内容をチャット履歴に保存
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # ストリーミング形式で生成された回答を出力
    with st.chat_message("assistant"):
        result_area = st.empty()
        text = ''
        for chunk in chain.stream(user_input):
            chunk_content = chunk.content if hasattr(chunk, "content") else str(chunk)
            text += chunk_content
            result_area.write(text)
    
    # 最終的な生成結果をチャット履歴に保存
    st.session_state.messages.append({"role": "assistant", "content": text})
