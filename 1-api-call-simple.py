import json
import boto3

# boto3クライアントの作成
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Bedrockのモデルにリクエストを送信
response = client.invoke_model(
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.9,
            "top_p": 0.9,
            "messages": [
                {
                    "role": "user",
                    "content": "「人生」を何かに例えてください。その理由も説明してください。",
                }
            ]
        }
    ),
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    accept = "application/json",
    contentType = "application/json",
)

# 生成した回答の抽出
response_body = json.loads(response.get("body").read())
answer = response_body["content"][0]["text"]

print(response_body)
# 生成した回答の出力
print(answer)
