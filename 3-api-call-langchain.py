from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

chat = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")

messages = [HumanMessage(content="秋の俳句を詠んで")]

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)