import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

# アプリケーションタイトル
st.title("ハンズオン - チャットボット")

# 使用するモデルの指定
chat = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")

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
    
    # Botメッセージの表示
    messages = [HumanMessage(content=prompt)]
    with st.chat_message("assistant"):
        result_area = st.empty()
        text = ''
        for chunk in chat.stream(messages):
            text += chunk.content
            result_area.write(text)

    # Botの回答内容をチャット履歴に保存
    st.session_state.messages.append({"role": "assistant", "content": text})