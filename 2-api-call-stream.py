import boto3
import json

# boto3クライアントの作成
client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

# Bedrockモデルにストリーミングでリクエストを送信
response = client.invoke_model_with_response_stream(
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": "春の俳句を1句詠んで"
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.7,
            "top_p": 0.9,
        }
    ),
    modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', 
    accept='application/json',
    contentType='application/json'
)

# ストリーミングレスポンスの各チャンクからテキストデータを抽出し、リアルタイムで出力
for event in response.get('body', []):
    if chunk := event.get('chunk'):
        chunk_data = json.loads(chunk.get('bytes').decode())
        if text := chunk_data.get('delta', {}).get('text'):
            print(text, end='', flush=True)