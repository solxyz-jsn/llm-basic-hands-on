import boto3

# boto3クライアントの作成
client = boto3.client(service_name = 'bedrock-runtime', region_name = "us-west-2")

# Converse APIを使用した回答の生成
response = client.converse(
    # モデルの指定
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    # プロンプトの指定
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": "動物に関する日本のことわざを3つ教えて"
                }
            ]
        }
    ],
    # システムプロンプトの指定
    system = [
        {
            "text": "あなたは日本の知識に詳しい専門家です。質問された内容に対して小学生でもわかるように簡単に回答してください。また、必ず日本語で回答を生成してください。",
        }
    ],
    # パラメータの設定
    inferenceConfig = {
        "maxTokens": 1000,
        "temperature": 0.5,
        "topP": 0.9,
    },
)

# 生成した回答の抽出
response_body = response['output']['message']["content"][0]["text"]

# 回答の出力
print(response_body)
