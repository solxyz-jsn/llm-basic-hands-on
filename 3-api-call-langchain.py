from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

# 使用するモデルとパラメータの指定
chat = ChatBedrock(
    # モデルの指定
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    
    # パラメータの設定
    model_kwargs = {
        "max_tokens": 1000,
        "top_p": 0.9,
        "temperature": 0.7,
    }
)

# プロンプトの設定
messages = [HumanMessage(content = "秋の俳句を詠んで")]

# 回答の生成を行い、生成内容を逐次出力
for chunk in chat.stream(messages):
    print(chunk.content, end = "", flush = True)
