import streamlit as st
import boto3
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain.schema import HumanMessage

# Amazon Bedrock clientの設定
def get_bedrock_client():
    return boto3.client(
        service_name = 'bedrock-runtime',
        region_name = 'us-west-2' 
    )

# ストリーミング形式の回答を生成
def generate_answer_streaming(query, vectorstore, bedrock_client):
    # ベクトル化に使用するモデルの設定
    embeddings = BedrockEmbeddings(
        client = bedrock_client,
        model_id = "cohere.embed-multilingual-v3"
    )

    # ユーザーの質問をベクトル化
    question_embedding = embeddings.embed_query(query)

    # ベクトルストアで質問に最も関連するドキュメントを検索
    docs = vectorstore.similarity_search_by_vector(question_embedding, k = 5)

    # 検索結果を1つのコンテキストとしてまとめる
    context = "\n".join([doc.page_content for doc in docs])

    # 回答の生成に使用するモデルの設定
    llm = ChatBedrock(
        client = bedrock_client,
        # TODO：Llama 3.2 モデルに変更予定
        model_id = "us.meta.llama3-2-90b-instruct-v1:0",
        streaming = True
    )
    
    # プロンプトのテンプレートを定義
    prompt = ChatPromptTemplate.from_template("以下のcontextに基づいて回答してください: {context} / 質問: {question}")

    # プロンプトを生成
    formatted_prompt = prompt.format(context = context, question = query)

    # HumanMessage形式でプロンプトを作成
    messages = [
        HumanMessage(content = formatted_prompt)
    ]

    # LLMで回答の生成
    return llm.stream(messages)

# Bedrock Clientの初期化
bedrock_client = get_bedrock_client()

# Chromaベクトルストアの読み込み
vectorstore = Chroma(
    collection_name = "pdf_embeddings",
    persist_directory = "./chroma_db"
)

# アプリケーションタイトル
st.title("Langchain - RAGチャットボット")

# チャット履歴の初期化
if "messages" not in st.session_state:
  st.session_state.messages = []

# チャット履歴の再表示
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# ユーザーからの入力によって処理を実行
if prompt := st.chat_input("メッセージを入力してください..."):
   # 入力されたユーザーメッセージの表示
  st.chat_message("user").markdown(prompt)

  # 質問内容をチャット履歴に保存
  st.session_state.messages.append({"role": "user", "content": prompt})

  # ユーザーの質問に基づき回答を生成
  response_generator = generate_answer_streaming(prompt, vectorstore, bedrock_client)

  # ストリーミング形式で生成された回答を出力
  with st.chat_message("assistant"):
    result_area = st.empty()
    text = ''
    for chunk in response_generator:
      chunk_content = chunk.content if hasattr(chunk, "content") else str(chunk)
      text += chunk_content
      result_area.write(text)

  # Botの回答内容をチャット履歴に保存
  st.session_state.messages.append({"role": "assistant", "content": text})
  