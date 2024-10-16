import boto3

# boto3クライアントの作成
client = boto3.client(service_name = 'bedrock-runtime', region_name = "us-west-2")

# Converse APIを使用した回答の生成
response = client.converse_stream(
    modelId = "us.meta.llama3-2-90b-instruct-v1:0",
    messages = [
        {
            "role": "user",
            "content": [{"text": "動物に関する日本のことわざを3つ教えて"}]
        }
    ],
    system = [
        {
            "text": "あなたは動物の知識に詳しい専門家です。質問された内容に対して小学生でもわかるように簡単に回答してください。また、必ず日本語で回答を生成してください。",
        }
    ],
    inferenceConfig = {
        "maxTokens": 1000,
        "temperature": 0.5,
        "topP": 0.9,
    },
)

# ストリーミングレスポンスの各チャンクからテキストデータを抽出し、リアルタイムで出力
stream = response.get('stream')
if stream:
    for event in stream:
        if delta := event.get('contentBlockDelta', {}).get('delta', {}).get('text'):
            print(delta, end="", flush=True)
